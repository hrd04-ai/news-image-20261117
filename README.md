[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/hrd04-ai/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/hrd04-ai/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

# The World in One Day — 17 November 2026

A newspaper front-page infographic that sums up Tuesday 17 November 2026 in
one image: a bold masthead naming the day, then six panels covering the day's
most consequential stories across regions and fields — the Kerch Bridge span
collapsing after a Ukrainian strike, Trump landing in Manila for the ASEAN
summit, two tankers hit by mines in the Strait of Hormuz, a software bug
slowing JPMorgan banking, Nvidia reporting earnings after Jensen Huang's
exit, and a ULA Vulcan rocket failing with 40 Amazon Leo satellites lost.
Each panel pairs a simple drawn pictogram with a short headline and one
factual sublabel, so the whole day reads clearly from the image alone. The
image is drawn locally with Pillow (`make_image.py`) and shipped as a
finished `entry.png`; `main.py` (standard library only) simply copies it to
the output path, so both grader runs produce byte-identical output.

## How to run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

This writes the image to `out/entry.png` (1024x1024 PNG, under 1 MiB).

## License

MIT — see `LICENSE`.
