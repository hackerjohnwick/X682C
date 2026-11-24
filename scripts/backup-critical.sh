#!/bin/sh
# Dump device-unique Infinix X682C partitions in ONE BROM session.
#
# Requires: phone powered off, USB cable, udev rules installed (see README.md).
# Usage: ./backup-critical.sh
# Output: backup/mtk-YYYYmmdd-HHMM/
set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PY="$ROOT/tools/mtkclient/.venv/bin/python"
MTK="$ROOT/tools/mtkclient/mtk.py"
OUT="$ROOT/backup/mtk-$(date +%Y%m%d-%H%M)"
mkdir -p "$OUT"

echo "== Save GPT =="
"$PY" "$MTK" gpt "$OUT" || true

echo "== Dump partitions (connect phone in BROM mode now) =="
PARTS="proinfo,nvram,nvdata,nvcfg,persist,protect1,protect2,seccfg,frp,misc,boot,recovery,dtbo,lk,lk2,boot_para,expdb,flashinfo,metadata,para,md1img,md_udc,logo,tkv,tranfs"
FILES="proinfo.bin,nvram.bin,nvdata.bin,nvcfg.bin,persist.bin,protect1.bin,protect2.bin,seccfg.bin,frp.bin,misc.bin,boot.bin,recovery.bin,dtbo.bin,lk.bin,lk2.bin,boot_para.bin,expdb.bin,flashinfo.bin,metadata.bin,para.bin,md1img.bin,md_udc.bin,logo.bin,tkv.bin,tranfs.bin"

cd "$OUT"
"$PY" "$MTK" r "$PARTS" "$FILES"

echo "== Done: $OUT =="
ls -lh "$OUT"
sha256sum "$OUT"/*.bin > "$OUT"/SHA256SUMS.txt
echo "Checksums: $OUT/SHA256SUMS.txt"
