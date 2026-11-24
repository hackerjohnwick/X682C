# Infinix HOT 10 (X682C) — recovery kit

![Device](https://img.shields.io/badge/device-Infinix%20HOT%2010%20X682C-orange?style=flat-square)
![SoC](https://img.shields.io/badge/SoC-MediaTek%20MT6768-blue?style=flat-square)
![Android](https://img.shields.io/badge/Android-10%20%C2%B7%20SDK%2029-3ddc84?style=flat-square)
![Build](https://img.shields.io/badge/build-220729V366-lightgrey?style=flat-square)
![NVRAM](https://img.shields.io/badge/NVRAM%2FIMEI%20backup-verified-brightgreen?style=flat-square)
![BROM](https://img.shields.io/badge/BROM%20bypass-verified-green?style=flat-square)
![SPFT](https://img.shields.io/badge/SPFT%20flash-untested-yellow?style=flat-square)

Self-contained recovery kit for one **Infinix HOT 10 X682C** on exact firmware
`X682C-H694CD-Q-GL-220729V366`.

Built from a live ADB session. Exact factory ROM, device-unique partition
backup, secure-BROM bypass, and a verified read/write path are all saved here.

> **Scope:** recovers this phone from **software/firmware bricks** when it still
> enumerates as preloader/BROM. A dead eMMC/SoC or a phone with no USB port needs
> a test point/ISP or hardware repair. This is not a universal MTK recovery kit.

## Status

| Area | State |
|---|---|
| Exact V366 full ROM | ✅ saved, hash + fingerprints verified |
| NVRAM / IMEI / persist backup | ✅ 25 partitions, all hashes verified |
| Secure-BROM bypass (SBC+SDA) | ✅ `Protection disabled` |
| mtkclient DA read | ✅ 872 MB dump completed |
| mtkclient DA write | ✅ write + read-back hash identical |
| SP Flash Tool actual flash | ⚠️ not physically tested |
| Full `super` write / NVRAM restore | ⚠️ not executed (destructive) |
| Dead eMMC / no USB | ❌ ISP/test point only |

Full matrix: [`docs/RECOVERY-READINESS.md`](docs/RECOVERY-READINESS.md).
Annotated file inventory: [`docs/PROJECT-STRUCTURE.md`](docs/PROJECT-STRUCTURE.md).
Full course: [`docs/LEARN.md`](docs/LEARN.md).

## Device

| | |
|---|---|
| Marketing name | Infinix HOT 10 |
| Model / product | X682C / X682C-GL |
| SoC | MediaTek MT6768 |
| CPU | ARM64, 8 cores |
| RAM / storage | 6 GB / 128 GB |
| Display | 720 × 1640, 320 dpi |
| Android | 10 (SDK 29) |
| Build | `X682C-H694CD-Q-GL-220729V366` |
| Security patch | 2022-07-05 |
| Partitioning | non-A/B, dynamic `super`, eMMC |
| Bootloader | locked, verified boot green |
| BROM security | SBC+SDA, bypass works |

Raw device data: [`docs/DEVICE.md`](docs/DEVICE.md), [`docs/device-info/`](docs/device-info/).

## Layout

```text
firmware/
  X682C-H694CD-Q-GL-220729V366.zip     exact full factory ROM (primary)
  V366/                                 extracted: scatter, super, boot, recovery...
  X682C-H694CD-Q-GL-220510V360.zip      previous build (fallback)
  OTA-V360-to-V366-a6abd9a8.zip         official OTA (fallback)
docs/
  RECOVERY-READINESS.md                 verified vs untested
  BROM-NOTES.md                         working BROM procedure, force-off combo
  DEVICE.md, device-info/               live device dump, IMEI, bugreport
  V366-info.md, V360-info.md            ROM hashes/fingerprints
  EXACT-V366-RESTORE.md                 fallback restore steps
  BACKUP-MANIFEST.md                    NVRAM/IMEI backup contents
  RESEARCH-X682C.md                     videos, forums, auth methods
  PLAN-lineageos.md                     LineageOS + OrangeFox + Magisk plan
  AGENTS.md                             canonical agent playbook
  LEARN.md                              full 20-part course
  PROJECT-STRUCTURE.md                  annotated inventory
  ota-metadata/                         OTA metadata
scripts/
  dump-nvram.py                         post-bypass 25-partition dump
  verify-write.py                       post-bypass write/read verifier
  backup-critical.sh                    pre-bypass script (reference)
backup/
  mtk-bypass/                           25 partitions + SHA256SUMS
  X682C-unique-backup-2026-11-24.tar.zst
tools/
  SP_Flash_Tool_v5.2228_Linux/          MediaTek flash tool
  mtkclient/                            mtkclient + Python venv
  bypass_utility/                       SLA/DAA bypass (mt6768)
  exploits_collection/                  upstream payloads
  udev/                                 Android/MTK udev rules
  x682c-twrp.img                        TWRP reference
README.md                               this file (only root doc)
AGENTS.md -> docs/AGENTS.md             tooling symlink
agent.md  -> docs/AGENTS.md             lowercase tooling symlink
SHA256SUMS.txt                          top-level artifact hashes
```

All documentation lives in `docs/`. Root `AGENTS.md` and `agent.md` are symlinks
so agent tooling finds the playbook.

`.gitignore` excludes firmware ZIPs, the private NVRAM backup, the Python venv,
and device identifiers. Publish those through a private release/storage, not a
public git commit.

Not committed in this public repo: `firmware/`, `backup/`, `docs/device-info/`,
and the proprietary **SP Flash Tool** directory. Keep the first three private;
download SPFT from the source listed under [Sources](#sources).

## Documentation

| Document | What it covers |
|---|---|
| [`docs/LEARN.md`](docs/LEARN.md) | Full course: basics -> bootloader, recovery, ROMs, root, bootloops, bricks, causes, MTK internals, labs, glossary, quiz. |
| [`docs/AGENTS.md`](docs/AGENTS.md) | Operational playbook for future agents: exact commands, rules, recovery A–E. |
| [`docs/RECOVERY-READINESS.md`](docs/RECOVERY-READINESS.md) | Verified vs untested matrix and recovery limits. |
| [`docs/BROM-NOTES.md`](docs/BROM-NOTES.md) | Secure-BROM bypass, DA read/write evidence, force-off/entry combos. |
| [`docs/DEVICE.md`](docs/DEVICE.md) | Device identity, build, partition map, raw-data index. |
| [`docs/V366-info.md`](docs/V366-info.md) | Exact ROM hashes, fingerprints, package contents. |
| [`docs/V360-info.md`](docs/V360-info.md) | Fallback V360 evidence and OTA preconditions. |
| [`docs/EXACT-V366-RESTORE.md`](docs/EXACT-V366-RESTORE.md) | Fallback V360 + OTA restore. |
| [`docs/BACKUP-MANIFEST.md`](docs/BACKUP-MANIFEST.md) | 25-partition NVRAM/IMEI backup contents and restore list. |
| [`docs/RESEARCH-X682C.md`](docs/RESEARCH-X682C.md) | Exact-model videos, forums, blogs, auth methods. |
| [`docs/PLAN-lineageos.md`](docs/PLAN-lineageos.md) | Future LineageOS + OrangeFox + Magisk plan. |
| [`docs/PROJECT-STRUCTURE.md`](docs/PROJECT-STRUCTURE.md) | Annotated file/folder inventory. |

## Quick start

### Phone is bricked / bootlooping

1. Force off: **Power + Volume Up** until vibration stops.
2. Enter preloader: hold **Volume Up + Volume Down**, plug USB.
3. Flash exact V366 with SP Flash Tool:
   ```sh
   tools/SP_Flash_Tool_v5.2228_Linux/SP_Flash_Tool_v5.2228_Linux/flash_tool.sh
   ```
   Scatter:
   `firmware/V366/X682C-H694CD-Q-GL-220729V366(MobiFirmware.com)/MT6768_Android_scatter.txt`
   Mode: **Download Only**, preloader unticked first.
4. If SPFT refuses, use the verified mtkclient path in
   [`docs/BROM-NOTES.md`](docs/BROM-NOTES.md).

### Phone boots normally

```sh
adb devices
adb shell getprop ro.build.display.id
# X682C-H694CD-Q-GL-220729V366
adb shell getprop ro.boot.verifiedbootstate
# green
```

### Verify the kit

```sh
sha256sum -c SHA256SUMS.txt
cd backup/mtk-bypass && sha256sum -c SHA256SUMS.txt
```

Expected: every line `OK`.

## Recovery paths

| Situation | Path |
|---|---|
| Bootloop / black screen / bad flash | SPFT exact V366; mtkclient fallback |
| Secure BROM blocks DA auth | `tools/bypass_utility` → `Protection disabled` |
| IMEI/NVRAM zeroed | restore `backup/mtk-bypass/` via bypass + DA |
| No USB/preloader at all | test point / eMMC ISP |
| Wants LineageOS/OrangeFox/Magisk | [`docs/PLAN-lineageos.md`](docs/PLAN-lineageos.md) |

### mtkclient path (verified)

```sh
cd $HOME/Infinix/tools/bypass_utility
../mtkclient/.venv/bin/python main.py
# wait for: Protection disabled

cd $HOME/Infinix
tools/mtkclient/.venv/bin/python scripts/dump-nvram.py
```

Run the dump/write as the **first** mtkclient process after bypass; the BROM
window is short. Do not run `gettargetconfig` first.

### Restore the stock splash

```sh
cd $HOME/Infinix
env -u LOGO_IMAGE tools/mtkclient/.venv/bin/python scripts/verify-write.py
```

## Verified evidence

- V366 zip:
  `ce62372d4e3f4cce49b9a929c0b6b5ead0eb18f910a0071918edb891d92c2603`
- 25 partition dumps: all `SHA256SUMS.txt` entries pass.
- `boot.bin` / `recovery.bin` hash-match exact V366 images.
- `nvram.bin` + `nvdata.bin` contain `NVD_IMEI`; `proinfo.bin` contains the serial.
- Bypass output: `Protection disabled`, target config `0x0`.
- Write test: exact `logo.bin` written and read back, identical hash.

Details: [`docs/V366-info.md`](docs/V366-info.md),
[`docs/BACKUP-MANIFEST.md`](docs/BACKUP-MANIFEST.md),
[`docs/BROM-NOTES.md`](docs/BROM-NOTES.md).

## Safety

1. **Never Format All** — wipes NVRAM/IMEI.
2. **Never flash X682B firmware** — wrong model.
3. **Never flash a custom `logo.bin`** — a mtklogo repack caused a boot loop +
   continuous vibration on this unit. Stock was restored.
4. Keep `backup/mtk-bypass/` private — IMEI/calibration.
5. Do not relock the bootloader with custom software.
6. Do not write the sparse `super.img` with mtkclient; use SP Flash Tool.

## If moved to another PC

The venv and absolute paths break; recreate:

```sh
python3 -m venv tools/mtkclient/.venv
tools/mtkclient/.venv/bin/pip install \
  pyusb pycryptodome pycryptodomex colorama pyserial \
  keystone-engine capstone unicorn mfusepy json5

sudo cp tools/udev/*.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules && sudo udevadm trigger
```

SP Flash Tool has its own bundled libs.

## Sources

- V366 full ROM: MediaFire quickkey `6kto8gp7xjeix7d` (MobiFirmware mirror)
- V360 full ROM: AndroidFileHost `?fid=15664248565197182288`
- V360→V366 OTA: official Google OTA CDN
- SP Flash Tool: `cdn.spflashtools.com`
- mtkclient: `github.com/bkerler/mtkclient`
- MTK-bypass: `github.com/MTK-bypass/bypass_utility`
- TWRP: SourceForge `infinix-custom-recovery`

Research index: [`docs/RESEARCH-X682C.md`](docs/RESEARCH-X682C.md).
