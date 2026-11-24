#!/usr/bin/env python3
"""Dump X682C device-unique partitions after MTK-bypass protection is disabled.

The phone must already be in BROM with protection disabled, e.g. after:
    cd tools/bypass_utility && ../mtkclient/.venv/bin/python main.py

Run:
    tools/mtkclient/.venv/bin/python scripts/dump-nvram.py
"""
import hashlib
import logging
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools", "mtkclient"))

from mtkclient.config.mtk_config import MtkConfig  # noqa: E402
from mtkclient.Library.mtk_class import Mtk  # noqa: E402
from mtkclient.Library.DA.mtk_da_handler import DaHandler  # noqa: E402
from mtkclient.Library.Partitions.gpt import GptSettings  # noqa: E402

PRELOADER = os.path.join(
    ROOT, "firmware", "V366",
    "X682C-H694CD-Q-GL-220729V366(MobiFirmware.com)",
    "preloader_x682c_h694.bin",
)

TARGETS = {
    "proinfo", "nvram", "nvdata", "nvcfg", "persist", "protect1", "protect2",
    "seccfg", "frp", "misc", "boot", "recovery", "dtbo", "lk", "lk2",
    "boot_para", "expdb", "flashinfo", "metadata", "para", "md1img", "md_udc",
    "logo", "tkv", "tranfs",
}

outdir = os.path.join(ROOT, "backup", "mtk-bypass")
os.makedirs(outdir, exist_ok=True)

config = MtkConfig(loglevel=logging.INFO, gui=None, guiprogress=None)
config.gpt_settings = GptSettings(0, 0, 0)
mtk = Mtk(config=config, loglevel=logging.INFO)

# The bypass tool resets USB when it exits. Give the BROM time to enumerate,
# then retry one clean connection. No other mtkclient command may run first.
connected = False
for attempt in range(1, 11):
    print(f"connect attempt {attempt}")
    if mtk.preloader.init():
        connected = True
        break
    try:
        mtk.port.close()
    except Exception:
        pass
    time.sleep(3)
    mtk = Mtk(config=config, loglevel=logging.INFO)

if not connected:
    sys.exit("Could not connect to BROM/preloader")

mtk.preloader.get_target_config()
print("target_config:", config.target_config)

with open(PRELOADER, "rb") as fh:
    preloader = fh.read()
config.preloader = preloader
mtk.daloader.patch = True

handler = DaHandler(mtk, logging.INFO)
mtk = handler.configure_da(mtk)
if mtk is None:
    sys.exit("DA configuration failed")

data, gpt = mtk.daloader.get_gpt(parttype="user")
if gpt is None:
    sys.exit("Could not read GPT")

found = {p.name for p in gpt.partentries}
missing = TARGETS - found
if missing:
    print("missing partitions:", ", ".join(sorted(missing)))

sums = []
for part in gpt.partentries:
    if part.name not in TARGETS:
        continue
    path = os.path.join(outdir, part.name + ".bin")
    print(f"reading {part.name} ({part.sectors * 0x200} bytes)")
    mtk.daloader.readflash(part.sector * 0x200, part.sectors * 0x200, path,
                           parttype="user", display=True)
    if os.path.exists(path):
        h = hashlib.sha256(open(path, "rb").read()).hexdigest()
        sums.append(f"{h}  {part.name}.bin")

with open(os.path.join(outdir, "SHA256SUMS.txt"), "w") as fh:
    fh.write("\n".join(sums) + "\n")
print("done:", outdir)
