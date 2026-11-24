# Recovery readiness — Infinix X682C

Updated 2026-11-24. Build `X682C-H694CD-Q-GL-220729V366`.

## Verified

| Item | Evidence |
|---|---|
| Exact full stock ROM | `firmware/X682C-...V366.zip`, SHA256 `ce62372d…`, zip test OK, fingerprints match phone |
| NVRAM / IMEI backup | `backup/mtk-bypass/`, 25 partitions, 872 MB, all SHA256 OK |
| Phone-specific IMEI store | `nvram.bin` / `nvdata.bin` contain `NVD_IMEI`; `proinfo.bin` has serial |
| Boot/recovery dump | SHA256 equals exact V366 `boot.img` / `recovery.img` |
| Secure-BROM bypass | `bypass_utility` → `Protection disabled`, all auth flags off |
| DA read | 872 MB dump completed |
| DA write | exact `logo.bin` written, read back, hash identical |

## Not physically tested

- SP Flash Tool download on this secure unit (mtkclient write is verified).
- Full `super` write.
- NVRAM write-back (identical-data write would verify it; not run).
- Hard brick with no BROM/preloader (needs test point or ISP).

## What this means

**Software brick (bootloop, black screen, BROM/preloader still appears):**
recoverable. Flash exact V366 with SP Flash Tool. If SPFT refuses, bypass +
mtkclient write can restore the partitions. IMEI/NVRAM are backed up.

**IMEI lost / null after a bad flash:** restore `nvram.bin`, `nvdata.bin`,
`nvcfg.bin`, `persist.bin`, `proinfo.bin`, `protect1.bin`, `protect2.bin` from
`backup/mtk-bypass/` through the same bypass + DA path, or with a service tool.

**Hard brick, no USB port at all:** test point / eMMC ISP. The saved NVRAM set
can be written by an ISP-capable shop. Exact ROM alone cannot rebuild IMEI.

## Custom logo warning

A `logo.bin` repacked with `mtklogo` from a PNG caused a boot loop + continuous
vibration on this unit. The exact stock V366 logo was written back and verified
(hash match). Do not flash custom logo images built that way. The failed experiment was removed.

## Honest limit

No phone can be *guaranteed* recoverable from every hardware failure. For
software/firmware bricks on this unit, the exact ROM + verified write path +
NVRAM backup is complete. For a dead eMMC/SoC, only hardware repair applies.
