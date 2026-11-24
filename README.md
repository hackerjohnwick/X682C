<div align="center">

# Infinix HOT 10 - X682C

**Recovery kit, field notes, and deep-dive documentation**

`X682C-H694CD-Q-GL-220729V366`

![Device](https://img.shields.io/badge/device-Infinix%20HOT%2010%20X682C-orange?style=for-the-badge)
![SoC](https://img.shields.io/badge/SoC-MediaTek%20MT6768-blue?style=for-the-badge)
![Android](https://img.shields.io/badge/Android-10%20%7C%20SDK%2029-3ddc84?style=for-the-badge)
![Build](https://img.shields.io/badge/build-220729V366-lightgrey?style=for-the-badge)
[![Release](https://img.shields.io/github/v/release/hackerjohnwick/X682C?style=for-the-badge&color=blue)](https://github.com/hackerjohnwick/X682C/releases/latest)

![NVRAM](https://img.shields.io/badge/NVRAM%2FIMEI%20backup-verified-brightgreen?style=flat-square)
![BROM](https://img.shields.io/badge/BROM%20bypass-verified-green?style=flat-square)
![DA write](https://img.shields.io/badge/DA%20write-verified-brightgreen?style=flat-square)
![SPFT](https://img.shields.io/badge/SPFT%20flash-untested-yellow?style=flat-square)
![Hardware](https://img.shields.io/badge/dead%20eMMC-ISP%20only-red?style=flat-square)

</div>

---

## What this is

A complete recovery kit for **one phone**: the Infinix HOT 10 **X682C** on exact
firmware `X682C-H694CD-Q-GL-220729V366`.

It contains the exact factory ROM, a device-unique NVRAM/IMEI backup, the
secure-BROM bypass, verified read/write scripts, and a full course explaining
how the phone boots, how it breaks, and how to bring it back.

> [!IMPORTANT]
> This public repository contains documentation, scripts, and safe tooling
> source. The private NVRAM/IMEI backup, raw device data, firmware ZIPs, and the
> proprietary SP Flash Tool are intentionally **not** committed. See
> [Repository scope](#repository-scope).

## Status at a glance

| Area | State |
|:---|:---|
| Exact V366 full ROM | ✅ Saved, hash and fingerprints verified |
| NVRAM / IMEI / persist backup | ✅ 25 partitions, all hashes verified |
| Secure BROM bypass (SBC+SDA) | ✅ `Protection disabled` |
| mtkclient DA read | ✅ 872 MB dump completed |
| mtkclient DA write | ✅ Write and read-back hash identical |
| SP Flash Tool actual flash | ⚠️ Not physically tested |
| Full `super` write / NVRAM restore | ⚠️ Not executed, destructive |
| Dead eMMC or no USB | ❌ Test point or ISP only |

**Read this first:** [Recovery readiness](docs/RECOVERY-READINESS.md) -
**Learn the whole thing:** [LEARN.md](docs/LEARN.md) -
**Operate it:** [AGENTS.md](docs/AGENTS.md)

## Download

[![Latest release](https://img.shields.io/github/v/release/hackerjohnwick/X682C?style=flat-square&color=blue)](https://github.com/hackerjohnwick/X682C/releases/latest)

The release carries the official OTA, TWRP reference, public docs/scripts
archive, SHA256 manifest, and verified source links for the exact V366 and
fallback V360 full ROMs. The 2.8 GB and 3.2 GB firmware ZIPs stay on their
source mirrors due GitHub asset limits; verify their hashes before flashing.

## Device

| | |
|:---|:---|
| Marketing name | Infinix HOT 10 |
| Model / product | X682C / X682C-GL |
| SoC | MediaTek MT6768 |
| CPU | ARM64, 8 cores |
| RAM / storage | 6 GB / 128 GB |
| Display | 720x1640, 320 dpi |
| Android | 10, SDK 29 |
| Build | `X682C-H694CD-Q-GL-220729V366` |
| Security patch | 2022-07-05 |
| Partitioning | non-A/B, dynamic `super`, eMMC |
| Bootloader | Locked, verified boot green |
| BROM security | SBC+SDA, open-source bypass works |

Raw device data: [DEVICE.md](docs/DEVICE.md) -
[device-info](docs/device-info/)

## Recovery flow

```text
Phone will not boot?
        |
        +-- ADB works? ----------> back up data, inspect build, choose soft fix
        |
        +-- Fastboot works? ------> flash boot / recovery / vbmeta (unlocked only)
        |
        +-- Preloader or BROM? ---> SPFT exact V366, or bypass + mtkclient
        |
        +-- No USB at all? -------> force off, drain, test point, ISP
```

| Situation | Use |
|:---|:---|
| Bootloop, black screen, bad flash | SP Flash Tool with exact V366 |
| SPFT refuses, BROM available | `bypass_utility` then mtkclient |
| IMEI or NVRAM zeroed | Restore `backup/mtk-bypass/` |
| No USB or preloader | Test point / eMMC ISP |
| Custom ROM / recovery / root | [LineageOS plan](docs/PLAN-lineageos.md) |

> [!WARNING]
> Never run **Format All** in SP Flash Tool. It erases NVRAM, IMEI, and
> calibration. Use **Download Only** or **Firmware Upgrade**.

## Quick start

### 1. Phone is bricked

```sh
# Force off
# Hold Power + Volume Up until vibration stops

# Enter preloader
# Hold Volume Up + Volume Down, then plug USB

# Flash exact V366
tools/SP_Flash_Tool_v5.2228_Linux/SP_Flash_Tool_v5.2228_Linux/flash_tool.sh
```

Scatter file:

```text
firmware/V366/X682C-H694CD-Q-GL-220729V366(MobiFirmware.com)/MT6768_Android_scatter.txt
```

Mode: **Download Only**, preloader unticked on the first attempt.

### 2. Phone boots

```sh
adb devices
adb shell getprop ro.build.display.id
# X682C-H694CD-Q-GL-220729V366

adb shell getprop ro.boot.verifiedbootstate
# green
```

### 3. Verify the kit

```sh
sha256sum -c SHA256SUMS.txt
cd backup/mtk-bypass && sha256sum -c SHA256SUMS.txt
```

Expected: every line `OK`.

## The verified mtkclient path

Only use this after reading [BROM notes](docs/BROM-NOTES.md).

```sh
# 1. Force off, enter preloader, then bypass
cd "$HOME/Infinix/tools/bypass_utility"
../mtkclient/.venv/bin/python main.py
# wait for: Protection disabled

# 2. Dump NVRAM and friends as the first client after bypass
cd "$HOME/Infinix"
tools/mtkclient/.venv/bin/python scripts/dump-nvram.py

# 3. Restore the stock splash if ever needed
env -u LOGO_IMAGE tools/mtkclient/.venv/bin/python scripts/verify-write.py
```

The BROM window is short. Run the dump or write as the **first** mtkclient
process after `Protection disabled`. Do not run `gettargetconfig` first.

## Repository map

```text
.
├── README.md                         this file
├── AGENTS.md -> docs/AGENTS.md       agent tooling symlink
├── agent.md  -> docs/AGENTS.md       lowercase tooling symlink
├── SHA256SUMS.txt                    top-level artifact hashes
├── .gitignore
├── docs/
│   ├── LEARN.md                      full 20-part course
│   ├── AGENTS.md                     operational playbook
│   ├── PROJECT-STRUCTURE.md          annotated inventory
│   ├── RECOVERY-READINESS.md         verified vs untested
│   ├── BROM-NOTES.md                 bypass, DA, force-off
│   ├── DEVICE.md                     device identity
│   ├── V366-info.md / V360-info.md   firmware evidence
│   ├── EXACT-V366-RESTORE.md         fallback restore
│   ├── BACKUP-MANIFEST.md            NVRAM/IMEI manifest
│   ├── RESEARCH-X682C.md             videos, forums, tools
│   ├── PLAN-lineageos.md             custom ROM plan
│   ├── device-info/                  private raw dump
│   └── ota-metadata/                 OTA metadata
├── scripts/
│   ├── dump-nvram.py                 post-bypass partition dump
│   ├── verify-write.py               write and read-back check
│   └── backup-critical.sh            reference script
├── firmware/                         local only, gitignored
├── backup/                           local only, private
└── tools/                            SPFT, mtkclient, bypass, udev, TWRP
```

Full annotated inventory: [PROJECT-STRUCTURE.md](docs/PROJECT-STRUCTURE.md).

## Documentation

| Document | What it covers |
|:---|:---|
| [**LEARN.md**](docs/LEARN.md) | Full course from layman basics to MTK internals, bootloader, recovery, ROMs, root, bootloops, bricks, causes, labs, glossary, quiz. |
| [AGENTS.md](docs/AGENTS.md) | Exact operational playbook for future agents. |
| [RECOVERY-READINESS.md](docs/RECOVERY-READINESS.md) | Verified vs untested matrix and recovery limits. |
| [BROM-NOTES.md](docs/BROM-NOTES.md) | Secure BROM bypass, DA read/write evidence, force-off and entry combos. |
| [DEVICE.md](docs/DEVICE.md) | Device identity, build, partition map, raw-data index. |
| [V366-info.md](docs/V366-info.md) | Exact ROM hashes, fingerprints, package contents. |
| [V360-info.md](docs/V360-info.md) | Fallback V360 evidence and OTA preconditions. |
| [EXACT-V366-RESTORE.md](docs/EXACT-V366-RESTORE.md) | Fallback V360 plus OTA restore. |
| [BACKUP-MANIFEST.md](docs/BACKUP-MANIFEST.md) | 25-partition NVRAM/IMEI backup and restore list. |
| [RESEARCH-X682C.md](docs/RESEARCH-X682C.md) | Exact-model videos, forums, blogs, auth methods. |
| [PLAN-lineageos.md](docs/PLAN-lineageos.md) | Future LineageOS + OrangeFox + Magisk plan. |
| [PROJECT-STRUCTURE.md](docs/PROJECT-STRUCTURE.md) | Annotated file and folder inventory. |

## Verified evidence

```text
V366 zip SHA256
ce62372d4e3f4cce49b9a929c0b6b5ead0eb18f910a0071918edb891d92c2603

boot.bin     = exact V366 boot.img
recovery.bin = exact V366 recovery.img
nvram.bin    contains NVD_IMEI
proinfo.bin  contains the device serial
write test   exact logo.bin written, read back, hash identical
```

Details: [V366 evidence](docs/V366-info.md) -
[backup manifest](docs/BACKUP-MANIFEST.md) -
[BROM notes](docs/BROM-NOTES.md)

## Safety

> [!CAUTION]
> 1. Never **Format All**. It wipes NVRAM, IMEI, and calibration.
> 2. Never flash X682B firmware. X682B is a different model.
> 3. Never flash a custom `logo.bin`. A mtklogo repack caused a boot loop and
>    continuous vibration on this unit.
> 4. Keep `backup/mtk-bypass/` private. It contains IMEI and calibration data.
> 5. Do not relock the bootloader with custom software installed.
> 6. Do not write sparse `super.img` with mtkclient. Use SP Flash Tool.

## Repository scope

| Item | In public repo | Why |
|:---|:---:|:---|
| Docs, scripts, source | ✅ | Reproducible and reviewable |
| Exact firmware ZIPs | ❌ | Large; keep in local kit or release |
| NVRAM / IMEI backup | ❌ | Private device identity |
| `docs/device-info/` | ❌ | Serial, IMEI, bugreport |
| SP Flash Tool | ❌ | Proprietary MediaTek binary |
| TWRP image | ✅ | Small third-party reference |
| mtkclient source | ✅ | Open source |

## If moved to another PC

The venv and absolute paths break. Recreate:

```sh
python3 -m venv tools/mtkclient/.venv
tools/mtkclient/.venv/bin/pip install \
  pyusb pycryptodome pycryptodomex colorama pyserial \
  keystone-engine capstone unicorn mfusepy json5

sudo cp tools/udev/*.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules && sudo udevadm trigger
```

SP Flash Tool bundles its own libraries.

## Sources

| Component | Source |
|:---|:---|
| V366 full ROM | MediaFire quickkey `6kto8gp7xjeix7d`, MobiFirmware mirror |
| V360 full ROM | AndroidFileHost `?fid=15664248565197182288` |
| V360 to V366 OTA | Official Google OTA CDN |
| SP Flash Tool | `cdn.spflashtools.com` |
| mtkclient | `github.com/bkerler/mtkclient` |
| MTK-bypass | `github.com/MTK-bypass/bypass_utility` |
| TWRP | SourceForge `infinix-custom-recovery` |

Research index: [RESEARCH-X682C.md](docs/RESEARCH-X682C.md)

<div align="center">

**One phone. One exact build. One verified recovery path.**

</div>
