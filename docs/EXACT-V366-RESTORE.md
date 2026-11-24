# Restore the exact current build: 220729V366

**Primary:** flash `X682C-H694CD-Q-GL-220729V366.zip` directly with SP Flash Tool.
It is the exact signed factory package; no OTA step is needed.

**Fallback:** this document's two-file path, if the V366 ZIP is damaged.

Fallback files:

1. `X682C-H694CD-Q-GL-220510V360.zip` — full stock base (V360).
2. `OTA-V360-to-V366-a6abd9a8.zip` — official OTA from V360 to the exact
   build the phone runs today (V366, security patch 2022-07-05).

## Steps

1. Extract V360, then flash it with SP Flash Tool:
   ```sh
   mkdir -p firmware/V360
   unzip firmware/X682C-H694CD-Q-GL-220510V360.zip -d firmware/V360
   ```
   - scatter: `firmware/V360/MT6768_Android_scatter.txt`
   - mode: **Download Only** (does not touch NVRAM/IMEI)
   - connect the powered-off phone, wait for the green check.
2. Let it boot once (first boot is slow). Do **not** set up accounts yet.
3. Reboot to **stock recovery**: `adb reboot recovery`, or hold **Vol Up +
   Power** while off.
4. In stock recovery choose **Apply update from ADB**, then:
   ```sh
   adb sideload OTA-V360-to-V366-a6abd9a8.zip
   ```
   Alternative: copy the OTA to a microSD, choose **Apply update from SD card**.
5. Reboot. Verify:
   ```sh
   adb shell getprop ro.build.display.id
   # X682C-H694CD-Q-GL-220729V366
   adb shell getprop ro.build.version.security_patch
   # 2022-07-05
   ```

## If sideload aborts

- `E3001` fingerprint mismatch: the phone is not on a build the OTA expects.
  Reflash V360 and retry. If it still fails, boot V360 Android and use
  Settings → Software Update; the phone downloads the OTA that matches its own
  installed build.
- `E3005` partition contents unexpected: one of boot/md1img/system/vendor/product
  is modified. Reflash V360 with **Firmware Upgrade**, then retry.
- Signature error: this OTA must be applied from **stock recovery**, not
  OrangeFox/TWRP.
- If OTA still fails, boot Android on V360 and use Settings → Software Update;
  the phone picks the same official package.

This fallback pair is verified against the OTA metadata and updater script.
A free full V366 factory ZIP was found later and is now the primary restore
(`V366-info.md`); this path remains only as a fallback.
