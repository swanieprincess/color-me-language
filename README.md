# Color Me Language

Source files for **The Learning Dojo**, a series of multilingual children's
coloring books. Every page is one cute, cartoony animal
drawn as clean black line art, with its name in four scripts set in outline
lettering so the words can be colored too:

- **English**
- **Korean** (hangeul)
- **Japanese** (hiragana / katakana)
- **Hanja / Chinese** (traditional characters)

This repository holds the source of truth for each book: the page manifests and
word lists, the page template, the art direction, and the series plan. The
layouts themselves are built in Moda (links in each book's README) and exported
as print-ready PDFs for Amazon KDP.

## Books

| # | Title | Status | Pages |
|---|-------|--------|-------|
| 1 | The Learning Dojo: Animals, Volume 1 | interior and full-wrap cover built in Inkscape (34 pages) | 34 |
| 2 | Under the Sea, Part 1 — Fish & Seaweed | word list drafted ([books/under-the-sea-1-fish](books/under-the-sea-1-fish/README.md)) | 32 |
| 3 | Under the Sea, Part 2 — Crustaceans | planned | — |
| 4 | Under the Sea, Part 3 — Other sea life | planned | — |
| 5 | Insects | planned | — |
| 6 | Amphibians | planned | — |
| 7 | Reptiles | planned | — |

See [docs/series-plan.md](docs/series-plan.md) for scope rules and candidate
animal lists for each book.

## Layout

- Page: US Letter, 8.5 × 11 in (816 × 1056 px at 96 dpi in Moda).
- The drawing fills the page inside a rounded frame; themed trinkets surround
  each animal (snowflakes and a glacier for the penguin, bamboo for the panda…).
- Four corner tags hold the words: English top-left, Korean top-right,
  Japanese bottom-left, Hanja/Chinese bottom-right. Each tag has a small gray
  header (ENGLISH / KOREAN / JAPANESE / HANJA/CHINESE) and the word in outline
  lettering (white fill, black 2.5 px edge).
- Page number centered at the foot.
- Fonts: Fredoka (Latin), Noto Sans KR, Noto Sans JP, Noto Sans TC.

The reusable Moda markup is in [templates/page.moda.xml](templates/page.moda.xml).

## Art direction

See [docs/art-direction.md](docs/art-direction.md): the reference style, the
generation prompt skeleton, and the rules (no sea animals in the Animals books,
every shape left white inside, no solid black fills, no text in the art).

## Repository map

```
books/<book-slug>/README.md      links, status, decisions for that book
books/<book-slug>/pages.csv      page manifest: order, animal, four words, trinkets
docs/series-plan.md              the series and the scope of each book
docs/art-direction.md            style, prompts, do/don't rules
docs/kdp-checklist.md            what KDP needs before upload
templates/page.moda.xml          the page layout markup (Moda)
templates/page.svg               the same layout for Inkscape
templates/cover.svg              KDP full-wrap cover template (34 pages, white paper)
docs/inkscape-workflow.md        vectorize the art, lay out, export print PDF
tools/render_page.py             local HTML→PDF proof renderer (Playwright)
art/vault.tar.age                the artwork, encrypted (age); raw files never committed
tools/art_vault.sh               lock / unlock / list the art vault
docs/art-vault.md                how the vault works and what goes in it
docs/fonts.md                    every font in use, its license, and OFL swaps
```
