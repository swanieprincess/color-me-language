#!/usr/bin/env bash
# art_vault.sh — keep the artwork in this PUBLIC repo without exposing it.
#
# The raw files live in art/raw/ (git-ignored). `lock` packs that folder into
# ONE encrypted file, art/vault.tar.age, which is what gets committed. Nobody
# without the passphrase can open it; GitHub only ever sees ciphertext.
#
#   tools/art_vault.sh lock      art/raw/**  ->  art/vault.tar.age
#   tools/art_vault.sh unlock    art/vault.tar.age  ->  art/raw/**
#   tools/art_vault.sh list      show what is inside the vault (asks for the passphrase)
#
# Needs `age` (https://age-encryption.org): brew install age  |  apt install age
# The passphrase is NEVER stored in the repo. Set ART_VAULT_PASSPHRASE in the
# environment to run non-interactively, otherwise age prompts for it.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RAW="$ROOT/art/raw"
VAULT="$ROOT/art/vault.tar.age"

need_age() {
  command -v age >/dev/null 2>&1 || { echo "age is not installed (brew install age)" >&2; exit 1; }
}

case "${1:-}" in
  lock)
    need_age
    [[ -d "$RAW" ]] || { echo "nothing to lock: $RAW does not exist" >&2; exit 1; }
    count=$(find "$RAW" -type f | wc -l | tr -d ' ')
    [[ "$count" -gt 0 ]] || { echo "nothing to lock: $RAW is empty" >&2; exit 1; }
    tmp="$(mktemp)"
    tar -C "$ROOT/art" -cf "$tmp" raw
    if [[ -n "${ART_VAULT_PASSPHRASE:-}" ]]; then
      python3 - "$tmp" "$VAULT" <<'PY'
import os, subprocess, sys, pty
src, dst = sys.argv[1], sys.argv[2]
pw = os.environ["ART_VAULT_PASSPHRASE"]
pid, fd = pty.fork()
if pid == 0:
    os.execvp("age", ["age", "-p", "-o", dst, src])
buf = b""
sent = 0
while True:
    try:
        chunk = os.read(fd, 1024)
    except OSError:
        break
    if not chunk:
        break
    buf += chunk
    if b"passphrase" in buf.lower() and sent < 2 and buf.rstrip().endswith(b":"):
        os.write(fd, pw.encode() + b"\n"); sent += 1; buf = b""
_, status = os.waitpid(pid, 0)
sys.exit(os.WEXITSTATUS(status))
PY
    else
      age -p -o "$VAULT" "$tmp"
    fi
    rm -f "$tmp"
    echo "locked $count file(s) from art/raw into art/vault.tar.age ($(du -h "$VAULT" | cut -f1))"
    ;;
  unlock)
    need_age
    [[ -f "$VAULT" ]] || { echo "no vault at $VAULT" >&2; exit 1; }
    tmp="$(mktemp)"
    if [[ -n "${ART_VAULT_PASSPHRASE:-}" ]]; then
      python3 - "$VAULT" "$tmp" <<'PY'
import os, sys, pty
src, dst = sys.argv[1], sys.argv[2]
pw = os.environ["ART_VAULT_PASSPHRASE"]
pid, fd = pty.fork()
if pid == 0:
    os.execvp("age", ["age", "-d", "-o", dst, src])
buf = b""; sent = 0
while True:
    try:
        chunk = os.read(fd, 1024)
    except OSError:
        break
    if not chunk:
        break
    buf += chunk
    if b"passphrase" in buf.lower() and sent < 1 and buf.rstrip().endswith(b":"):
        os.write(fd, pw.encode() + b"\n"); sent += 1; buf = b""
_, status = os.waitpid(pid, 0)
sys.exit(os.WEXITSTATUS(status))
PY
    else
      age -d -o "$tmp" "$VAULT"
    fi
    mkdir -p "$ROOT/art"
    tar -C "$ROOT/art" -xf "$tmp"
    rm -f "$tmp"
    echo "unlocked into art/raw ($(find "$RAW" -type f | wc -l | tr -d ' ') files)"
    ;;
  list)
    need_age
    [[ -f "$VAULT" ]] || { echo "no vault at $VAULT" >&2; exit 1; }
    age -d "$VAULT" | tar -tf -
    ;;
  *)
    sed -n '2,15p' "$0"
    exit 1
    ;;
esac
