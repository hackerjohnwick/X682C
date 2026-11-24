# Infinix Hot 10 — X682C (connected device)

Dump taken over ADB on 2026-11-24. Raw data: `device-info/`.

## Identity

| Item | Value |
|---|---|
| Marketing name | Infinix HOT 10 |
| Model | Infinix X682C |
| Product | X682C-GL (Global) |
| Serial | REDACTED (private) |
| Build | X682C-H694CD-Q-GL-220729V366 |
| Android | 10 (SDK 29, QP1A.190711.020) |
| Security patch | 2022-07-05 |
| Build date | 2022-07-29 / 2022-07-30 CST |
| SoC | MediaTek MT6768 (Helio G70/G85 family) |
| CPU | 8x ARM Cortex, arm64-v8a |
| Kernel | 4.14.141+ (2022-07-29) |
| RAM | 6 GB (5,952,916 kB) |
| Storage | 128 GB, userdata 110 GB |
| Display | 720 x 1640, 320 dpi |
| Battery | Li-ion, 100%, 4.28 V, health good |
| Encryption | FBE (file-based), state encrypted |
| Bootloader | LOCKED, verified boot GREEN, dm-verity enforcing |
| Dynamic partitions | yes (super), non-A/B |

## Current partition map (`/dev/block/by-name`)

boot_para p1, expdb p4, frp p5, metadata p6, md_udc p7, misc p15,
md1img p18, gz1 p24, gz2 p25, lk p27, lk2 p28, logo p29, boot p30,
dtbo p31, cache p38, userdata p40, flashinfo p42, plus:
nvcfg, nvdata, nvram, otp, para, persist, proinfo, protect1, protect2,
recovery, scp1, scp2, sec1, seccfg, spmfw, sspm_1, sspm_2, super,
tee1, tee2, tkv, tranfs, vbmeta, vbmeta_system, vbmeta_vendor.

Full symlink list: `device-info/block-by-name.txt`.

## Partition layout notes

- `super` holds system, vendor, product (dynamic partitions).
- Non-A/B: single `boot`, `recovery`, `dtbo`, `lk`, `vbmeta*`.
- Device-unique data that must never be lost: `nvram`, `nvdata`, `nvcfg`,
  `persist`, `proinfo`, `protect1`, `protect2`, `seccfg`, `frp`.

## Raw info files

- `props-full.txt` — every getprop key (1279 lines)
- `props-key.txt` — build/product/boot properties
- `kernel-system.txt` — kernel, memory
- `display-battery-storage.txt` — display, battery, filesystems
- `block-by-name.txt` — partition symlinks
- `partition-map.txt` — full offset/size table from the V360 scatter
- `identifiers.txt` — serial + IMEI (mode 600, private; do not upload)
- `cpuinfo.txt`, `thermal.txt`, `packages*.txt`, `secure-settings.txt`,
  `connectivity.txt`, `telephony.txt`, `identifiers-props.txt`
