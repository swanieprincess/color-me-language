# The art vault

This repository is public, but the artwork is not. The finished pages, cover
art and any working files are committed **encrypted only**, as a single file:

```
art/vault.tar.age      committed  — the encrypted bundle (age, passphrase)
art/raw/               ignored    — the real files, only on your own machine
```

Anyone can clone the repo and see that the file exists. Without the passphrase
it is random bytes. The passphrase is kept in a password manager, never in the
repo, never in an issue or PR.

## Daily use

```bash
brew install age                      # once, on the Mac

tools/art_vault.sh unlock             # vault -> art/raw/   (asks for the passphrase)
# ... add or change files in art/raw/ ...
tools/art_vault.sh lock               # art/raw/ -> vault   (asks twice)
git add art/vault.tar.age && git commit -m "Update art vault"
```

`tools/art_vault.sh list` prints what is inside without extracting.

## What goes in

- `art/raw/pages/NN-animal.png` — the flattened page exports (380 dpi).
- `art/raw/cover/` — cover art pieces and the assembled cover PDF.
- `art/raw/source/` — anything else worth keeping: traced SVGs, Inkscape files.

The `.gitignore` refuses `png`, `jpg`, `jpeg`, `pdf`, `psd`, `tif`, `webp`,
`ai` and `svg` under `art/`, so a raw file cannot be committed by accident.
Everything outside `art/` (templates, docs, the manifest) stays public.

## If the passphrase is lost

The vault cannot be opened. Keep the raw files backed up somewhere private as
well (Drive, an external disk); the repo copy is a convenience, not the only
copy.

## Rotating the passphrase

`unlock` with the old one, `lock` with the new one, commit. Old commits still
hold the old ciphertext, which only the old passphrase opens, so a leaked old
passphrase exposes only what was in the vault at that time.
