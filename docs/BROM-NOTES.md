# BROM / auth notes — X682C

Tested 2026-11-24 on the connected unit.

## Dump succeeded

`dump-nvram.py` completed a 25-partition read in one DA session:

```
DAXFlash - Successfully uploaded stage 2
DAXFlash - DA SLA is disabled
...
done: /home/arnav/Infinix/backup/mtk-bypass
```

872 MB, `sha256sum -c` passes. `boot.bin` / `recovery.bin` hash-match the exact
V366 package. `nvram.bin` + `nvdata.bin` contain `NVD_IMEI`; `proinfo.bin`
contains the serial.

## Write path verified

`verify-write.py` wrote the exact V366 `logo.bin` (2,181,680 bytes) through the
DA and read it back:

```
image sha256: b71c9952fed54d6704bc385f1354509f4f91248cbf9dcb733944e77ab27ea625
read  sha256: b71c9952fed54d6704bc385f1354509f4f91248cbf9dcb733944e77ab27ea625
WRITE VERIFIED
```

So read **and** write both work after the bypass. The same DA path can restore
`boot`, `recovery`, `super` and the NVRAM set.

## Remaining verification

- SP Flash Tool download path: still untested on this secure unit. mtkclient
  write is verified as the fallback.
- Full `super` write and NVRAM restore were not run (would be destructive).

## Current state

The phone booted normally after the tests. BROM is only used for read/write
sessions. Force-off combo confirmed on this unit: **Power + Volume Up** (Power
alone for 30 s did not stop a boot loop). To boot normally, press Power once.

## Secure BROM before bypass

`adb reboot edl` brings up **preloader** (`0e8d:2000`), then it resets.
mtkclient `crash` reaches **BROM** (`0e8d:0003`):

```
HW code:        0x707
Target config:  0xe5
SBC enabled:    True
SLA enabled:    False
DAA enabled:    True
Mem read auth:  True
Mem write auth: True
Cmd 0xC8 blocked: True
Auth file is required. Use --auth option.
```

Without an Infinix auth file, `printgpt`/`r` failed with handshake errors.

## Bypass tested — works

`tools/bypass_utility/main.py` was run from the normal Ubuntu kernel, no FireISO:

```
Device hw code: 0x707
Device secure boot: True
Device serial link authorization: False
Device download agent authorization: True
Found device in preloader mode, trying to crash...
Found device = 0e8d:0003
Disabling watchdog timer
Disabling protection
Protection disabled
```

After that, `mtkclient gettargetconfig` reported:

```
Target config: 0x0
SBC enabled: False
SLA enabled: False
DAA enabled: False
Mem read auth: False
Mem write auth: False
Cmd 0xC8 blocked: False
```

So the open-source bypass **does work on this exact unit**. No auth file is
needed after it.

## Next clean procedure (for another dump)

1. Hold Power 15–20 s → Android.
2. Run:
   ```sh
   cd /home/arnav/Infinix/tools/bypass_utility
   adb reboot edl
   ../mtkclient/.venv/bin/python main.py
   ```
3. When it prints `Protection disabled`, **immediately** run:
   ```sh
   /home/arnav/Infinix/tools/mtkclient/.venv/bin/python \
     /home/arnav/Infinix/scripts/dump-nvram.py
   ```
4. Do not run `gettargetconfig` or any other mtkclient command between the
   bypass and the dump; the BROM window is short.

Do not disconnect between bypass and dump.

## Other routes

- Service tool with Infinix auth: TFM Tool Pro MTK, Hydra, CM2MT2, EFT Pro,
  Griffin-Unlocker (all list `X682C Hot 10 (Auth)`).
- eMMC ISP / test point: Medusa, Easy JTAG, UFI Box. Bypasses SoC auth.
- Do not download random `auth_sv5.auth` files; signed per security version.

## Flashing implication

SP Flash Tool may still flash because it uses its own signed DA. Test it on a
non-critical partition only after a full backup exists; never run **Format All**
on this secure unit.
