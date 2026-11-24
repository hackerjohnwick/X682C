# X682C device-unique backup — 2026-11-24

Source: connected Infinix X682C, build `X682C-H694CD-Q-GL-220729V366`,
Android 10, MT6768, secure BROM.

Method:
1. `tools/bypass_utility` — `Protection disabled` (DAA/SLA off).
2. `scripts/dump-nvram.py` — mtkclient DA read of the GPT partitions.

Result: 25 partitions, 872 MB. Verify with:

```sh
cd backup/mtk-bypass
sha256sum -c SHA256SUMS.txt
```

## Contents

| File | Size | Why it matters |
|---|---|---|
| `nvram.bin` | 64 MB | IMEI / radio NVRAM (contains `NVD_IMEI`) |
| `nvdata.bin` | 64 MB | modem data / IMEI store |
| `nvcfg.bin` | 32 MB | NV config |
| `persist.bin` | 48 MB | sensors, Wi-Fi/BT calibration, DRM |
| `proinfo.bin` | 3 MB | product info; contains serial `REDACTED (private)` |
| `protect1.bin`, `protect2.bin` | 8 MB each | protected calibration |
| `seccfg.bin` | 8 MB | secure config / lock state |
| `frp.bin` | 1 MB | FRP state |
| `boot.bin`, `recovery.bin` | 32 MB each | exact current images |
| `dtbo.img`, `lk.bin`, `lk2.bin`, `logo.bin` | — | boot chain / splash |
| `md1img.bin`, `md_udc.bin` | 128 MB / 23 MB | modem firmware |
| `misc.bin`, `boot_para.bin`, `expdb.bin`, `metadata.bin`, `para.bin`, `flashinfo.bin`, `tkv.bin`, `tranfs.bin` | — | misc / logs / transfer |

## Verification

- `sha256sum -c SHA256SUMS.txt`: **all OK**
- `boot.bin` SHA256 = exact V366 package `boot.img`
  `ff563d7084f0fbe099056fd805cc9c4826f23eee3d72e872104992bb55c5addd`
- `recovery.bin` SHA256 = exact V366 package `recovery.img`
  `445b0b302022e1f8948ddbbd60ebf802e91db21366a430ecf8f72dca6e39de58`
- `nvram.bin` / `nvdata.bin` contain `NVD_IMEI` paths and non-zero data
- `proinfo.bin` contains the phone serial
- Write path verified separately: exact V366 `logo.bin` written and read back
  with matching SHA256 (`scripts/verify-write.py`)

Private data. Do not upload or share. Keep a copy on another disk.

## Restore

This set is the safety net, not the first-line flash. First-line unbrick is the
exact V366 factory package with SP Flash Tool (`firmware/V366/`).

If NVRAM/IMEI is lost after a bad flash, these are the partitions to write back
with mtkclient after the bypass, or with a service tool/ISP.
