# HANDOFF — The Learning Dojo: Marine Life, Volume 2

Standing handoff between sessions. Read it before starting work and keep it
current. It lists only open work and the state it is in.

**Public repo.** Never commit the art-vault passphrase, credentials, signed
download links or session links. Artwork goes only into the encrypted vault
(`art/vault.tar.age`, see `docs/art-vault.md`). Author credit is **Swan Moon**.

Last updated: 2026-11-16.

## State right now

| Item | State |
|---|---|
| 52 animal pages (EN / KO / JA / Hanja) | Drawn and audited page by page. AI fixes done. |
| "Did you know?" intro pages i–vi | Text and 52 cut-out icons placed, squared and checked. |
| Grouper (13) and conch (31) swap | Done on canvas and in repo files. |
| Review PDF | Exported from Moda 2026-10-29 and given to Swan as a signed link (not stored here). |
| Inkscape vector cleanup | **In progress (Swan).** Pages traced to paths in `~/Documents/marinelife.svg` on her Mac. Her decorations and removals are final: never undo or "correct" them. |
| Inkscape file backup | `tools/source_vault.sh` encrypts it to `art/source/marinelife.svg.xz.age` (xz + age passphrase). Swan runs the lock on her Mac and pushes; the clone is at `~/claude-work/color-me-language`. |
| English words in Sandoll | **Added 2026-11-11.** New layer "English words" with 52 text objects, one per animal page (not the intro pages). Swan is deleting the old traced English words underneath herself. |
| Cover front art | **Waiting on Swan** (she draws it). Cover template: `art/raw/cover/marine-life-cover.svg` in the vault. |
| Korean check | **Waiting on a native speaker:** 다금바리 (13) and 소라고둥 (31). See `docs/korean-review-sheet.md`. |
| ⚑ facts | Double-check every ⚑ fact in `books/marine-life/did-you-know.md` before print. |
| KDP print PDF | Not built. Do this after the cleaned pages come back. |

Branch `claude/initial-structure`, PR #1 open (draft). Everything is committed and pushed.

## Next step: doubled-word check

When Swan says "done" (file saved, Inkscape quit):

1. Confirm Inkscape is closed (`pgrep -l inkscape`). Never touch the SVG while it is open.
2. Render Inkscape pages 8–59 (animals 1–52) read-only:
   `inkscape marinelife.svg --export-type=png --export-page=N --export-dpi=96 --export-filename=…`
   (about 5 s a page; run in the background and poll).
3. Crop the English tag (x 36–336, y 36–148 on the 1080 px page) into contact sheets.
4. Send Swan the list of pages that still show a doubled or leftover old word. She fixes them; don't edit the file.

## Next steps when Swan sends the cleaned pages

1. Put the cleaned files under `art/raw/` (never in `books/` or anywhere public).
2. Lock the vault: `ART_VAULT_PASSPHRASE=… tools/art_vault.sh lock`, commit only `art/vault.tar.age`.
3. Build the KDP print PDF against `docs/kdp-checklist.md` (trim, bleed, margins, page count).
4. Move finished items from this file into the book's README or a changelog.

## Where the working files are

- **Moda canvas** `cvs_5Z4APA5SZV9W7V8AQQ0CHQQAB5` holds every page and icon.
  - Intro pages: i `page-1793245874829-42600992`, ii `page-1793252126601-670954140`,
    iii `page-1793252126603-593300770`, iv `page-1793252126603-687069604`,
    v `page-1793252126604-8274820`, vi `page-1793252126605-462377292`.
  - Art nodes: 13 grouper `rect-1793099430933-178223506`, 19 coral `rect-1793101042295-827638144`,
    24 squid `rect-1793108099126-716521488`, 26 jellyfish `rect-1793108124468-434469223`,
    31 conch `rect-1793168382678-28056782`, 34 shrimp `rect-1793168578060-666589202`,
    42 humpback `rect-1793225058022-632036312`.
  - Replaced icons: 13 `rectangle-1793282183027-805596409`, 31 `rectangle-1793282183113-588790367`,
    24 `rectangle-1793302995652-555406303`, 19 `rectangle-1793303179899-33583982`,
    34 `rectangle-1793303179963-9077491`, 9 hammerhead `rectangle-1793255921592-957010759`.
- **Repo:** `books/marine-life/pages.csv` (names), `books/marine-life/did-you-know.md` (facts),
  `docs/marine-life-lineup.md`, `docs/korean-review-sheet.md`, `docs/marine-life-inkscape-cleanup.md`.

## Inkscape file facts (marinelife.svg)

- Units mm, viewBox 0 0 210 297. Inkscape page 1 is an A4 blank; pages 2–59 are 285.75 mm squares.
- Layers "1"–"6" are intro pages i–vi; layers "7"–"58" are animals 1–52 in `pages.csv` order.
  Each uses `matrix(0.26458333,0,0,0.26458334,220,0)`; page k's content sits at px x = 1100·(k−1).
- The English layer (`id="layer-english-words"`) is the last layer in the file; text ids `english-word-1`…`-52`.
  Centre x 186, font size 60 px (smaller for long names; Hammerhead Shark, Long-arm Octopus and
  Humpback Whale are 36 px on two lines).
- Backup from before the English layer: `~/Documents/marinelife-backup-2026-11-11-before-english-font.svg`.
- Many layers still hold the embedded page picture under the traced paths (55 images). The old
  English words are baked into those too: hide or delete the pictures before export.
- Open decision: page 1 is A4 but `docs/kdp-checklist.md` says 8.5×11 trim.
- Working scripts on the Mac: `~/claude-work/marine/` (`add_english.py`, `sheet.py`, venv with pillow).

## Fonts (Vol 2)

- English word: **Sandoll Samliphopangche Outline** (산돌 삼립호빵체). SIL OFL 1.1 per Sandoll's page;
  free to use in a sold book, but the font file itself can't be sold. Latin and partial Hangul only,
  no Japanese or Chinese. Installed on the Mac with the Basic weight.
- Also installed: Noto Sans KR / JP / TC (variable) and Fredoka.
- To do (offered, not requested): add these to `docs/fonts.md` and save Sandoll's licence PDF.

## What was learned (do not re-learn)

- Page art: aspect 3:4, model nano-banana-lite, reference image = the Vol 1 turtle. Icons: 1:1 with AI cutout.
- After duplicating an icon, square it: `x: 62`, width = height = slot size, fit `contain`.
- Moda image *edits* are unreliable: they can do nothing (humpback), flip the image (jellyfish)
  or leave junk (squid). When two edits fail, regenerate the page instead.
- An edit to fix eyes on one animal can add eyes elsewhere: check every animal on the page (shrimp).
- `NO_RENDER_IMPACT` on an update means the canvas is already in that state.
- The Moda MCP disconnects often; reload its tools and carry on.
- The proxy blocks downloads from Moda's CDN (403), so PDFs go to Swan as a signed link.
- Remote Mac access (Desktop Commander): start each command with `cd ~`; zsh aborts on an unmatched
  glob; no Accessibility permission, so I can't click, save or quit apps. Swan does that.
- sandollcloud.com is unreachable from the cloud session; fetch it via the Mac.
- Swan knows Inkscape well: don't explain how to use it.

## Risk to act on

The art-vault passphrase existed only in this session's scratchpad, which is deleted when the
session ends. **Swan: keep your own copy in a password manager.** Without it the vault cannot be opened.
