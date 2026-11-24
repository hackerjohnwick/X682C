# X682C V366 full factory package — verification

**This is the exact build currently on the phone.**

Source: MediaFire `quickkey 6kto8gp7xjeix7d`, file
`X682C-H694CD-Q-GL-220729V366(MobiFirmware.com).zip`, uploaded 2022-12-15.
Resolved from the MobiFirmware free mirror; the MediaFire page needed a real
browser to pass Cloudflare, then the CDN link was downloaded with aria2c.

| Check | Result |
|---|---|
| Size | 2,967,499,850 bytes — matches MediaFire API |
| SHA256 | `ce62372d4e3f4cce49b9a929c0b6b5ead0eb18f910a0071918edb891d92c2603` — matches MediaFire `hash` |
| MD5 | `aa0ca67b8ea1ad0c8bf5e25dfd0aef87` |
| ZIP test | `unzip -t`: No errors detected |
| Contents | 45 files in the zip, 5,158,470,119 bytes uncompressed; ad/log junk removed from extracted copy |
| Board | `android-info.txt` → `board=Infinix-X682C` |
| Scatter | `MT6768_Android_scatter.txt`, project `x682c_h694`, MT6768 |
| Built with | `Checksum.ini` → `TOOL=v5.2128.02`, Change_ID 1659111954 |
| Build date | 2022-07-29 |
| Security patch | 2022-07-05 |

## Fingerprints (read from `super.img`)

```
ro.product.build.fingerprint = Infinix/X682C-GL/Infinix-X682C:10/QP1A.190711.020/220729V366:user/release-keys
ro.vendor.build.fingerprint  = Infinix/X682C-GL/Infinix-X682C:10/QP1A.190711.020/220729V302:user/release-keys
ro.system.build.fingerprint  = Infinix/TSSI/FULL-64:10/QP1A.190711.020/220729V280:user/release-keys
ro.build.display.id          = X682C-H694CD-Q-GL-220729V366
```

These match the connected phone exactly (`ro.build.fingerprint` V366,
`ro.vendor.build.fingerprint` V302, `ro.system.build.fingerprint` V280).

## Package contents

`preloader_x682c_h694.bin`, `boot.img`, `boot-adb.img`, `recovery.img`,
`dtbo.img`, `lk.img`, `logo.bin`, `md1img.img`, `super.img` (4.7 GB raw),
`cache.img`, `userdata.img`, `vbmeta*.img`, `APDB`, `MDDB`, `PGPT`, scatter,
`Checksum.ini`.

## Use

Extracted files are covered by
`../firmware/V366/X682C-H694CD-Q-GL-220729V366(MobiFirmware.com)/SHA256SUMS.txt`.

Primary unbrick package:

1. SP Flash Tool → `MT6768_Android_scatter.txt`.
2. **Download Only** first. Preloader optional; tick it only if the preloader is
   broken.
3. Flash, boot, verify `adb shell getprop ro.build.display.id`.

`V360` + OTA pair is kept only as a fallback. It is no longer needed for the
exact-build restore.
