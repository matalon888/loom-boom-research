# Raw corpora

| File | Rows | What it is |
|---|---|---|
| `play_reviews.json` | 746 | Google Play reviews for `com.loom.android`, 15 storefronts, 3 sort orders + explicit 1/2/3-star sweeps |
| `ios_reviews.json` | 625 | Apple App Store reviews for app id `1474480829`, 20 country storefronts, via the public RSS review feed |
| `reddit_rel.json` | 220 | Reddit posts/comments where Loom-the-product is genuinely the subject, filtered from 2,833 scraped rows across 40 subreddits |
| `hn_comments.json` | 318 | Hacker News comments expressing an opinion about Loom (link-only mentions removed), from 956 Algolia hits |

All fields are as returned by the source, plus a `src` / `sub` tag noting where each row came from.
