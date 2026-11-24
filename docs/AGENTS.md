# AGENTS.md — Infinix X682C recovery kit

Context for any future agent in `/home/arnav/Infinix`.
Read this, then `docs/RECOVERY-READINESS.md` and `docs/BROM-NOTES.md`.

## TL;DR

Recovery kit for **one phone**:

- Infinix HOT 10, model **X682C**, MT6768, Android 10
- Exact build `X682C-H694CD-Q-GL-220729V366`
- Current state: **booted, stock, verified boot green**
- Exact full ROM, NVRAM/IMEI backup, auth bypass, verified DA read/write

A **software brick is recoverable** if the phone still enumerates as
preloader/BROM. Dead eMMC/SoC or no USB needs test point/ISP or hardware repair.

SP Flash Tool actual flash is **not** physically tested. mtkclient DA read/write
**is** tested.

## Device

| Item | Value |
|---|---|
| Model | Infinix HOT 10 X682C / X682C-GL |
| SoC | MediaTek MT6768 |
| RAM / storage | 6 GB / 128 GB |
| Display | 720 x 1640 |
| Android | 10, SDK 29 |
| Build | X682C-H694CD-Q-GL-220729V366 |
| Patch | 2022-07-05 |
| Serial | REDACTED (private) |
| IMEI | private, `docs/device-info/identifiers.txt` |
| Partitions | non-A/B, dynamic super, eMMC |
| Bootloader | locked, verified boot green |
| BROM | SBC+SDA; open-source bypass works |

Raw: `docs/DEVICE.md`, `docs/device-info/`.

## Layout

```
firmware/
  X682C-...V366.zip              exact full ROM — primary
  V366/.../                      extracted scatter, super, boot, recovery
  X682C-...V360.zip              previous build — fallback
  OTA-V360-to-V366...zip         official OTA — fallback
docs/
  RECOVERY-READINESS.md          verified vs unverified
  BROM-NOTES.md                  working BROM procedure + force-off
  DEVICE.md, device-info/        device dump, IMEI, bugreport
  V366-info.md, V360-info.md     ROM evidence
  EXACT-V366-RESTORE.md          fallback restore
  BACKUP-MANIFEST.md             NVRAM/IMEI backup contents
  RESEARCH-X682C.md              videos/forums/auth methods
  PLAN-lineageos.md              LineageOS + OrangeFox + Magisk plan
  ota-metadata/                  OTA metadata + partition list
  AGENTS.md                      this playbook
  LEARN.md                       full 20-part course
  PROJECT-STRUCTURE.md           annotated inventory
scripts/
  dump-nvram.py                  post-bypass 25-partition dump (tested)
  verify-write.py                post-bypass write/read verify (tested)
  backup-critical.sh             pre-bypass script (blocked, reference)
backup/
  mtk-bypass/                    25 partitions, SHA256SUMS
  X682C-unique-backup-...tar.zst portable archive + .sha256
tools/
  SP_Flash_Tool_v5.2228_Linux/   SP Flash Tool
  mtkclient/                     mtkclient + .venv
  bypass_utility/                SLA/DAA bypass for mt6768
  exploits_collection/           payloads
  udev/                          Android/MTK udev rules
  x682c-twrp.img                 TWRP reference
README.md                        GitHub-facing overview (only root doc)
AGENTS.md -> docs/AGENTS.md      root symlink for agent tooling
agent.md  -> docs/AGENTS.md      lowercase root symlink
SHA256SUMS.txt                   top-level artifact hashes
```

## Verified

- V366 zip SHA256 `ce62372d4e3f4cce49b9a929c0b6b5ead0eb18f910a0071918edb891d92c2603`
- 25 partition dumps: `sha256sum -c backup/mtk-bypass/SHA256SUMS.txt`
- `boot.bin`/`recovery.bin` match exact V366 images
- `nvram.bin`/`nvdata.bin` contain `NVD_IMEI`; `proinfo.bin` has serial
- Bypass: `Protection disabled`, target config `0x0`
- Write: exact `logo.bin` written + read back, identical SHA256
- Root: `sha256sum -c SHA256SUMS.txt`

## Rules

1. **Never Format All** — wipes NVRAM/IMEI.
2. **Never flash X682B firmware** — different model.
3. **Never flash a custom `logo.bin`.** A mtklogo repack caused boot loop +
   continuous vibration here; stock was restored.
4. Keep `backup/mtk-bypass/` private.
5. Do not relock bootloader with custom software.
6. Do not write sparse `super.img` with mtkclient raw write; use SPFT for super.
7. BROM has a short window: run dump/write as the first command after bypass.
8. Force off: **Power + Volume Up**. Power alone 30 s did not work.
9. Enter preloader: phone off, hold **Volume Up + Volume Down**, plug USB.

## Entry

- Android: `adb devices`.
- Preloader: `adb reboot edl` → `0e8d:2000` (few seconds).
- BROM: `0e8d:0003` (bypass/crash).
- No USB: test point/ISP or battery disconnect.

## Recovery A — ADB works

1. Back up user data.
2. Restore exact build via SPFT (B) or mtkclient (C).
3. Verify:
   ```
   adb shell getprop ro.build.display.id
   # X682C-H694CD-Q-GL-220729V366
   adb shell getprop ro.boot.verifiedbootstate
   # green
   ```

## Recovery B — SP Flash Tool (primary)

Tool:
`tools/SP_Flash_Tool_v5.2228_Linux/SP_Flash_Tool_v5.2228_Linux/flash_tool.sh`

1. Charge; USB 2.0; good cable.
2. Download → Scatter-loading →
   `firmware/V366/X682C-H694CD-Q-GL-220729V366(MobiFirmware.com)/MT6768_Android_scatter.txt`
3. **Download Only**, preloader unticked first.
4. Download → connect powered-off phone (Vol Up+Down if needed).
5. Green circle = success; first boot slow.
6. Still bootlooping → **Firmware Upgrade**.
7. Preloader only from this exact package, only if no enumeration.

SPFT console did not detect BROM here; GUI untested. If SPFT refuses, use C.

## Recovery C — mtkclient (verified)

1. Force off: Power + Volume Up.
2. Preloader: hold Vol Up + Vol Down, plug USB (or `adb reboot edl`).
3. Bypass:
   ```sh
   cd /home/arnav/Infinix/tools/bypass_utility
   ../mtkclient/.venv/bin/python main.py
   ```
   Wait for `Protection disabled`.
4. Immediately run **one** client:
   - Backup:
     ```sh
     cd /home/arnav/Infinix
     tools/mtkclient/.venv/bin/python scripts/dump-nvram.py
     ```
   - Write: use `scripts/verify-write.py` as the tested connection template;
     change `PART` and `IMAGE` for another partition.
5. No extra mtkclient command first; it consumes the window.
6. Power off: Power + Volume Up.

Stock logo restore:
```sh
cd /home/arnav/Infinix
env -u LOGO_IMAGE tools/mtkclient/.venv/bin/python scripts/verify-write.py
```

Custom `logo` images are not recommended (boot-loop risk).

## Recovery D — IMEI/NVRAM lost

From `backup/mtk-bypass/`, after bypass + DA:

```
nvram.bin    -> nvram
nvdata.bin   -> nvdata
nvcfg.bin    -> nvcfg
persist.bin  -> persist
proinfo.bin  -> proinfo
protect1.bin -> protect1
protect2.bin -> protect2
```

Do not write `seccfg.bin`/`frp.bin` casually. Write one at a time, read back,
compare SHA256. Never restore another phone's NVRAM.

No USB/BROM → ISP shop must write these.

## Recovery E — hard brick / no USB

- Test point or eMMC ISP (Medusa, Easy JTAG, UFI Box).
- Battery disconnect, then Vol Up+Down while plugging.
- Exact ROM cannot rebuild IMEI; the NVRAM backup can, via ISP.
- Dead eMMC/SoC = hardware repair.

## Goal

**Software/firmware bricks on this X682C:** yes, with caveats.
**Hardware-dead:** no.

Self-contained only at `/home/arnav/Infinix` on Linux. If moved:

```sh
python3 -m venv tools/mtkclient/.venv
tools/mtkclient/.venv/bin/pip install pyusb pycryptodome pycryptodomex colorama pyserial keystone-engine capstone unicorn mfusepy json5
sudo cp tools/udev/*.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules && sudo udevadm trigger
```

SPFT bundles its own libs.

## Current state

Online via ADB, exact V366, verified boot green, stock splash, NVRAM backup done.
No flash write pending. User data untouched except logo writes.

## Health check

```sh
cd /home/arnav/Infinix
sha256sum -c SHA256SUMS.txt
cd backup/mtk-bypass && sha256sum -c SHA256SUMS.txt
adb devices -l
adb shell getprop ro.build.display.id
```
