"""Shared utilities: config, paths, HTTP with retry/backoff/ledger, raw capture, checkpoints."""
from __future__ import annotations

import csv
import gzip
import hashlib
import json
import os
import random
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
import yaml
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")

STATUS = ("SUCCESS", "PARTIAL", "BLOCKED", "FAILED", "NOT_CONFIGURED", "EXHAUSTED")


def load_yaml(name: str) -> dict:
    with open(ROOT / "config" / name) as f:
        return yaml.safe_load(f)


PROJECT = load_yaml("project.yaml")
SOURCES = load_yaml("source_targets.yaml")


def utcnow() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def new_run_id(prefix: str) -> str:
    return f"{prefix}_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"


def env_present(*keys: str) -> bool:
    """True if all keys are set and non-empty. Never returns or logs the values."""
    return all(bool(os.environ.get(k, "").strip()) for k in keys)


def sha256(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8", "ignore")).hexdigest()


def author_hash(platform: str, author: str | None) -> str | None:
    if not author or author in ("[deleted]", "[removed]"):
        return None
    salt = os.environ.get("AUTHOR_HASH_SALT", "hycane-default-salt")
    return sha256(f"{salt}|{platform}|{author}")[:20]


# ---------------------------------------------------------------- ledger
_ledger_lock = threading.Lock()
LEDGER_PATH = ROOT / "data" / "logs" / "request_ledger.csv"
LEDGER_FIELDS = ["ts", "source", "endpoint_class", "query_id", "page", "status", "http_status",
                 "result_count", "retries", "latency_ms", "note"]


def ledger(**row):
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    new = not LEDGER_PATH.exists()
    row = {k: row.get(k, "") for k in LEDGER_FIELDS} | {"ts": utcnow()}
    with _ledger_lock, open(LEDGER_PATH, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=LEDGER_FIELDS)
        if new:
            w.writeheader()
        w.writerow(row)


# ---------------------------------------------------------------- http
class Http:
    """Polite HTTP client: per-source min interval, exponential backoff, honours Retry-After."""

    def __init__(self, source: str, min_interval_s: float = 1.0, headers: dict | None = None,
                 fixed_backoff_s: float | None = None):
        self.source = source
        self.fixed_backoff = fixed_backoff_s
        self.min_interval = min_interval_s
        self.s = requests.Session()
        self.s.headers["User-Agent"] = PROJECT["http"]["user_agent"]
        if headers:
            self.s.headers.update(headers)
        self._last = 0.0

    def _wait(self):
        dt = time.time() - self._last
        if dt < self.min_interval:
            time.sleep(self.min_interval - dt)
        self._last = time.time()

    def get(self, url: str, params: dict | None = None, endpoint_class: str = "", query_id: str = "",
            page: Any = "", expect_json: bool = True, max_retries: int | None = None):
        """Returns (status, http_status, payload|None). Never raises on HTTP errors."""
        max_retries = PROJECT["http"]["max_retries"] if max_retries is None else max_retries
        base = PROJECT["http"]["backoff_base_s"]
        retries = 0
        while True:
            self._wait()
            t0 = time.time()
            try:
                r = self.s.get(url, params=params, timeout=PROJECT["http"]["timeout_s"])
                code = r.status_code
            except requests.RequestException as e:
                code, r = 0, None
                err = type(e).__name__
            lat = int((time.time() - t0) * 1000)
            retryable = code in (0, 429, 500, 502, 503, 504, 520, 522, 524)
            payload = None
            if r is not None and code == 200:
                try:
                    payload = r.json() if expect_json else r.text
                except ValueError:
                    payload, code, retryable = None, -1, True
                # Arctic Shift signals overload with 200/422 + error payload
                if isinstance(payload, dict) and payload.get("error") and "slow down" in str(payload.get("error")).lower():
                    payload, retryable = None, True
            if r is not None and code == 422 and "slow down" in r.text.lower():
                retryable = True
            if payload is not None:
                n = _count(payload)
                ledger(source=self.source, endpoint_class=endpoint_class, query_id=query_id, page=page,
                       status="SUCCESS", http_status=code, result_count=n, retries=retries, latency_ms=lat)
                return "SUCCESS", code, payload
            if retryable and retries < max_retries:
                retries += 1
                wait = base * (2 ** (retries - 1)) + random.uniform(0, 1)
                if self.fixed_backoff:
                    wait = self.fixed_backoff * (1 + 0.25 * retries) + random.uniform(0, 2)
                if r is not None and r.headers.get("Retry-After", "").isdigit():
                    wait = max(wait, int(r.headers["Retry-After"]))
                time.sleep(min(wait, 180))
                continue
            status = "BLOCKED" if code in (401, 403) else "FAILED"
            note = (r.text[:200].replace("\n", " ") if r is not None else locals().get("err", ""))
            ledger(source=self.source, endpoint_class=endpoint_class, query_id=query_id, page=page,
                   status=status, http_status=code, result_count=0, retries=retries, latency_ms=lat, note=note)
            return status, code, None


def _count(payload) -> int:
    if isinstance(payload, list):
        return len(payload)
    if isinstance(payload, dict):
        for k in ("data", "posts", "items", "hits", "results", "comments", "message"):
            v = payload.get(k)
            if isinstance(v, list):
                return len(v)
            if isinstance(v, dict) and isinstance(v.get("items"), list):
                return len(v["items"])
        return 1
    return 1 if payload else 0


# ---------------------------------------------------------------- raw capture
def save_raw(platform: str, run_id: str, name: str, payload: Any, meta: dict) -> str:
    """Immutable gzip JSON capture. Returns path relative to ROOT. Never overwrites."""
    d = ROOT / "data" / "raw" / platform / run_id
    d.mkdir(parents=True, exist_ok=True)
    safe = "".join(c if c.isalnum() or c in "-_." else "_" for c in name)[:150]
    p = d / f"{safe}.json.gz"
    i = 1
    while p.exists():
        p = d / f"{safe}__{i}.json.gz"
        i += 1
    with gzip.open(p, "wt", encoding="utf-8") as f:
        json.dump({"meta": meta | {"captured_at": utcnow(), "run_id": run_id}, "payload": payload}, f,
                  ensure_ascii=False)
    return str(p.relative_to(ROOT))


def iter_raw(platform: str):
    """Yield (relpath, meta, payload) for every raw capture of a platform."""
    for p in sorted((ROOT / "data" / "raw" / platform).rglob("*.json.gz")):
        with gzip.open(p, "rt", encoding="utf-8") as f:
            obj = json.load(f)
        yield str(p.relative_to(ROOT)), obj["meta"], obj["payload"]


# ---------------------------------------------------------------- checkpoints
class Checkpoint:
    def __init__(self, name: str):
        self.path = ROOT / "data" / "checkpoints" / f"{name}.json"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.state = json.loads(self.path.read_text()) if self.path.exists() else {}

    def done(self, key: str) -> bool:
        return key in self.state.get("done", {})

    def mark(self, key: str, info: Any = True):
        self.state.setdefault("done", {})[key] = info
        self.save()

    def save(self):
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(self.state, indent=1))
        tmp.replace(self.path)


def append_csv(path: Path, rows: list[dict], fields: list[str]):
    path.parent.mkdir(parents=True, exist_ok=True)
    new = not path.exists()
    with open(path, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        if new:
            w.writeheader()
        w.writerows(rows)


RUNS_PATH = ROOT / "data" / "manifests" / "collection_runs.csv"
RUN_FIELDS = ["run_id", "source", "started_at", "ended_at", "status", "requests", "raw_files", "objects", "note"]


def log_run(**row):
    append_csv(RUNS_PATH, [row], RUN_FIELDS)
