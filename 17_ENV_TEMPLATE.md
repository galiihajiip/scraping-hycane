# 17 Environment Template

Copy this to `.env` and keep it out of Git.

```env
YOUTUBE_API_KEY=
REDDIT_CLIENT_ID=
REDDIT_CLIENT_SECRET=
REDDIT_USER_AGENT=
X_API_KEY=
X_API_SECRET=
X_BEARER_TOKEN=
META_APP_ID=
META_APP_SECRET=
META_ACCESS_TOKEN=
THREADS_ACCESS_TOKEN=
TIKTOK_CLIENT_KEY=
TIKTOK_CLIENT_SECRET=
TIKTOK_ACCESS_TOKEN=
SEARCH_API_KEY=
OPENALEX_MAILTO=
SEMANTIC_SCHOLAR_API_KEY=
CROSSREF_MAILTO=
LLM_API_KEY=
S3_ENDPOINT=
S3_ACCESS_KEY=
S3_SECRET_KEY=
S3_BUCKET=
```

Never print or commit secrets. Mask them in logs.

Likely package families: requests/httpx, pydantic, pandas/polars, pyarrow, numpy, scikit-learn, scipy, statsmodels, matplotlib/plotly, BeautifulSoup/lxml, Playwright where permitted, tenacity, tqdm, python-dotenv, fastText/langdetect, sentence-transformers, BERTopic/UMAP/HDBSCAN, nltk/spacy as useful, rapidfuzz, datasketch, jinja2. Pin tested versions after implementation.
