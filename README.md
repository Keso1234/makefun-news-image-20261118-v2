# The World in One Day — 18 November 2026 (v2)

[![make.fun](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/Keso1234/makefun-news-image-20261118-v2/rank.svg)](https://make.fun/bounty/news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/Keso1234/makefun-news-image-20261118-v2/reward.svg)](https://make.fun/bounty/news-image-20261118)

An entry for the [make.fun](https://make.fun) bounty
[news-image-20261118](https://make.fun/bounty/news-image-20261118):
sum up 18 November 2026's world news in one image.

## What it is

A magazine-cover poster of Wednesday 18 November 2026, drawn entirely
by code (PIL, no photographs). v2 of our entry: v1, a newspaper front
page, scored 97.9552% (rank 1,758 of 12,730) against a 98.6458% pay
cutoff, so v2 keeps the same verified stories but rebuilds the design
around legibility at thumbnail size — a much bigger masthead and date
band, a 70 pt lead headline, 30 pt story headlines, and far fewer words.

- **Lead story — Gulf war escalates:** the U.S. hit an Iranian missile
  site on Qeshm Island; Iran struck back at U.S. bases in Kuwait
  and Bahrain.
- **Xi & Putin meet in Shenzhen** ahead of Thursday's three-way summit
  with Trump.
- **Kerch Bridge hit** — a Ukrainian strike drops a road span into
  the strait.
- **Peltola flips Alaska** — Democrats take a 56–44 Senate majority.
- **Measles-free status lost** — 5,412 U.S. cases in 2026, after
  26 years.
- **Voyager 1 goes further than ever** — one light-day out, 16 billion
  miles from Earth.
- Ticker: Ebola in DR Congo passes 11,000 cases; Nvidia posts a record
  $115.8B quarter; Israel elects Matan Kahana speaker.

Sources: Reuters, Associated Press, AFP, NASA, WHO.

## How it runs

`main.py` (Python 3.13, standard library only) copies `entry.png` to
`/output/entry.png`. `generate.py` is the program that drew the image;
re-running it reproduces the exact same bytes (fixed seed, no clock,
no network).

```sh
python3 generate.py entry.png   # rebuild the image
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see [LICENSE](LICENSE).
