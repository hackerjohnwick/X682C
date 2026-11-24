# Plan — LineageOS + OrangeFox + Magisk on Infinix Hot 10 (X682C)

Device: Infinix X682C, MT6768, Android 10 stock, kernel 4.14.141,
dynamic partitions, **non-A/B**, bootloader unlocked (data wiped). Stock build:
`X682C-H694CD-Q-GL-220729V366`.

Reality check: there is **no official LineageOS or OrangeFox build** for X682C.
This is a port. Existing base: unofficial TWRP device tree
(`Infinix-G70/android_device_twrp_infinix_x682c`) and an unofficial
`x682c-twrp.img`. Latest LineageOS (23.x / Android 16) may not run on the 4.14
kernel; target **LineageOS 21 (Android 14)** first, fall back to a LineageOS GSI
if the kernel/device tree will not boot.

Order: **unlock → OrangeFox → ROM → root**. Do not skip ahead.

## 0. Before touching anything (done / keep)

- [x] Exact full V366 ROM + V360/OTA fallback saved (`firmware/`).
- [x] SP Flash Tool Linux + mtkclient + udev rules saved (`tools/`).
- [x] Run `scripts/dump-nvram.py`; NVRAM/IMEI set saved and verified.
- [ ] Enable Developer options → USB debugging + OEM unlocking.
- [ ] Note IMEI, serial, and current build; keep `DEVICE.md`.

Unlocking wipes data. Back up photos/files first.

## 1. Bootloader unlock (done 2026-11-24)

```sh
adb reboot bootloader
fastboot devices
fastboot flashing unlock
# confirm on phone with Vol Up / Power
fastboot getvar unlocked        # expect: unlocked: yes
fastboot reboot
```

- If `flashing unlock` is rejected, try `fastboot oem unlock`.
- If both fail, stop: no recovery/ROM work is possible on a locked bootloader.
- After unlock, re-enable USB debugging; verify `ro.boot.flash.locked=0`.

Gate: **passed** (`unlocked: yes`). Data was wiped. Re-enable USB debugging after setup.

## 2. Dump stock images (unlocked, before modifying)

Needed for OrangeFox, LineageOS and rollback:

```sh
# With root (Magisk) or from OrangeFox/TWRP shell:
dd if=/dev/block/by-name/boot of=/sdcard/boot.img
dd if=/dev/block/by-name/recovery of=/sdcard/recovery.img
dd if=/dev/block/by-name/dtbo of=/sdcard/dtbo.img
dd if=/dev/block/by-name/vbmeta of=/sdcard/vbmeta.img
dd if=/dev/block/by-name/lk of=/sdcard/lk.img
```

Also pull `vendor`, `odm`, `product` blobs (or use the V360 ROM images) for the
LineageOS device tree. Store all of it in `backup/stock-images/` (create it).

## 3. OrangeFox recovery

1. Use the TWRP tree as the base:
   ```sh
   git clone -b pbrp https://github.com/Infinix-G70/android_device_twrp_infinix_x682c
   ```
   Place it at `device/infinix/X682C`, add `vendor/infinix/X682C` blobs and the
   stock `boot.img`/kernel.
2. Sync OrangeFox (branch matching Android 12.1/13 base):
   ```sh
   git clone https://gitlab.com/OrangeFox/sync.git
   cd sync && ./orangefox_sync.sh --branch 12.1 --path ~/fox_12.1
   ```
3. Set `FOX_DEVICE=Infinix-X682C`, `TARGET_DEVICE=X682C`,
   `PRODUCT_USE_DYNAMIC_PARTITIONS := true`, `TW_INCLUDE_FASTBOOTD := true`,
   `TW_IS_VENDOR_BOOT` off (device has a real recovery partition).
4. Build:
   ```sh
   source build/envsetup.sh
   lunch fox_X682C-eng
   mka recoveryimage
   ```
5. Test without touching stock:
   ```sh
   fastboot boot out/target/product/X682C/recovery.img
   ```
   If `fastboot boot` is unsupported, flash it:
   ```sh
   fastboot flash recovery recovery.img
   ```
6. Verify: decrypts/reads data, mounts super, USB OTG, ADB sideload,
   backup/restore, fastbootd.

Gate: OrangeFox boots and can read/write `super`; a full nandroid exists.

## 4. LineageOS port

Target: `lineage-21.0` (Android 14) with the 4.14 kernel. Newer branches only if
the kernel and HALs are ported.

1. Device tree: fork the TWRP tree to `device/infinix/X682C`, add
   `lineage_X682C.mk`, `BoardConfig.mk`, fstab (dynamic super, non-A/B),
   `PRODUCT_USE_DYNAMIC_PARTITIONS := true`.
2. Kernel: use stock 4.14.141 source if Infinix published it; otherwise
   prebuilt kernel from `boot.img` (`TARGET_PREBUILT_KERNEL`).
3. Vendor: extract `vendor`, `odm`, `product` from the V360 ROM; add
   `extract-files.sh` / proprietary-files list.
4. HALs: MT6768 needs the Transsion/MTK HALs (camera, audio, ril, sensors).
   Reuse the stock vendor partition (`TARGET_COPY_OUT_VENDOR := vendor`) before
   trying source-built HALs.
5. Build:
   ```sh
   repo init -u https://github.com/LineageOS/android.git -b lineage-21.0
   repo sync -c -j8
   source build/envsetup.sh
   breakfast X682C
   brunch X682C
   ```
6. Flash (dynamic partitions, use fastbootd):
   ```sh
   fastboot reboot fastboot
   fastboot flash system system.img
   fastboot flash boot boot.img
   fastboot --disable-verity --disable-verification flash vbmeta vbmeta.img
   fastboot reboot
   ```
   Wipe data once when moving from stock.

Fallback if no boot: LineageOS GSI for arm64 A-only (`system.img`) flashed to the
`system` partition in fastbootd, keeping stock vendor/boot.

Gate: boots, RIL, Wi-Fi, camera, audio, sensors, fingerprint, charging.

## 5. Magisk root

After LineageOS boots stably:

1. Extract `boot.img` from the built ROM.
2. Magisk app → Install → Select and Patch a File → `boot.img`.
3. Flash the patched image:
   ```sh
   fastboot flash boot magisk_patched-*.img
   fastboot reboot
   ```
   Or from OrangeFox: `adb sideload Magisk-v27.x.apk` / install zip.
4. Verify: Magisk app shows installed, `su -c id` returns uid 0.
5. Hide/DenyList only after core functions are confirmed.

## Rollback / unbrick

Stock restore path is already saved:
`firmware/X682C-...V366.zip` → SP Flash Tool. V360 + OTA is the fallback.
Keep OrangeFox + stock boot backups too.

## Risks

- `fastboot flashing unlock` may be disabled by Infinix; without it the plan stops.
- MTK BROM may be patched; mtkclient backup may need the test point.
- No official device tree: camera/RIL/audio HAL work is the hard part.
- Latest LineageOS may need a 5.x GKI kernel this device never had; LineageOS 21
  or a GSI is the realistic target.
- Never relock the bootloader with custom firmware installed.
