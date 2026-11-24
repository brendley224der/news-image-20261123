# The World Today — Sunday 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/brendley224der/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/brendley224der/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A one-image newspaper front page summing up the world's news of
Sunday 23 November 2026. Entry for the make.fun bounty
[`news-image-20261123`](https://make.fun/c/news-image-20261123)
("Sum up 23 November's world news in one image", $100 USDC, top 50 share).

## The front page

- **Lead:** Bahrain demands UN action after Iran's Revolutionary Guards
  claim missile and drone strikes on US positions at Al-Riffa and Awali;
  Bahrain says a civilian plant was hit and set ablaze, with two people hurt.
- **Ukraine war:** a Russian cargo ship is still burning off Finland after
  an attack; 14 people are missing after a drone hit flats in the Kyiv region.
- **Climate:** the COP31 final draft in Turkiye drops the words "fossil fuels"
  as talks stall.
- **Asia:** South Korea's education minister resigns amid an AI exam-cheating
  scandal.
- **Diplomacy:** Nepal's PM Balendra Shah holds talks with PM Modi in Delhi.
- **Cricket:** India post a record 720 for 9 in the Wellington Test.
- **Europe:** thousands march in Lisbon over living costs.
- **Also today:** UN states keep talking on lethal AI weapons; Myanmar calls
  an ASEAN move unfair; 7 dead and 50 missing in an Indonesia factory fire;
  Mexico seizes "El Chapo Isidro", 11 dead; Eisenkot calls settler arson
  "Jewish terrorism".

News as reported on the morning of 23 November 2026 (Arab News front page,
Dunya News, Jagran Josh / Observer Voice roundups, wire reports).

## How it is made

`main.py` draws the 1024x1024 PNG from scratch with the Python standard
library only — a tiny framebuffer, a hand-made 5x7 bitmap font and a
minimal PNG writer (no Pillow, no numpy). The output is deterministic:
running it twice writes byte-identical files.

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

In the grader the program writes `/output/entry.png`
(`MAKEFUN_OUTPUT_DIR` or `/output`).

## License

MIT. See [LICENSE](LICENSE).
