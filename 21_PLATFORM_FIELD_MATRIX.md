# 21 Platform Field and Collector Matrix

Use this as a collector-planning reference. Re-check current provider docs at runtime.

| Platform | Primary object | Secondary object | Core fields to capture | Preferred access | Notes |
|---|---|---|---|---|---|
| YouTube | video | comment/reply | IDs, text, timestamp, parent, likes/replies, URL | official Data API | commentThreads pagination; use comments endpoint for full replies |
| Reddit | submission | comment/reply | IDs, subreddit, title/body, text, score, timestamp, parent, URL | official API | preserve tree structure |
| X | post | reply/quote | ID, text, timestamp, public engagement, conversation ID, URL | official API | fields depend on access tier |
| TikTok | video | comment/reply | video ID, text, timestamp, likes/replies, parent | Research API if approved | research access and fields are eligibility-dependent |
| Instagram | media | comment/reply | media ID, text, timestamp, engagement fields available | official Meta access | permissions may limit public comment availability |
| Facebook | post | comment/reply | post ID, text, timestamp, engagement fields available | official Meta access | public-page/group access varies; never use private data |
| Threads | post | reply | post ID, text, timestamp, engagement fields available | official Threads/Meta access | permissions/access may vary |
| Forum | thread | post/reply | URL, title, author hash, timestamp, text, parent | permitted public HTML/API | follow site rules |
| Marketplace | product | review | product, rating, review text, date, verified status if explicit | permitted public/API | do not infer verified purchase |

## Common collector requirements

Every connector must support:

- pagination;
- checkpointing;
- retry/backoff;
- raw capture;
- provenance;
- rate-limit handling;
- source-level status;
- structured error logging.

## API efficiency

Do not make one request per item when batch endpoints exist. For YouTube, exploit pagination and batch-compatible ID retrieval. For TikTok Research comments, respect documented maximum page sizes and cursors. For all services, log actual returned counts rather than relying on advertised totals.
