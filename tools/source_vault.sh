#!/usr/bin/env bash
# source_vault.sh — encrypt ONE large working file (e.g. the Inkscape SVG) for this PUBLIC repo.
#
# Kept apart from art/vault.tar.age so locking it never needs the main vault opened.
# The file is xz-compressed, then encrypted with an age passphrase, into
# art/source/<name>.xz.age. Only that ciphertext is ever committed.
#
#   tools/source_vault.sh lock   ~/Documents/marinelife.svg      -> art/source/marinelife.svg.xz.age
#   tools/source_vault.sh unlock art/source/marinelife.svg.xz.age [out-dir]   (default ~/Documents/vault-restore)
#
# age asks for the passphrase (twice when locking). Use the same one as the art vault
# and keep it in a password manager. It is never stored in the repo.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LIMIT=$((95 * 1024 * 1024))   # GitHub refuses files over 100 MB

command -v age >/dev/null || { echo "age is not installed (brew install age)" >&2; exit 1; }

case "${1:-}" in
  lock)
    src="${2:?usage: source_vault.sh lock <file>}"
    [[ -f "$src" ]] || { echo "no such file: $src" >&2; exit 1; }
    mkdir -p "$ROOT/art/source"
    out="$ROOT/art/source/$(basename "$src").xz.age"
    tmp="$(mktemp)"; trap 'rm -f "$tmp"' EXIT
    echo "compressing $(basename "$src") ..."
    xz -T0 -6 -c "$src" > "$tmp"
    age -p -o "$out.new" "$tmp"
    size=$(wc -c < "$out.new" | tr -d ' ')
    if (( size > LIMIT )); then
      rm -f "$out.new"; echo "too big for GitHub after compression ($size bytes); not saved" >&2; exit 1
    fi
    mv "$out.new" "$out"
    echo "locked -> ${out#$ROOT/} ($(du -h "$out" | cut -f1))"
    ;;
  unlock)
    enc="${2:?usage: source_vault.sh unlock <file.xz.age> [out-dir]}"
    dest="${3:-$HOME/Documents/vault-restore}"
    mkdir -p "$dest"
    name="$(basename "$enc" .xz.age)"
    [[ -e "$dest/$name" ]] && { echo "refusing to overwrite $dest/$name" >&2; exit 1; }
    age -d "$enc" | xz -d > "$dest/$name"
    echo "restored -> $dest/$name"
    ;;
  *) sed -n 2,13p "$0"; exit 1 ;;
esac
