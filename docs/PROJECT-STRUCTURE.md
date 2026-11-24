# Project structure — Infinix X682C recovery kit

This is the annotated map of the kit. All paths are relative to the repository
root `/home/arnav/Infinix`.

## Design

- `docs/` — every human-readable note, report, manifest, plan, and the agent
  playbook. Only `README.md` stays at root; `AGENTS.md`/`agent.md` are symlinks
  into `docs/` for tooling.
- `scripts/` — every project script. Third-party tools keep their own scripts
  under `tools/`.
- `firmware/` — exact stock packages. Extracted trees are working copies.
- `backup/` — device-unique data. **Private; never commit.**
- `tools/` — vendored third-party recovery tools.
- `docs/AGENTS.md` is the canonical playbook; root `AGENTS.md` and `agent.md`
  are symlinks to it for agent-tool compatibility.

## Top level

```text
Infinix/
├── README.md                    GitHub-facing overview, badges, quick start
├── AGENTS.md                    symlink -> docs/AGENTS.md
├── agent.md                     symlink -> docs/AGENTS.md
├── SHA256SUMS.txt               hashes of top-level artifacts
├── .gitignore                   excludes private data, firmware, venv, logs
├── docs/                        all docs, including AGENTS/LEARN/STRUCTURE
├── scripts/                     project scripts (see below)
├── firmware/                    stock ROM packages and extracted V366
├── backup/                      NVRAM/IMEI set + portable archive
└── tools/                       SPFT, mtkclient, bypass, udev, TWRP
```

| File | Purpose |
|---|---|
| `README.md` | Public overview: device, status, layout, recovery commands, safety, sources. |
| `AGENTS.md` | Symlink to `docs/AGENTS.md` (agent tooling). |
| `agent.md` | Symlink to `docs/AGENTS.md` (lowercase tooling name). |
| `SHA256SUMS.txt` | SHA256 for V366 ZIP, V360 ZIP, OTA ZIP, TWRP image, backup archive. Verify with `sha256sum -c`. |
| `.gitignore` | Blocks private/large artifacts: IMEI, bugreport, `backup/`, firmware ZIPs/extracted trees, venv, caches, logs. |

## `docs/`

| File | Contents |
|---|---|
| `RECOVERY-READINESS.md` | Verified vs untested matrix, what is recoverable, honest hardware limit. |
| `BROM-NOTES.md` | Secure-BROM findings, working bypass steps, DA read/write results, force-off combo. |
| `DEVICE.md` | Device identity, build, SoC, partition map, raw-info index. |
| `V366-info.md` | Exact V366 ROM hashes, fingerprints, package contents, verification. |
| `V360-info.md` | V360 fallback ROM hashes, fingerprints, OTA precondition evidence. |
| `EXACT-V366-RESTORE.md` | Fallback V360 + OTA restore path. |
| `BACKUP-MANIFEST.md` | 25-partition NVRAM/IMEI backup contents, sizes, verification, restore list. |
| `RESEARCH-X682C.md` | Exact-model YouTube, forum, blog, and commercial-tool research. |
| `PLAN-lineageos.md` | Future LineageOS + OrangeFox + Magisk port plan. |
| `AGENTS.md` | Canonical operational playbook: verified state, entry modes, recovery A–E, rules, health checks. |
| `LEARN.md` | Full 20-part course from layman basics to MTK internals, bootloader, recovery, ROMs, root, bootloops, bricks, recovery, causes, glossary, quiz. |
| `PROJECT-STRUCTURE.md` | This annotated inventory. |
| `ota-metadata/` | OTA metadata files (see below). |
| `device-info/` | Raw live-device dump (see below). |

### `docs/ota-metadata/`

| File | Contents |
|---|---|
| `ota-v366-metadata.txt` | Official OTA pre/post build fingerprints, patch, timestamp, block type. |
| `ota-v366-dynamic_partitions_op_list.txt` | Dynamic partition resize operations used by the OTA. |

### `docs/device-info/`

| File | Contents |
|---|---|
| `identifiers.txt` | Serial + IMEI. **Private**, mode 600, gitignored. |
| `identifiers-props.txt` | Identifier-related properties. |
| `props-full.txt` | Full `getprop` dump. |
| `props-key.txt` | Build/product/boot properties. |
| `block-by-name.txt` | Partition symlinks from `/dev/block/by-name`. |
| `partition-map.txt` | Offset/size map from V360/V366 scatter. |
| `cpuinfo.txt`, `thermal.txt` | CPU and thermal data. |
| `kernel-system.txt` | Kernel version, cmdline attempt, memory. |
| `display-battery-storage.txt` | Display, battery, filesystems. |
| `packages.txt`, `packages-thirdparty.txt` | Installed packages. |
| `gms.txt`, `secure-settings.txt`, `connectivity.txt`, `telephony.txt`, `misc-sys.txt` | Service/settings snapshots. |
| `bugreport-2026-11-24.zip` | Android bugreport archive. |

## `scripts/`

| Script | Purpose | State |
|---|---|---|
| `dump-nvram.py` | Connect post-bypass, upload DA, read 25 GPT partitions into `backup/mtk-bypass/`, write SHA256SUMS. | Tested; produced 872 MB. |
| `verify-write.py` | Post-bypass write of exact `logo.bin`, read back, compare SHA256. Template for other partition writes. | Tested; `WRITE VERIFIED`. |
| `backup-critical.sh` | Pre-bypass mtkclient loop for NVRAM/proinfo/persist/boot. Kept as reference. | Blocked by secure BROM without bypass. |

Both Python scripts compute `ROOT` as the parent of `scripts/`, so they work from
any current directory while the kit stays at `/home/arnav/Infinix`.

## `firmware/`

| Path | Size | Purpose |
|---|---:|---|
| `X682C-H694CD-Q-GL-220729V366.zip` | 2.8 GB | Exact full factory ROM. Primary unbrick package. |
| `V366/X682C-H694CD-Q-GL-220729V366(MobiFirmware.com)/` | 4.9 GB | Extracted V366 working copy. |
| `X682C-H694CD-Q-GL-220510V360.zip` | 3.2 GB | Previous full build. Fallback only. |
| `OTA-V360-to-V366-a6abd9a8.zip` | 238 MB | Official signed OTA from V360 to V366. Fallback only. |

### Extracted V366 package

| File | Purpose |
|---|---|
| `MT6768_Android_scatter.txt` | SP Flash Tool scatter layout for X682C. |
| `super.img` | Raw dynamic-partition image (system/vendor/product), 4.7 GB. |
| `boot.img`, `boot-adb.img` | Boot images. |
| `recovery.img` | Stock recovery. |
| `preloader_x682c_h694.bin`, `preloader.img`, `preloader_emmc.img` | Preloader variants; flash only if needed. |
| `lk.img`, `dtbo.img`, `logo.bin` | Boot chain / splash; `lk.img` is written to both `lk` and `lk2`. |
| `md1img.img`, `MDDB...EDB`, `APDB...` | Modem firmware and database. |
| `vbmeta*.img`, `tee.img`, `scp.img`, `sspm.img`, `spmfw.img`, `tkv.img`, `tranfs.img` | Verified boot / firmware components. |
| `PGPT`, `ota_scatter.txt`, `ota_update_list.txt`, `android-info.txt` | Partition / OTA layout metadata. |
| `Checksum.ini`, `SHA256SUMS.txt` | Factory checksums and local extracted-file hashes. |
| `cache.img`, `userdata.img` | Blank/minimal data images. |
| `kernel`, `efuse_MT6768.xml`, `installed-files-*` | Build metadata. |

Ad/log junk and `.url` files were removed from the extracted copy. The ZIP is
kept unchanged as the downloaded artifact.

## `backup/`

### `backup/mtk-bypass/`

25 device-unique partitions, 872 MB. All entries pass
`sha256sum -c SHA256SUMS.txt`.

| Group | Files | Why |
|---|---|---|
| IMEI / radio | `nvram.bin`, `nvdata.bin`, `nvcfg.bin`, `md1img.bin`, `md_udc.bin` | IMEI store, modem config/firmware. |
| Calibration / DRM | `persist.bin`, `proinfo.bin`, `protect1.bin`, `protect2.bin` | Sensors, Wi-Fi/BT, product info, protected calibration. |
| Security / FRP | `seccfg.bin`, `frp.bin` | Lock state and FRP. Do not write casually. |
| Boot / splash | `boot.bin`, `recovery.bin`, `dtbo.bin`, `lk.bin`, `lk2.bin`, `logo.bin` | Exact current boot chain. |
| Misc | `misc.bin`, `boot_para.bin`, `expdb.bin`, `metadata.bin`, `para.bin`, `flashinfo.bin`, `tkv.bin`, `tranfs.bin` | Logs/state/transfer data. |

### `backup/X682C-unique-backup-2026-11-24.tar.zst`

Portable archive of `backup/mtk-bypass/`, 64 MB compressed. Its `.sha256` file
is next to it. **Private.**

## `tools/`

| Path | Purpose |
|---|---|
| `SP_Flash_Tool_v5.2228_Linux/` | MediaTek SP Flash Tool, Linux x64, bundled DA and libs. Entry: `SP_Flash_Tool_v5.2228_Linux/SP_Flash_Tool_v5.2228_Linux/flash_tool.sh`. |
| `mtkclient/` | mtkclient source + Python venv with pyusb/crypto/capstone/keystone/unicorn. Entry: `.venv/bin/python mtk.py`. |
| `bypass_utility/` | Open-source MTK SLA/DAA bypass. `main.py`, `default_config.json5`, mt6768 payload. |
| `exploits_collection/` | Upstream payloads used by `bypass_utility`. |
| `udev/` | `50-android.rules`, `51-edl.rules`, `52-mtk.rules`, `99-ttyacms.rules`. |
| `x682c-twrp.img` | Unofficial TWRP image, reference for the future OrangeFox port. |

Third-party trees retain their upstream licenses; `.git` metadata and caches
were removed. The Python venv is local to this path and is gitignored.

## Generated / private vs source

- **Generated at runtime:** `backup/mtk-bypass/*.bin`, `SHA256SUMS.txt`,
  `scripts/__pycache__/`, mtkclient `.state`/`hwparam.json`.
- **Private:** `docs/device-info/identifiers.txt`, bugreport, all of `backup/`.
- **Do not edit:** ZIPs, extracted stock images, `firmware/V366/.../SHA256SUMS.txt`.
- **Safe to edit:** `README.md`, `docs/*` (including `docs/AGENTS.md`, except private data),
  `scripts/*`, `.gitignore`.

## Verification

```sh
cd /home/arnav/Infinix
sha256sum -c SHA256SUMS.txt
cd backup/mtk-bypass && sha256sum -c SHA256SUMS.txt

cd /home/arnav/Infinix
tools/mtkclient/.venv/bin/python -m py_compile \
  scripts/dump-nvram.py scripts/verify-write.py
```
