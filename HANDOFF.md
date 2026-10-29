# HANDOFF — The Learning Dojo: Marine Life, Volume 2

Standing handoff between sessions. Read it before starting work and keep it
current. It lists only open work and the state it is in.

**Public repo.** Never commit the art-vault passphrase, credentials, signed
download links or session links. Artwork goes only into the encrypted vault
(`art/vault.tar.age`, see `docs/art-vault.md`). Author credit is **Swan Moon**.

Last updated: 2026-10-29.

## State right now

| Item | State |
|---|---|
| 52 animal pages (EN / KO / JA / Hanja) | Drawn and audited page by page. AI fixes done. |
| "Did you know?" intro pages i–vi | Text and 52 cut-out icons placed, squared and checked. |
| Grouper (13) and conch (31) swap | Done on canvas and in repo files. |
| Review PDF | Exported from Moda 2026-10-29 and given to Swan as a signed link (not stored here). |
| Inkscape cleanup | **Waiting on Swan.** List: `docs/marine-life-inkscape-cleanup.md`. |
| Cover front art | **Waiting on Swan** (she draws it). Cover template: `art/raw/cover/marine-life-cover.svg` in the vault. |
| Korean check | **Waiting on a native speaker:** 다금바리 (13) and 소라고둥 (31). See `docs/korean-review-sheet.md`. |
| ⚑ facts | Double-check every ⚑ fact in `books/marine-life/did-you-know.md` before print. |
| KDP print PDF | Not built. Do this after the cleaned pages come back. |

Branch `claude/initial-structure`, PR #1 open (draft). Everything is committed and pushed.

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

## What was learned (do not re-learn)

- Page art: aspect 3:4, model nano-banana-lite, reference image = the Vol 1 turtle. Icons: 1:1 with AI cutout.
- After duplicating an icon, square it: `x: 62`, width = height = slot size, fit `contain`.
- Moda image *edits* are unreliable: they can do nothing (humpback), flip the image (jellyfish)
  or leave junk (squid). When two edits fail, regenerate the page instead.
- An edit to fix eyes on one animal can add eyes elsewhere: check every animal on the page (shrimp).
- `NO_RENDER_IMPACT` on an update means the canvas is already in that state.
- The Moda MCP disconnects often; reload its tools and carry on.
- The proxy blocks downloads from Moda's CDN (403), so PDFs go to Swan as a signed link.

## Risk to act on

The art-vault passphrase existed only in this session's scratchpad, which is deleted when the
session ends. **Swan: keep your own copy in a password manager.** Without it the vault cannot be opened.
