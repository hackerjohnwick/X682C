#!/usr/bin/env python3
"""Safely verify the MTK DA write path on X682C.

Writes the exact V366 `logo.bin` back to the `logo` partition, reads it back,
and compares hashes. Read/write only; no reboot, no data partition.

Run after `bypass_utility` printed `Protection disabled`, as the first
mtkclient process. Same connection rules as dump-nvram.py.
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

PKG = os.path.join(ROOT, "firmware", "V366",
                   "X682C-H694CD-Q-GL-220729V366(MobiFirmware.com)")
PRELOADER = os.path.join(PKG, "preloader_x682c_h694.bin")
IMAGE = os.environ.get("LOGO_IMAGE", os.path.join(PKG, "logo.bin"))
PART = "logo"

config = MtkConfig(loglevel=logging.INFO, gui=None, guiprogress=None)
config.gpt_settings = GptSettings(0, 0, 0)
mtk = Mtk(config=config, loglevel=logging.INFO)

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
    sys.exit("Could not connect to BROM")

mtk.preloader.get_target_config()
with open(PRELOADER, "rb") as fh:
    config.preloader = fh.read()
mtk.daloader.patch = True

handler = DaHandler(mtk, logging.INFO)
mtk = handler.configure_da(mtk)
if mtk is None:
    sys.exit("DA configuration failed")

data, gpt = mtk.daloader.get_gpt(parttype="user")
part = next((p for p in gpt.partentries if p.name == PART), None)
if part is None:
    sys.exit("partition not found: " + PART)

with open(IMAGE, "rb") as fh:
    image = fh.read()
image_hash = hashlib.sha256(image).hexdigest()
addr = part.sector * 0x200
length = part.sectors * 0x200

print(f"writing {PART}: {len(image)} bytes from {IMAGE}")
if not mtk.daloader.writeflash(addr, len(image), IMAGE, parttype="user"):
    sys.exit("writeflash failed")

print("reading back")
after = mtk.daloader.readflash(addr, length, "", parttype="user", display=True)
after_hash = hashlib.sha256(after[:len(image)]).hexdigest()
print("image sha256:", image_hash)
print("read  sha256:", after_hash)
if after_hash != image_hash:
    sys.exit("MISMATCH")
print("WRITE VERIFIED")
