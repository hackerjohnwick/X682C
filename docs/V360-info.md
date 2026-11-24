# X682C V360 factory package — verification

Source: AndroidFileHost `?fid=15664248565197182288` (uploader XDO-ID).
Downloaded 2026-11-24 with aria2c, 16 connections.

| Check | Result |
|---|---|
| Size | 3,402,051,113 bytes (matches HTTP Content-Length) |
| MD5 | `a2b85f3a7c97800258edd610843452a1` — matches AFH listing |
| SHA256 | `ac92e5755e5f279476f8aaff6e89a298c903f742a3c1594bb3364cf5735c5fec` |
| ZIP test | `unzip -t`: No errors detected |
| Board | `android-info.txt` → `board=Infinix-X682C` |
| Scatter | `MT6768_Android_scatter.txt`, project `x682c_h694`, platform MT6768 |
| Built with | `Checksum.ini` → `TOOL=v5.2128.02`, Change_ID 1652181570 |
| Target fingerprint | `Infinix/X682C-GL/Infinix-X682C:10/QP1A.190711.020/220510V360:user/release-keys` |
| Vendor fingerprint | `.../220510V299:user/release-keys` (read from `super.img`) |
| System | Android 10, SDK 29, security patch 2022-05-05 |
| `super.img` | Android sparse, 5,452,732,436 bytes raw |
| Contents | 41 files: preloader, APDB, MDDB, PGPT, boot, recovery, dtbo, lk, logo, super, vbmeta*, userdata, scatter |

## Why the V366 OTA accepts this package

`META-INF/com/google/android/updater-script` allows these current fingerprints:

- `Infinix/X682C-GL/Infinix-X682C:10/QP1A.190711.020/220510V299:user/release-keys`
- `Infinix/X682C-GL/Infinix-X682C:10/QP1A.190711.020/220729V302:user/release-keys`

V360's **vendor** fingerprint is V299 (verified above), and the V360 recovery
ramdisk (`prop.default`, `default.prop`) also reports V299 for
`ro.vendor/product/system/bootimage.build.fingerprint`. Stock recovery therefore
matches the first allowed precondition. The second (V302) covers devices whose
vendor was already updated. The OTA's metadata explicitly lists the pre-build as
V360, so this is the intended predecessor package.

Target (from `META-INF/com/android/metadata`):

```
post-build=Infinix/X682C-GL/Infinix-X682C:10/QP1A.190711.020/220729V366:user/release-keys
post-build-incremental=220729V366
post-security-patch-level=2022-07-05
ota-type=BLOCK
```

## Partition caution

Partitions with `file_name: NONE` in the scatter: `pgpt, boot_para, proinfo,
para, expdb, frp, metadata, md_udc, nvcfg, nvdata, persist, protect1, protect2,
seccfg, nvram, otp, flashinfo, sgpt`.

SP Flash Tool **Download Only** skips them. **Format All + Download** erases
them, including IMEI/calibration. Always keep the mtkclient backup.
