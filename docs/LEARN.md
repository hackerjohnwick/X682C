# LEARN.md — Infinix X682C: from zero to deep water

A complete course for this exact phone and this recovery kit:

- **Infinix HOT 10 X682C**
- MediaTek **MT6768**
- Android **10**, build **X682C-H694CD-Q-GL-220729V366**
- non-A/B, dynamic `super`, eMMC

No prior knowledge assumed. Read in order the first time. Later use it as a
reference.

## The 20 parts

1. [Foundations](#part-1-foundations)
2. [Storage, partitions, images](#part-2-storage-partitions-images)
3. [Boot process and verified boot](#part-3-boot-process-and-verified-boot)
4. [Tools and interfaces](#part-4-tools-and-interfaces)
5. [Firmware, ROMs, OTAs](#part-5-firmware-roms-otas)
6. [NVRAM, IMEI, calibration](#part-6-nvram-imei-calibration)
7. [Bootloader](#part-7-bootloader)
8. [Custom recovery](#part-8-custom-recovery-twrp--orangefox)
9. [Custom ROM](#part-9-custom-rom-lineageos--gsi)
10. [Root](#part-10-root-magisk)
11. [Bootloop](#part-11-bootloop)
12. [Brick taxonomy](#part-12-brick-taxonomy)
13. [Recovery playbooks](#part-13-recovery-playbooks)
14. [Why it happens](#part-14-why-it-happens--causal-map)
15. [Deep water: MTK](#part-15-deep-water--mtk-internals)
16. [This kit](#part-16-this-kit-step-by-step)
17. [Troubleshooting](#part-17-troubleshooting-encyclopedia)
18. [Safe learning path](#part-18-safe-learning-path)
19. [Glossary](#part-19-glossary-with-analogies)
20. [Check yourself](#part-20-check-yourself)

> This guide teaches. It does not replace `README.md` at the repo root (quick
> start), `docs/AGENTS.md` (operational playbook), or
> `docs/PROJECT-STRUCTURE.md` (inventory).
> Everything here is about understanding and doing safely.

---

## How to use this guide

- **Parts 1–6** are the foundation: hardware, storage, boot, tools, firmware,
  NVRAM/IMEI.
- **Parts 7–10** are modification: bootloader, custom recovery, custom ROM, root.
- **Parts 11–14** are failure: bootloop, bricks, recovery playbooks, causes.
- **Parts 15–20** are deep water, this kit, troubleshooting, labs, glossary, quiz.
- Every major concept has a one-line analogy.
- Commands are real, but some are **destructive**. Read the warning before each.
- The phone in this kit is currently stock and working. Do not flash it “to test”
  unless you accept the risk and have the backup.

**Analogy:** this is a driving manual, not a “press this while the car is moving”
list.

---

## Part 1: Foundations

### 1.1 The phone is a stack, not one thing

Hardware:

| Part | Job | Analogy |
|---|---|---|
| SoC | CPU, GPU, modem, USB, storage controller on one chip | Whole office building on one chip |
| CPU | Executes code | Workers |
| RAM | Temporary memory; loses contents on power-off | Desks and whiteboards |
| eMMC | Permanent flash storage | Filing cabinets |
| PMIC | Power distribution | Building electrician |
| Modem | Cellular radio | Post office |
| Sensors | Motion, light, proximity, fingerprint | Building sensors |

Software:

```text
BootROM
  -> Preloader
    -> LK / bootloader
      -> boot.img (kernel + ramdisk)
        -> Android
          -> apps
```

Separate paths:

```text
bootloader -> recovery.img -> stock recovery / TWRP / OrangeFox
bootloader -> fastboot protocol over USB
BootROM    -> BROM/EDL service mode over USB
```

**Analogy:** a relay race. Each runner hands the baton to the next. A brick is a
dropped baton; the earlier it drops, the deeper the repair.

### 1.2 Bits, bytes, blocks

- 1 byte = 8 bits.
- Storage is read/written in **blocks** (usually 512-byte logical sectors).
- A 64 MB partition is about 131,072 sectors.

Flashing writes sectors, not files. Files are just containers.

**Analogy:** eMMC is a library of numbered pages; flashing writes page numbers
directly.

### 1.3 What “brick” actually means

A brick is not one disease:

- **Android brick:** Android fails, but recovery/fastboot/bootloader work.
- **Boot brick:** `boot` or `super` is bad; recovery/fastboot may work.
- **Bootloader brick:** LK/preloader bad; only preloader/BROM appears.
- **Deep brick:** only BROM/test point; or no USB.
- **Hardware:** dead eMMC/PMIC/CPU/board.

Always find the **highest layer that still responds**.

**Analogy:** “the building is closed” could mean the front door is locked, the
manager is missing, the power is out, or the foundation cracked. Each has a
different fix.

### 1.4 The three questions for any broken phone

1. **What still appears on USB?** Nothing, preloader, BROM, fastboot, ADB?
2. **What did I change last?** Logo, boot, ROM, Magisk module, OTA, none?
3. **What is unique and must not be lost?** IMEI/NVRAM, photos, encryption keys?

**Analogy:** triage: breathing, cause, valuables.

---

## Part 2: Storage, partitions, images

### 2.1 eMMC vs UFS

- **eMMC**: simpler flash, one command/data bus; common on budget phones.
- **UFS**: faster, full-duplex; common on flagships.

This X682C uses **eMMC**.

**Analogy:** eMMC is a single-lane road; UFS is a dual carriageway.

### 2.2 GPT: the table of contents

GPT lists each partition’s name, start block, size, type, and unique ID.

Linux exposes names under `/dev/block/by-name/`. Example:

```text
boot -> /dev/block/mmcblk0p30
cache -> /dev/block/mmcblk0p38
userdata -> /dev/block/mmcblk0p40
```

The exact map is in `docs/device-info/block-by-name.txt` and
`docs/device-info/partition-map.txt`.

| Concept | Meaning | Analogy |
|---|---|---|
| GPT | Partition table | Table of contents |
| Block | 512-byte unit | One page |
| Partition | Named storage region | One filing cabinet |
| Logical partition | Partition inside `super` | Room inside a warehouse |

### 2.3 The X682C partition map

Important entries:

| Partition | Role | Analogy |
|---|---|---|
| `preloader` | First-stage MediaTek loader | Night guard’s instructions |
| `lk`, `lk2` | Little Kernel bootloader | Building manager |
| `boot` | Kernel + ramdisk | Engine + startup script |
| `recovery` | Recovery OS | Basement workshop |
| `dtbo` | Device tree overlays | Hardware configuration sheets |
| `vbmeta*` | Android Verified Boot metadata | Tamper seals |
| `super` | Dynamic container for system/vendor/product | Warehouse with movable rooms |
| `system` | Android framework/apps | Main offices |
| `vendor` | Vendor HALs/firmware | Building-specific equipment |
| `product` | Product apps/config | Tenant customizations |
| `userdata` | User files/app data, encrypted | Personal lockers |
| `cache` | OTA/temp cache | Loading bay |
| `metadata` | Encryption/OTA metadata | Logbook |
| `misc` | Bootloader commands/state | Sticky note on manager’s desk |
| `persist` | Sensors, Wi-Fi/BT, DRM calibration | Calibration certificates |
| `nvram` | Modem/IMEI NV store | Passport office |
| `nvdata` | Modem/IMEI data | Passport backup files |
| `nvcfg` | NV configuration | Passport forms |
| `proinfo` | Product info/serial | Birth certificate |
| `protect1/2` | Protected calibration | Sealed calibration vault |
| `seccfg` | Lock/security state | Building lock policy |
| `frp` | Factory Reset Protection | Anti-theft latch |
| `logo` | Splash images | Front-door sign |
| `md1img` | Modem firmware | Post office machinery |
| `md_udc` | Modem user data | Post office records |
| `scp`, `sspm`, `spmfw`, `tee`, `tkv`, `tranfs` | MediaTek firmware pieces | Building subsystems |

Full map: `docs/DEVICE.md`, `docs/device-info/partition-map.txt`.

### 2.4 A/B vs non-A/B

- **A/B**: two copies of boot/system (`_a`, `_b`); updates switch slots.
- **Non-A/B**: one copy; updates patch in place.

This phone is **non-A/B**. It has a real `recovery` partition and a single
`boot`.

**Analogy:** A/B is two spare engines; non-A/B is one engine repaired in place.

### 2.5 Dynamic partitions and `super`

Android 10 introduced **dynamic partitions**. `system`, `vendor`, and `product`
are logical partitions inside one physical `super` partition. Their sizes can
change.

**Analogy:** a warehouse with movable internal walls; replacing the warehouse
replaces every room.

### 2.6 Raw vs sparse images

- **Raw**: every block, including zeros.
- **Sparse**: compact format with headers and only non-zero chunks.

`super.img` in the V366 package is **sparse**. SP Flash Tool handles it.
mtkclient raw `writeflash` does **not** convert it. Writing sparse data raw
corrupts the partition.

**Analogy:** a compressed shipping crate must be unpacked before placing the
furniture; dumping the crate itself is wrong.

### 2.7 File systems and encryption

Android uses ext4/f2fs for partitions. `userdata` is encrypted with
**File-Based Encryption (FBE)**. Recovery may not read it without credentials.

**Analogy:** each locker has its own lock; losing the key ring loses the
contents even if the locker is still there.

### 2.8 Checksums

- **MD5**: quick fingerprint.
- **SHA256**: strong fingerprint used by this kit.
- **ZIP test**: verifies archive structure.

**Analogy:** a checksum is the file’s fingerprint. Same name, different
fingerprint = different file.

---

## Part 3: Boot process and verified boot

### 3.1 Normal boot, step by step

1. Power/charger wakes PMIC.
2. SoC starts **BootROM** (immutable, inside the chip).
3. BootROM loads **preloader** from eMMC boot area into RAM.
4. Preloader sets up DRAM/storage and loads **LK** (bootloader).
5. LK checks keys/boot mode, loads **boot.img**.
6. Kernel mounts `super` and `userdata`.
7. Android `init` starts services; lock screen appears.

**Analogy:** foundation -> guard -> manager -> engine -> offices.

### 3.2 Recovery, fastboot, BROM

- **Recovery**: bootloader loads `recovery.img`; maintenance OS.
- **Fastboot**: bootloader USB protocol; flashing.
- **Preloader mode**: `0e8d:2000`, early loader; brief.
- **BROM**: `0e8d:0003`, chip service mode.
- **EDL**: emergency download; on MediaTek usually BROM/preloader.

**Analogy:** recovery is the workshop, fastboot is the loading dock, BROM is the
service hatch under the building.

### 3.3 Android Verified Boot (AVB)

`vbmeta` stores hashes/signatures and flags. A locked bootloader checks them.
`dm-verity` checks blocks as they are read.

States:

- **green**: verified stock.
- **orange**: unlocked/custom.
- **red**: verification failed.

This phone currently reports **green**, bootloader locked.

| Concept | Meaning | Analogy |
|---|---|---|
| AVB | Verified boot policy | Signed shipping manifest |
| `vbmeta` | Metadata/signatures/flags | Tamper seal |
| `dm-verity` | Block integrity check | Checking every page |
| Green state | Verified stock | All seals intact |

### 3.4 Why each stage fails

| Stage | Failure | Symptom |
|---|---|---|
| BootROM | Hardware/test point only | No USB or BROM only |
| Preloader | Bad preloader | Preloader loop, no LK |
| LK | Bad bootloader | Black screen, BROM only |
| `boot` | Bad kernel/ramdisk | Logo loop, no Android |
| `super` | Bad system/vendor | Boot animation loop |
| `userdata` | Encryption/key mismatch | Loop after lock screen |
| `vbmeta` | AVB mismatch | “Verification failed”, red state |
| `logo` | Invalid format | Splash loop/vibration (seen here) |

**Analogy:** each relay runner can drop the baton; the symptom tells you which
runner.

---

## Part 4: Tools and interfaces

### 4.1 ADB

Android Debug Bridge. Talks to Android or recovery.

```sh
adb devices
adb shell getprop ro.build.display.id
adb reboot bootloader
adb reboot recovery
adb reboot edl
```

**Analogy:** intercom to reception.

### 4.2 Fastboot

Bootloader flashing protocol. Write access depends on unlock state.

```sh
fastboot devices
fastboot flash boot boot.img
fastboot reboot
```

**Analogy:** loading dock with a strict manager.

### 4.3 SP Flash Tool

MediaTek’s flashing tool.

- Needs a **scatter file** and a **DA** (`MTK_AllInOne_DA.bin`).
- Modes: Download Only, Firmware Upgrade, Format All.
- Handles sparse `super.img`.

**Download Only** flashes listed images. It leaves partitions marked
`file_name: NONE` alone (NVRAM, proinfo, persist, etc.). **Format All** erases
them.

**Analogy:** a delivery service with a floor plan; Download Only delivers listed
items, Format All empties every room first.

### 4.4 mtkclient

Open-source Python tool for MediaTek BROM/preloader. Uploads a DA, reads/writes
partitions, dumps GPT.

```sh
python mtk.py printgpt
python mtk.py r nvram,nvdata nvram.bin,nvdata.bin
python mtk.py w logo logo.bin
```

**Analogy:** a universal service laptop that speaks the chip’s language.

### 4.5 bypass_utility and auth

Secure MediaTek boot can require:

- **SBC**: Secure Boot.
- **SLA**: Serial Link Authentication.
- **DAA**: Download Agent Authentication.

`bypass_utility` uses the kamakiri exploit to disable SLA/DAA in RAM.

This unit initially:

```text
SBC: True
SLA: False
DAA: True
Mem read auth: True
Mem write auth: True
```

After bypass:

```text
target config: 0x0
SBC/SLA/DAA: False
read/write auth: False
Protection disabled
```

The change is **temporary**; a power cycle restores normal security.

**Analogy:** the service hatch normally checks a signed work order; the bypass
temporarily turns off the signature checker.

### 4.6 USB drivers and udev

Linux uses udev rules to grant USB access. Windows needs MTK VCOM/preloader
drivers. SPFT includes a `Driver` folder.

**Analogy:** an access list for USB devices.

### 4.7 Tool comparison

| Tool | Level | Strength | Weakness |
|---|---|---|---|
| ADB | Android/recovery | Easy, safe | No access if Android dead |
| Fastboot | Bootloader | Standard flashing | Needs unlocked bootloader |
| SPFT | Preloader/BROM | Factory ROM, sparse support | Auth/driver quirks |
| mtkclient | BROM/preloader | Scriptable, read/write, backup | Needs DA/auth or bypass |
| bypass_utility | BROM | Disables SLA/DAA | Temporary; one-client window |
| Test point/ISP | Hardware | Works when USB dead | Opening phone, tools |

---

## Part 5: Firmware, ROMs, OTAs

### 5.1 Stock firmware package

A factory package contains:

- scatter map
- preloader, LK, boot, recovery, dtbo, vbmeta
- `super` (system/vendor/product)
- modem images and databases
- logo, cache, userdata
- checksums

The exact package here is `firmware/X682C-H694CD-Q-GL-220729V366.zip`.

**Analogy:** a complete replacement parts kit.

### 5.2 Full vs incremental OTA

- **Full OTA**: complete images; larger; broad source compatibility.
- **Incremental OTA**: patches changed blocks; smaller; exact source required.

The saved OTA is block-based, V360 → V366. Its updater checks source
fingerprints/block hashes and aborts on mismatch.

**Analogy:** a full OTA is a new engine; an incremental OTA is a repair kit cut
for one exact engine.

### 5.3 Build fingerprints

Example:

```text
Infinix/X682C-GL/Infinix-X682C:10/QP1A.190711.020/220729V366:user/release-keys
```

This identifies brand/product/device/Android/build/variant.

The V366 package has:

- product `220729V366`
- vendor `220729V302`
- system `220729V280`

All match the phone.

**Analogy:** a passport number; similar numbers are not the same person.

### 5.4 Scatter file fields

```yaml
- partition_index: SYS30
  partition_name: boot
  file_name: boot.img
  is_download: true
  linear_start_addr: 0x23500000
  partition_size: 0x2000000
  region: EMMC_USER
```

`file_name: NONE` means SPFT has no image for that partition.

**Analogy:** a delivery manifest with shelf numbers and box sizes.

### 5.5 Why exact build matters

Different builds can have different:

- partition layout
- vendor HALs
- preloader/LK
- AVB keys
- OTA preconditions
- modem databases

A “close enough” ROM can bootloop or lose IMEI.

**Analogy:** a key cut for a similar lock may enter but not turn.

---

## Part 6: NVRAM, IMEI, calibration

### 6.1 What NVRAM is

Modem NVRAM stores radio identity and calibration: IMEI, RF parameters, network
settings. On this phone it is split across `nvram`, `nvdata`, `nvcfg`.

**Analogy:** the phone’s passport office and calibration certificates.

### 6.2 What is device-unique

| Partition | Contains | Loss means |
|---|---|---|
| `nvram` | IMEI/NV store | Null IMEI, no signal |
| `nvdata` | modem data | IMEI/network problems |
| `nvcfg` | NV config | modem config issues |
| `persist` | sensors, Wi-Fi/BT MAC/calibration, DRM | sensors/MAC/DRM issues |
| `proinfo` | serial/product info | missing serial/product data |
| `protect1/2` | protected calibration | calibration loss |
| `seccfg` | lock state | lock/security problems |
| `frp` | FRP state | reset protection state |

**Analogy:** each is a different sealed certificate for a different subsystem.

### 6.3 Why ROM flash does not restore IMEI

`super` and `boot` do not contain your IMEI. The scatter marks NVRAM/proinfo/
persist as `file_name: NONE`; Download Only leaves them. Format All erases them.

**Analogy:** replacing the offices does not recreate your passport; it lives in
a separate vault.

### 6.4 The backup in this kit

`backup/mtk-bypass/` — 25 partitions, 872 MB, all SHA256 verified:

- nvram, nvdata, nvcfg
- persist, proinfo, protect1/2
- seccfg, frp
- boot, recovery, dtbo, lk, lk2, logo
- md1img, md_udc
- misc/state partitions

`nvram`/`nvdata` contain `NVD_IMEI`; `proinfo` contains the serial.

**Analogy:** a fireproof safe with copies of every unique certificate.

### 6.5 Restore rules

After bypass + DA, write one at a time:

```text
nvram, nvdata, nvcfg, persist, proinfo, protect1, protect2
```

Read back and compare SHA256. Do not write `seccfg`/`frp` casually. Never use
another phone’s NVRAM.

**Analogy:** return the correct passport to the correct person.

### 6.6 Legal note

IMEI modification is regulated in many countries. This kit restores the phone’s
own backup; it is not for changing identity or bypassing theft controls.

---

## Part 7: Bootloader

### 7.1 What the bootloader is

LK (Little Kernel) is MediaTek’s bootloader. It:

- initializes hardware
- reads buttons/boot mode
- verifies images (AVB)
- loads `boot`, `recovery`, or fastboot

**Analogy:** the building manager who decides which door opens.

### 7.2 Locked vs unlocked

- **Locked**: only signed stock images; fastboot writes blocked.
- **Unlocked**: custom images allowed; verified boot becomes orange; data wipes.

`ro.boot.flash.locked=1` means locked.

**Analogy:** locked building with a strict inspection policy.

### 7.3 Unlock procedure (expected for this phone)

```sh
adb reboot bootloader
fastboot devices
fastboot flashing unlock
# confirm on phone
fastboot getvar unlocked
```

If rejected:

- enable **OEM unlocking** in Developer options
- try `fastboot oem unlock`
- update ADB/fastboot
- check USB cable/port

**This was not executed on this phone.** The plan is in
`docs/PLAN-lineageos.md`.

**Analogy:** asking the manager to remove the master lock; it wipes the
building’s personal lockers.

### 7.4 What unlock changes

- wipes `userdata`
- allows custom boot/recovery
- changes AVB state to orange
- may affect banking/DRM apps
- voids warranty

**Analogy:** the inspection sticker is removed; some tenants no longer trust the
building.

### 7.5 Relock rules

Only relock with **full stock** firmware and stock boot/recovery/vbmeta.
Relocking with custom software can brick or refuse to boot.

**Analogy:** do not re-arm the alarm while the windows are still open.

### 7.6 Why unlock fails

| Cause | Fix |
|---|---|
| OEM unlocking off | Enable in Developer options |
| No unlock support | `fastboot flashing unlock` unsupported |
| Driver/USB | Cable, port, udev/driver |
| Battery low | Charge |
| Wrong mode | Must be bootloader, not ADB |

---

## Part 8: Custom recovery (TWRP / OrangeFox)

### 8.1 What recovery is

A small OS in `recovery.img` that can:

- apply signed OTA
- wipe data/cache
- mount partitions
- adb sideload
- backup/restore

**Analogy:** a workshop in the basement.

### 8.2 Stock vs custom

- Stock recovery: signed OTA only; limited UI.
- TWRP/OrangeFox: touch UI, terminal, backup, file manager, MTP, fastbootd.

**Analogy:** stock is a service window; custom is a full workshop.

### 8.3 Non-A/B and dynamic partitions

This phone:

- real `recovery` partition (not recovery-as-boot)
- `super` with logical system/vendor/product
- no slots

Recovery must:

- read `super` (or use fastbootd)
- handle non-A/B fstab
- decrypt/format `userdata`
- support USB OTG/MTP

**Analogy:** the workshop must know the warehouse’s movable walls.

### 8.4 Building OrangeFox/TWRP

Inputs:

- device tree: `device/infinix/X682C`
- kernel: stock 4.14 or prebuilt
- vendor blobs: from stock ROM
- fstab: dynamic super, non-A/B
- BoardConfig flags:
  - `PRODUCT_USE_DYNAMIC_PARTITIONS := true`
  - `TW_INCLUDE_FASTBOOTD := true`
  - recovery partition present
  - `TARGET_ARCH=arm64`, `TARGET_2ND_ARCH=arm`

Build:

```sh
source build/envsetup.sh
lunch fox_X682C-eng
mka recoveryimage
```

Test:

```sh
fastboot boot recovery.img
# if unsupported:
fastboot flash recovery recovery.img
```

**Analogy:** build a workshop that fits this basement; do not use a random
workshop from another building.

### 8.5 Why custom recovery bootloops/fails

| Cause | Symptom | Fix |
|---|---|---|
| Wrong kernel/ramdisk | Black screen/loop | Use matched stock kernel |
| Wrong fstab | Cannot mount data/super | Fix fstab |
| AVB/vbmeta | Verification failure | Disable verity/verification |
| Encryption | Data unreadable | Format data or decrypt |
| Sparse super | Mount fail | Use fastbootd/TWRP support |
| Wrong device tree | Touch/display dead | Correct device tree |
| Boot image too large | Flash fail | Trim ramdisk/modules |

**Analogy:** a workshop with the wrong door sizes cannot open the rooms.

### 8.6 Recovery backups

A nandroid can back up `boot`, `system`, `vendor`, `data`. For this kit, the
most important backups are already in `backup/mtk-bypass/`.

**Analogy:** photocopy the certificates before renovating.

---

## Part 9: Custom ROM (LineageOS / GSI)

### 9.1 What a custom ROM is

A replacement Android system built from source or a generic image:

- **device-specific ROM**: device tree + kernel + vendor blobs
- **GSI**: generic system image; uses stock vendor/kernel

**Analogy:** device-specific is a tailored suit; GSI is adjustable clothing.

### 9.2 Parts of a device port

| Part | Job | Analogy |
|---|---|---|
| Device tree | Build recipe and hardware config | Architectural plan |
| Kernel | Hardware drivers | Engine |
| Vendor blobs | Proprietary libraries | Custom fittings |
| HALs | Camera/audio/RIL/sensors interfaces | Department adapters |
| fstab | Mount rules | Room map |
| SELinux policy | Access control | Security rules |

### 9.3 This phone’s reality

- Android 10 vendor, kernel 4.14
- no official LineageOS device tree
- no official OrangeFox
- dynamic `super`, non-A/B
- MT6768 HALs from Transsion/MediaTek

Realistic target: **LineageOS 21 (Android 14)** with the 4.14 kernel, or a GSI.
Newer LineageOS may require a newer kernel/GKI this phone never had.

**Analogy:** fitting a modern engine into an older car; possible, but the
mounts and wiring must match.

### 9.4 Build flow (high level)

```sh
repo init -u https://github.com/LineageOS/android.git -b lineage-21.0
repo sync -c -j8
source build/envsetup.sh
breakfast X682C
brunch X682C
```

**Analogy:** gather the blueprint, parts, and tools, then assemble.

### 9.5 Flashing a ROM

Dynamic partitions need fastbootd:

```sh
fastboot reboot fastboot
fastboot flash system system.img
fastboot flash boot boot.img
fastboot --disable-verity --disable-verification flash vbmeta vbmeta.img
fastboot reboot
```

Wipe data when moving from stock/another ROM.

**Analogy:** replace the rooms, engine, and inspection policy together.

### 9.6 Why custom ROMs fail

| Cause | Result |
|---|---|
| Wrong vendor blobs | Camera/RIL/audio dead |
| Wrong kernel | No boot |
| Missing firmware | No modem/Wi-Fi |
| AVB not disabled | Verification loop |
| Wrong partition sizes | Flash fails |
| Encryption mismatch | Bootloop at lock |
| Wrong GSI arch | No boot |
| SELinux denial | Services crash |
| Kernel too old for Android | Bootloop |

**Analogy:** a body that rejects the transplanted organ; compatibility is
everything.

---

## Part 10: Root (Magisk)

### 10.1 What root is

Root means uid 0: full control of Android. Magisk provides **systemless** root
by patching the boot ramdisk, not modifying `/system`.

**Analogy:** a master key, hidden in the engine’s startup script.

### 10.2 Magisk flow

1. Extract the exact `boot.img`.
2. Magisk app → Install → Select and Patch a File.
3. Flash patched image:
   ```sh
   fastboot flash boot magisk_patched.img
   ```
4. Boot; verify Magisk app and `su`.

**Analogy:** stamp a master key into the startup script.

### 10.3 AVB and vbmeta

On Android 10, patched boot may require:

```sh
fastboot --disable-verity --disable-verification flash vbmeta vbmeta.img
```

This changes the verification policy, not the kernel.

**Analogy:** turn off the tamper alarm; it does not fix a bad engine.

### 10.4 Why root bootloops on X682C

Known trap: patched `boot`/`recovery` images that do not match the exact build
or ramdisk can bootloop. Use the exact V366 `boot.img`; do not mix builds.

Also:

- wrong vbmeta flags
- Magisk module incompatible
- encryption/data issue
- boot image too large

**Analogy:** the wrong key shape gets stuck in the lock.

### 10.5 Unroot / recover

- Flash exact stock `boot.img`.
- Or restore `boot.bin` from `backup/mtk-bypass/`.
- Remove Magisk modules in safe mode if Android still boots.

### 10.6 Order of operations

**Unlock -> custom recovery -> custom ROM -> root.**

Root last because a ROM flash replaces `boot` and may overwrite Magisk.

**Analogy:** renovate first, install the master key last.

---

## Part 11: Bootloop

### 11.1 Definition

A bootloop is a cycle: bootloader → kernel → Android → crash/reboot. It can
happen at any stage.

**Analogy:** a record stuck at the same groove.

### 11.2 Causes by stage

| Stage | Causes | Clues |
|---|---|---|
| Bootloader | Bad LK/preloader | Black screen, BROM only |
| Kernel | Bad boot.img, wrong ramdisk | Logo loop, no ADB |
| Logo | Bad logo.bin format | Splash loop/vibration |
| System | Bad `super`, missing files | Boot animation loop |
| Data | Encryption/key mismatch | Loop after lock |
| AVB | vbmeta/verity mismatch | Red state/verification |
| Modules | Magisk/Zygisk module | Loop after root |
| Hardware | eMMC/PMIC | No USB, heat |

### 11.3 Diagnosis ladder

1. Force off: **Power + Volume Up**.
2. Try normal boot.
3. Try recovery.
4. Try fastboot.
5. Check USB IDs (`lsusb`, Device Manager).
6. If Android boots, get `adb logcat`, `dmesg`, `pstore`.
7. If not, SPFT/mtkclient.

**Analogy:** check each floor of the building before calling the demolition crew.

### 11.4 Recovery ladder

| Available | Action |
|---|---|
| Android | Clear app/module; OTA; factory reset |
| Recovery | Wipe cache/data; sideload OTA; restore backup |
| Fastboot | Flash boot/recovery/vbmeta; unlock |
| Preloader/BROM | SPFT exact ROM; mtkclient |
| No USB | Force off/drain/test point/ISP |

### 11.5 Prevention

- Exact build/model.
- Full battery, good cable, USB 2.0.
- Do not interrupt flash.
- Do not Format All.
- Do not flash custom logo without verification.
- Keep stock boot/logo/vbmeta.
- Backup NVRAM first.

---

## Part 12: Brick taxonomy

### 12.1 Categories

| Type | What survives | Typical fix |
|---|---|---|
| Soft brick | Android/fastboot/recovery | Wipe, flash boot/system |
| Boot brick | Bootloader/fastboot | Flash boot/super |
| Preloader brick | Preloader/BROM | SPFT/mtkclient |
| Deep brick | BROM only | Bypass + DA/SPFT |
| No USB | Nothing | Force off, drain, test point/ISP |
| Hardware | Nothing | Board repair |

### 12.2 Force-off and entry on X682C

- **Force off**: **Power + Volume Up** (confirmed; Power alone 30 s failed).
- **Preloader**: phone off, hold **Volume Up + Volume Down**, plug USB.
- **Normal boot**: press Power.
- **Recovery**: Volume Up + Power (timing varies).
- **Fastboot**: `adb reboot bootloader` or recovery/bootloader menu.

### 12.3 Case study: custom logo

A custom `logo.bin` repacked with mtklogo caused a boot loop + continuous
vibration. Stock V366 `logo.bin` was written back with mtkclient, read-back hash
matched, phone booted.

Lessons:

- cosmetic partitions can break boot;
- a verified write path is essential;
- test on a harmless partition first;
- do not trust an untested repacker.

**Analogy:** a badly wired sign can trip the main breaker.

### 12.4 No USB at all

If force-off works but no USB appears:

- battery disconnect/reconnect;
- test point;
- ISP;
- PMIC/eMMC fault.

**Analogy:** the service hatch is welded shut; open the cabinet physically.

---

## Part 13: Recovery playbooks

### 13.1 A — Android works

```sh
adb devices
adb shell getprop ro.build.display.id
adb shell getprop ro.boot.verifiedbootstate
```

Use for app/data issues, not for flashing.

### 13.2 B — Recovery works

Stock recovery:

- wipe cache
- factory reset
- apply OTA from ADB/SD

Custom recovery:

- restore backup
- flash boot/system/vbmeta
- read `super` via fastbootd

### 13.3 C — Fastboot works

Requires unlocked bootloader for writes.

```sh
fastboot devices
fastboot flash boot boot.img
fastboot flash recovery recovery.img
fastboot --disable-verity --disable-verification flash vbmeta vbmeta.img
fastboot reboot
```

### 13.4 D — Preloader/BROM

Preferred: SP Flash Tool exact V366, Download Only.

Fallback: mtkclient.

```sh
cd $HOME/Infinix/tools/bypass_utility
../mtkclient/.venv/bin/python main.py
# wait for Protection disabled

cd $HOME/Infinix
tools/mtkclient/.venv/bin/python scripts/dump-nvram.py
```

The dump/write must be the **first** mtkclient process after bypass.

### 13.5 E — No USB

Force off, drain, battery disconnect, test point, ISP.

### 13.6 F — IMEI/NVRAM lost

Restore from `backup/mtk-bypass/` after bypass + DA. Write one partition,
read back, compare SHA256.

### 13.7 Exact build restore

Use `firmware/X682C-...V366.zip` with SPFT. Fallback: V360 + OTA.

---

## Part 14: Why it happens — causal map

| Cause | Why it breaks | Prevention |
|---|---|---|
| Wrong model ROM | Partition layout/hardware differ | Check X682C vs X682B |
| Wrong build | Vendor/AVB/modem mismatch | Match fingerprint |
| Format All | Erases NVRAM/calibration | Download Only |
| Sparse image raw write | Headers treated as data | Use SPFT for super |
| Interrupted flash | Partial partition | Battery/cable/USB 2.0 |
| Low battery | Power loss mid-write | Charge >50% |
| Bad cable/hub | Data errors/disconnect | Original cable, direct port |
| Custom logo repack | Invalid format | Do not flash untested logo |
| Patched boot mismatch | Kernel/ramdisk/AVB mismatch | Exact boot.img |
| Relock with custom | Bootloader rejects images | Relock only stock |
| Vbmeta flags wrong | Verification/verity policy | Match build |
| Encryption mismatch | Data key invalid | Format data or restore keys |
| Magisk module | System crash at boot | Safe mode/remove |
| Anti-rollback | Bootloader refuses old firmware | Do not downgrade blindly |
| eMMC wear/fault | Read/write errors | Backup, replace |

**Analogy:** every failure has a paper trail; follow it backward.

### 14.1 Failure right after each modification

| Step | Common failure | Why | First fix |
|---|---|---|---|
| Bootloader unlock | Wipe/data loss; orange state; apps refuse | Unlock deliberately wipes `userdata`; AVB state changes | Expected; restore data; do not relock with custom software |
| Custom recovery flash | Black screen/loop; cannot mount data/super | Wrong kernel, fstab, AVB, encryption, or slot model | Flash stock boot/recovery; use a matched device tree |
| Custom ROM flash | Bootloop; no camera/RIL/audio; verification fail | Vendor blobs/kernel/HAL mismatch; vbmeta not disabled; wrong GSI arch | Restore stock boot; use matched vendor; disable verity |
| Root (Magisk) | Bootloop; app detection; module crash | Wrong `boot.img`, ramdisk mismatch, module, vbmeta, encryption | Flash exact stock `boot.img`; remove modules in safe mode |
| Relock bootloader | Refuses to boot / brick | Custom images fail AVB | Unlock again or flash full stock before relocking |
| Format All | Null IMEI/baseband; no sensors/Wi-Fi | NVRAM/calibration erased | Restore the 25-partition backup via bypass/ISP |

**Analogy:** each renovation step can break a different utility; restore the
matching blueprint before blaming the whole building.

---

## Part 15: Deep water — MTK internals

### 15.1 BootROM, preloader, BROM

- **BootROM**: immutable, first code, USB protocol.
- **Preloader**: eMMC boot area, DRAM/storage init.
- **BROM**: BootROM service mode, `0e8d:0003`.
- **Preloader mode**: `0e8d:2000`, brief.

**Analogy:** foundation, guard, service hatch.

### 15.2 DA stages

- DA1: small loader, communication.
- DA2: full storage toolkit (XFlash).
- EMI: DRAM settings.
- Extensions: extra commands.

**Analogy:** service van, full toolbox, electrical diagram.

### 15.3 Auth: SBC, SLA, DAA

- SBC: secure boot.
- SLA: serial link auth.
- DAA: download agent auth.

This unit: `SBC+SDA`, config `0xe5`. Bypass disables checks in RAM.

**Analogy:** signed manifest, cable ID check, laptop check.

### 15.4 GPT and sector math

`size = (last_lba - first_lba + 1) * 512`.
mtkclient reads GPT, then reads sectors.

**Analogy:** page numbers and page counts.

### 15.5 Sparse and super

Sparse format stores chunks; `super` contains logical partitions with metadata.
SPFT expands sparse; mtkclient raw write does not.

**Analogy:** compressed crate vs furniture.

### 15.6 OTA internals

- transfer list commands: `new`, `zero`, `erase`, `copy`, `move`
- `.new.dat`: new data
- `.patch.dat`: patches
- updater script: fingerprints, hashes
- boot patch

**Analogy:** tailor’s alteration kit cut for one suit.

### 15.7 AVB internals

`vbmeta`: hashes/signatures, flags, rollback index. Locked bootloader enforces.

**Analogy:** signed manifest + tamper seal.

### 15.8 One-client BROM window

After bypass, the BROM may accept one clean DA session. Extra commands can
consume it; power cycle resets.

**Analogy:** a one-time visitor pass.

### 15.9 ISP/test point

Direct eMMC access bypasses SoC. Used for dead USB/eMMC.

**Analogy:** physical key to the filing cabinet.

---

## Part 16: This kit, step by step

### 16.1 Inventory

- `firmware/V366` — exact ROM
- `backup/mtk-bypass` — 25 partitions
- `scripts/dump-nvram.py` — backup
- `scripts/verify-write.py` — write test
- `tools/SP_Flash_Tool...` — SPFT
- `tools/mtkclient` — mtkclient
- `tools/bypass_utility` — auth bypass
- `docs/` — notes/research
- `docs/PROJECT-STRUCTURE.md` — map

### 16.2 What is verified

- V366 hash/fingerprints
- 25 partition hashes
- boot/recovery match
- bypass works
- DA read/write works
- stock logo restored

### 16.3 What is not

- SPFT actual flash
- full `super` write
- NVRAM restore
- hard no-USB

### 16.4 Current state

Phone online, exact V366, green verified boot, stock splash, NVRAM backup done.

---

## Part 17: Troubleshooting encyclopedia

| Error/symptom | Meaning | Fix |
|---|---|---|
| `adb: no devices` | USB/debug/driver | Cable, port, authorize, udev |
| `unauthorized` | RSA prompt | Accept on phone |
| `fastboot` empty | Not bootloader/driver | Reboot mode, USB 2.0 |
| SPFT no port | Not preloader/BROM | Buttons, cable, driver |
| `Auth file is required` | DAA/SLA | Bypass/auth |
| `Handshake failed` | Wrong mode/window | Power cycle, first client |
| `Sync error` | Too early/late | Retry, bypass again |
| `dm-verity` failed | Modified system | Stock/disable verity |
| Bootloop + vibration | Boot/logo corruption | Stock logo/boot |
| IMEI null | NVRAM lost | Restore backup |
| No USB | Deep/hardware | Force off/drain/ISP |
| Phone hot | Bootloop/charging | Unplug, cool |
| `super` write fails | Sparse/raw mismatch | SPFT |
| Custom logo loop | Bad format | Stock logo |

**Analogy:** each error is a labeled fuse; find the circuit.

---

## Part 18: Safe learning path

1. **Observer**: read docs, ADB read-only, checksums.
2. **Android user**: ADB/fastboot/recovery basics.
3. **Read-only low-level**: GPT, dump `proinfo`.
4. **Controlled write**: harmless partition, read back, hash.
5. **Full recovery**: SPFT, NVRAM restore.
6. **Custom**: unlock/recovery/ROM/root.

**Analogy:** shallow end before the ocean.

---

## Part 19: Glossary with analogies

| Term | Meaning | Analogy |
|---|---|---|
| ADB | Debug bridge | Intercom |
| AOSP | Android Open Source Project | Public blueprint |
| AVB | Verified boot | Signed manifest |
| A/B | Two system slots | Two spare engines |
| Bootloader | Loads kernel/recovery | Manager |
| BootROM | Immutable first code | Foundation |
| BROM | BootROM USB mode | Service hatch |
| Calibration | Device-specific RF/sensor data | Tuning certificates |
| DA | Download Agent | Repair laptop |
| DAA | Download Agent Auth | Laptop check |
| dm-verity | Block integrity | Page-by-page check |
| DTBO | Device tree overlays | Config sheets |
| eMMC | Flash storage | Filing cabinets |
| EDL | Emergency download | Loading dock |
| Fastboot | Bootloader protocol | Loading dock |
| FBE | File-based encryption | Per-locker locks |
| Firmware | Low-level software | Fixed systems |
| FRP | Reset protection | Anti-theft latch |
| GPT | Partition table | Table of contents |
| GSI | Generic system image | Universal furniture |
| IMEI | Cellular identity | Passport number |
| Kernel | Hardware core | Utilities |
| LK | Little Kernel | Assistant manager |
| Magisk | Systemless root | Fake badge |
| NVRAM | Modem/IMEI store | Passport office |
| OTA | Over-the-air update | Remote repair kit |
| Partition | Named storage region | Filing cabinet |
| Preloader | Early loader | Night guard |
| Ramdisk | Boot root filesystem | Startup toolbox |
| Recovery | Maintenance OS | Workshop |
| Scatter | Flash map | Floor plan |
| SBC | Secure boot | Foundation inspection |
| SLA | Serial link auth | Cable ID check |
| Sparse | Compact image | Shipping crate |
| `super` | Dynamic container | Movable-wall warehouse |
| TWRP | Custom recovery | Independent workshop |
| vbmeta | AVB metadata | Tamper seal |
| Vendor blobs | Proprietary libs | Custom fittings |
| VCOM | MediaTek COM port | Service phone line |
| Verified boot | Integrity policy | Inspection sticker |

---

## Part 20: Check yourself

1. BootROM vs preloader vs LK vs boot.img?
2. Why does `adb reboot edl` show preloader?
3. What does `Protection disabled` change, and does it survive reboot?
4. Why can a ROM flash leave IMEI intact?
5. What does Format All destroy?
6. Why can’t mtkclient raw-write sparse `super.img`?
7. Full vs incremental OTA?
8. Why green verified boot with locked bootloader?
9. What does Magisk patch, and why bootloop?
10. First three checks for a “brick”?
11. Why is `persist` important?
12. Why never write another phone’s NVRAM?
13. nvram vs nvdata vs nvcfg?
14. Safest first write test?
15. Why is “no USB” a different class?
16. What causes a custom recovery to bootloop?
17. What causes a custom ROM to bootloop?
18. What order to unlock/recovery/ROM/root?
19. What is the force-off combo on this phone?
20. What is the one-client BROM rule?

---

## Final mental model

- BootROM starts the building.
- Preloader opens the doors.
- LK chooses the path.
- Kernel runs utilities.
- Android runs offices.
- Partitions are rooms and cabinets.
- NVRAM is the passport office.
- `vbmeta` is the tamper seal.
- BROM/DA is the service hatch and certified laptop.
- Backups are fireproof copies.
- Checksums are fingerprints.

When something breaks: identify the highest living layer, protect unique data,
use the exact image, verify every write, and keep the stock path.
