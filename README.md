# The Loom Complaint Ledger

A competitive teardown of **Loom**, built from 4,500 first-party user comments, and turned into a product backlog and go-to-market plan for [Boom Share](https://boomshare.ai).

## Three public pages

| | |
|---|---|
| 📄 **[The Complaint Ledger](https://matalon888.github.io/loom-boom-research/)** | The teardown: what Loom's users complain about, ranked, turned into a backlog |
| 🧲 **[Acquisition Playbook](https://matalon888.github.io/loom-boom-research/playbook.html)** | How every competitor grows *without* paid search — sitemap evidence + nine plays |
| 🧭 **[Strategy Memo](https://matalon888.github.io/loom-boom-research/strategy.html)** | Where the uncontested ground actually is — the paid distribution loop, social, and Boom Match |
| 📣 **[Team Memo](https://matalon888.github.io/loom-boom-research/memo.html)** | The one-page internal brief — the plot, the reasoning, and who does what |
| 🧠 **[Screen Recall Campaign](https://matalon888.github.io/loom-boom-research/recall.html)** | The invented sub-niche merging recorder + memory game, with an 80-creator cross-platform roster |
| 📱 **[Mobile Design](https://matalon888.github.io/loom-boom-research/mobile.html)** | How Boom Match works on phones — screenshots instead of live capture, plus the privacy rules |
| 📉 **[Funnel Model](https://matalon888.github.io/loom-boom-research/funnel.html)** | 57.8M views modelled down to a paying desktop user — and why credits must pay for it |
| 🖼️ **[Photo Questions](https://matalon888.github.io/loom-boom-research/photos.html)** | 21 memory questions built from photo EXIF + on-device vision, with scoring and share-card rules |
| 🔐 **[Data Access](https://matalon888.github.io/loom-boom-research/access.html)** | Every data source we could ask for, with what it really costs to get |
| 📋 **[The Roster](https://matalon888.github.io/loom-boom-research/roster.html)** | All 80 creators, sortable and searchable, with fees, reach and CPM |
| 🎯 **[The 50 Creators](https://matalon888.github.io/loom-boom-research/creators.html)** | 50 X creators whose output is already screen recordings — ranked, with the $20-referral DM |
| 💬 **[1,795 Raw Comments](https://matalon888.github.io/loom-boom-research/comments.html)** | Every user comment behind it, searchable and filterable |

---

## What's in here

| Path | What it is |
|---|---|
| `docs/index.html` | The teardown report |
| `docs/playbook.html` | The competitor acquisition playbook |
| `docs/strategy.html` | The strategy memo — paid distribution loop, social, Boom Match |
| `docs/recall.html` | The Screen Recall campaign + 80-creator roster |
| `docs/creators.html` | The 50-creator recruitment list + outreach |
| `docs/comments.html` | The searchable raw-comment explorer |
| `data/` | The raw scraped corpora as JSON — see `data/README.md` |
| `scripts/` | Every scraper and analysis script used, so the numbers are reproducible |

## The corpus

| Source | Volume | Method |
|---|---|---|
| Google Play | **746** text reviews | `com.loom.android`, 15 storefronts × 3 sort orders + explicit 1/2/3-star sweeps |
| Apple App Store | **625** reviews | App id `1474480829`, public RSS review feed, 20 country storefronts |
| Reddit | **2,833** rows → **220** relevant → 507 mention windows | 40 subreddits, filtered to threads where Loom-the-product is genuinely the subject |
| Hacker News | 956 items → **318** comments | Algolia API, link-only mentions removed |
| Capterra / Trustpilot | 529-review aggregate + verbatims | Read directly |

## Headline findings

**1. The rating split is the opening.** Loom is 3.2★ on Google Play (5,565 ratings) and 4.7–4.8★ everywhere buyers rate the *service*. People love the product and hate the software.

**2. The top complaint isn't price — it's losing your work.** Across 661 negative app reviews: login/account 20%, crashes 17%, hung uploads 15%, can't download 14%. Folded together, roughly a third of all negative reviews are some version of *"I recorded something important and Loom lost it"* — usually with real stakes attached.

**3. Reddit and HN argue economics, not bugs.** 135 mentions of price, seats and billing. The 5-minute / 25-video free caps are the churn trigger; you can't download your own MP4 even on a paid plan; and in **February 2026 Atlassian deleted Loom's free Creator Lite seats**, auto-converting them to paid. Reported result: a team with 90 passive viewers going from $240 to $24,000 a year.

**4. Nobody is solving watch-through.** Two independent threads report the same thing — a 15-second median view on a two-minute walkthrough. Every competitor races on production polish; the actual failure is on the consumption side.

**5. Loom monetises at roughly $2 per registered user per year.** $50M ARR (Oct 2023, last public) across 25M+ registered users. The category leader never solved conversion, which means nobody has proven the pricing model to beat.

## Reproducing

```bash
python3 -m venv venv && ./venv/bin/pip install google-play-scraper requests
./venv/bin/python scripts/play_scrape.py     # Google Play
python3 scripts/appstore.py                  # Apple App Store (stdlib only)
python3 scripts/hn.py && python3 scripts/hn_c.py   # Hacker News
./venv/bin/python scripts/analyze.py         # theme counts
./venv/bin/python scripts/quotes.py          # verbatims per theme
```

Reddit collection used a third-party scraping actor (Reddit blocks direct API access); `scripts/red_an.py` and `scripts/red_q2.py` do the filtering and theming on its output.

## Caveats

- Written reviews skew negative on both app stores. The percentages describe the shape of complaints **among complainers**, not the share of all users affected.
- Trustpilot and G2 blocked direct collection and are represented by summaries rather than a full verbatim corpus.
- Chrome Web Store reviews — likely Loom's largest single review pool — could not be pulled and are absent entirely.
- Reddit collection was stopped early at the scraper budget, so 220 relevant threads is a floor, not a ceiling.
- Market figures are third-party estimates where noted. Loom's last public ARR is October 2023; nothing has been disclosed since the Atlassian acquisition.

Collected 19 August 2026.
