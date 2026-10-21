#!/bin/sh
# Экспорт всех схем draw.io из images/src/*.drawio в images/<name>.png.
# Масштаб 3, поле 10 единиц; 1 единица draw.io = 0,254 мм на печати.
set -e
cd "$(dirname "$0")"
DRAWIO="${DRAWIO:-/Applications/draw.io.app/Contents/MacOS/draw.io}"
for f in *.drawio; do
  n="${f%.drawio}"
  "$DRAWIO" -x -f png -s 3 -b 10 -o "../$n.png" "$f"
done
