#!/usr/bin/env bash
# Build AGENTS.md files from a stack manifest.
#
# Usage: scripts/compose.sh <manifest> <out-dir>
#
# Manifest lines:   <output-path>: <item> <item> ...
#   item = a module id under templates/ (e.g. base, languages/go)
#        = or a path ending in .md, relative to the manifest's directory
# Blank lines and lines starting with # are ignored.
# Any output named *AGENTS.md over AGENTS_MAX_LINES (default 200) triggers a warning.
set -euo pipefail

if [ "$#" -ne 2 ]; then
  echo "usage: $0 <manifest> <out-dir>" >&2
  exit 2
fi

manifest=$1
out=$2
root=$(cd "$(dirname "$0")/.." && pwd)
mdir=$(cd "$(dirname "$manifest")" && pwd)

while IFS= read -r line || [ -n "$line" ]; do
  case "$line" in ''|'#'*) continue ;; esac
  path=${line%%:*}
  items=${line#*:}
  dest="$out/$path"
  mkdir -p "$(dirname "$dest")"
  : > "$dest"
  first=1
  for item in $items; do
    case "$item" in
      *.md) src="$mdir/$item" ;;
      *)    src="$root/templates/$item/AGENTS.md" ;;
    esac
    if [ ! -f "$src" ]; then
      echo "error: missing module '$item' (looked for $src)" >&2
      exit 1
    fi
    [ "$first" -eq 1 ] || printf '\n' >> "$dest"
    cat "$src" >> "$dest"
    first=0
  done
  lines=$(wc -l < "$dest" | tr -d ' ')
  case "$path" in
    *AGENTS.md)
      if [ "$lines" -gt "${AGENTS_MAX_LINES:-200}" ]; then
        echo "warning: $dest is $lines lines (budget ${AGENTS_MAX_LINES:-200}); move detail into docs/agent-rules/" >&2
      fi ;;
  esac
  echo "wrote $dest ($lines lines)"
done < "$manifest"
