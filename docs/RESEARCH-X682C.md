# X682C tutorials, videos, forums — research notes

Collected 2026-11-24. Third-party content; firmware itself was verified by hash.

## Exact-model YouTube

| Video | What it shows |
|---|---|
| `UYkfrpP-_s8` — Infinix Hot 10 X682C Full Flash Stock Firmware OS Repair Guide | Full flash, dead/software recovery. GSM Phone Repair. |
| `5i8vRLnbwa8` — How To Full Flash Infinix Hot 10 X682C Using Free Tool | Full flash using a free tool. |
| `UaXRmuQyAoc` — Infinix Hot 10 X682B/X682C Firmware Flash File without password | Free firmware route for both variants. |
| `c9dGjuLEzL0` — How To Root Infinix Hot 10 X682C / Magisk | Root via Magisk, Urdu/Hindi. |
| `UTHKVUsgTXM` — Infinix Hot 10 X682C IMEI Repair | Null IMEI, crypt IMEI after wrong flash, network fix. |
| `tlDJK8jpTQ8` — Infinix Hot 10 (X682C) Read Full Flash / Dead Boot Fix By CM2 | Full-flash readback with CM2. |
| `ShY1kk8S0R8` — How To Flash Infinix Hot 10 X682C Dead Boot Repair Free File | Dead-boot flash. |
| `z-OjFtAzWqo` — Flash Infinix/Tecno Latest Security Without Test Point, BROM + UMT + SPFT | Not X682C-specific; same MTK/Infinix method for secure units. |

## Forums / blogs

- Hovatek `thread-35620` — X682B/X682C stock ROM + individual component files
  (boot, recovery, lk, scatter, preloader, full ROM).
- Hovatek `thread-39955` — “flash Infinix Hot 10 X682C”.
- Hovatek `thread-48548` — X682C stuck on logo after OTA; staff advice: back up
  firmware as-is before flashing, then use the correct X682B **or** X682C package.
- Hovatek `thread-46342` — generic “backup your firmware as is” guide.
- Hovatek `thread-46323` — WWR + SP Flash Tool readback/backup guide.
- XDA `t/4252713` — X682C TWRP/root; notes bootloop from patched boot.
- XDA tag `x682c` — GSI/custom ROM threads for Hot 10.
- Magisk issue `topjohnwu/Magisk#4112` — X682C bootloop from patched
  boot/recovery on Android 10.
- `firmware4mobile.com/2025/02/infinix-hot-10-x682c-stock-rom-flash.html`
- `officialroms.com/infinix-hot-10-x682c-flash-file/`
- `androidwintool.com/supported-models/infinix/infinix-hot-10-x682c` — lists six
  builds including `220729V366`, META-mode IMEI operation.
- 4PDA Hot 10 Play thread — uses `MTK_Bypass_Updated` + `brom.bat` with both
  volume keys; **different model**, method only.

## Secure-BROM / auth route

The exact model is listed as “(Auth)” by service tools:

- TFM Tool Pro MTK, Hydra Tool, EFT Pro, Tr Tool (HalabTech), Griffin-Unlocker
  (explicit X682C NVRAM backup/restore), Infinity CM2MT2, UnlockTool.
- These carry an Infinix `auth_sv5.auth` or call an auth server. That is how
  shops read NVRAM and repair IMEI on this security level.

Open-source alternative:

- XDA `t/4232377` — “MediaTek / MTK Auth Bypass (SLA/DAA)”.
- GitHub `MTK-bypass/bypass_utility` — supports **mt6768**. It disables
  SLA/DAA, then SP Flash Tool can read/write without an auth file.
- On Linux the README requires FireISO or a patched kamakiri kernel.
- This unit reports `HW code 0x707`, `var_1 0x25`; the utility's config has
  exactly `0x707` → `mt6768_payload.bin`, `var_1 0x25`.

Local copy, tested 2026-11-24:

```
tools/bypass_utility/          # main.py + default_config.json5 + payloads
tools/exploits_collection/     # upstream payloads
```

It ran from the normal Ubuntu kernel (no FireISO required), crashed preloader to
BROM and printed `Protection disabled`. `gettargetconfig` then reported all
security flags off (`target config 0x0`). The remaining step is a fresh BROM
cycle with `scripts/dump-nvram.py` for the actual partition dump.

## What this confirms

1. Full stock restore on X682C is well documented and the exact V366 package is
   now saved and hash-verified.
2. Shops do not magically avoid auth: they use paid auth tools, a signed auth
   file, or direct eMMC/ISP work.
3. The open-source bypass is the only free route to a full NVRAM dump on this
   unit; otherwise a service tool or ISP is required.
4. Root/TWRP threads confirm the known X682C bootloop trap with patched
   boot/recovery images — keep the stock `boot.img` and exact build.
