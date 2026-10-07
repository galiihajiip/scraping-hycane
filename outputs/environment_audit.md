# Environment Audit

Audit date: 2026-10-08 (UTC). Machine: Apple M1 Pro, 8 cores, 16 GB RAM, macOS (Darwin 25.2.0).

| Item | Status | Notes |
|---|---|---|
| Python | 3.13.13 (miniforge) | Project venv at `.venv/` |
| pip / venv | OK | Pinned versions in `requirements.txt` |
| Core packages | Installed | pandas, pyarrow, numpy, scikit-learn, scipy, statsmodels, requests, beautifulsoup4, lxml, datasketch, emoji, PyYAML, python-dotenv |
| NLP packages | Installed | torch (MPS backend available), transformers, sentence-transformers, bertopic, umap-learn, hdbscan, lingua-language-detector, vaderSentiment |
| Visualization | Installed | matplotlib (static PNG/SVG), plotly.js via cdnjs (dashboard) |
| Browser automation | Playwright + headless Chromium installed | Used **only** to render and QA the local dashboard; not used for scraping |
| Node | v26.8.2 | Available; not used by the pipeline |
| Internet connectivity | OK | Endpoint tests in `source_access_audit.md` |
| GPU/accelerator | Apple MPS | Transformer inference runs on MPS |
| Storage | ~210 GB free | Raw captures are gzip JSON |
| `.env` | Created 2026-10-08 with `YOUTUBE_API_KEY` only (permissions 600, git-ignored) | Initially absent; `.env.example` created. Values never printed in logs |
| API credentials | YouTube Data API only | Reddit OAuth, X, Meta, Threads, TikTok, Semantic Scholar, search API keys absent |
| Git | Initialised by this run | `.gitignore` excludes `.env`, `.venv/`, raw/bronze/silver data, caches |

## Consequences
- X API, Meta/Threads, TikTok Research API and Reddit OAuth are `NOT_CONFIGURED`. YouTube Data API was enabled mid-run after the user supplied a key.
- Collection used the YouTube Data API (with key), keyless public APIs, and robots-compliant public HTML only.
