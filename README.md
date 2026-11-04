# kameo-nx-installer

Version 1.0.0, for **kameo-nx 1.0.0**: Kameo: Elements of Power on the Nintendo Switch (homebrew), by ChanseyIsTheBest.

This page makes the Switch package from **your own copy** of the game. It runs entirely in your browser: your game files are
not uploaded, and none of the game's files come with kameo-nx.

## What you need

- Your **Xbox 360 disc** of Kameo: Elements of Power (NTSC-U or PAL) as an `.iso` image, or the folder it was extracted to,
  with `default.xex` and the `.lvl` files in it.
- **Title update 2** for that disc, its Xbox 360 package: `TU_16L61UI_0000000000000.00000000000G1` (in the update's `6C8AE566`
  folder) for the NTSC-U disc, `TU_16L61UI_000000K000000.00000000000G5` (folder `45BB5521`) for the PAL disc. kameo-nx is
  the updated game, so this is required.
- Optional: the **DLC** packs (Add-On, Design-A-Skin, Power and Winter Warrior).
- A desktop **Chromium browser** (Chrome, Edge, Brave...), about 8 GB of free memory and 7 GB of free disk space for the
  download.
- A Switch that runs homebrew (Atmosphère) with **Sphaira**, and an SD card with at least 8 GB free.

## How to use it

1. Open the page: **https://chanseyisthebest.github.io/kameo-nx-installer/**
2. **Choose your game**: the disc image (`.iso`) or the extracted folder. The page checks that it is the supported version.
3. **Choose title update 2** (and the DLC packs, at the same time, if you have them).
4. Choose **who compiles the shaders**. Leave it on **This page**: see
   [Letting the Switch compile the shaders](#letting-the-switch-compile-the-shaders).
5. Press **Create kameo-nx.zip**. The zip downloads while it is made; keep the page open until it finishes.
6. Extract `kameo-nx.zip` to the **root of the SD card**. It makes `switch/kameo-nx/`.
7. On the Switch, open **Sphaira**, find Kameo: Elements of Power, press **X** to open Options and choose **Install Forwarder**.
   Make sure **Address Space** is set to **39-bit**, choose **Create Forwarder**, then start the game from the **Home Screen**.
   This lets the game use all four CPU cores, which it cannot do through a title takeover. The first start sets this up;
   from the second start on it runs on four cores.

On a PC with 16 threads, the whole build with all the DLC took about 7.5 minutes in a browser, 4.5 of them for the shaders.
The zip is about 6 GB.

To run the page on your own computer: `python serve.py 8193 .` in this folder, then open http://127.0.0.1:8193/.

## Letting the Switch compile the shaders

**Not recommended.** With **The Switch, as you play** the page still makes the game's shaders from your files, but leaves them
for the console to compile, so it finishes sooner. The game then stops each time it first needs a shader, often for minutes in
a new area, and runs slower for a long time afterwards.

## Settings

`switch/kameo-nx/kameo.toml` holds the settings you may want to change, with a comment on each: the language (by default the
Switch's system language), anti-aliasing, dynamic resolution, the frame cap, four-core mode, logs and the controls. Delete it
and the game writes it again at the next start.

## If something goes wrong

- Crash logs are written to `switch/kameo-nx/logs/rex/rex_crash.log`.
- For a bug report, open `kameo.toml`, remove the `#` in front of `log_level = "info"`, play until the problem happens, and send
  the `switch/kameo-nx/logs/` folder.
- The page says the game or the update is not supported: kameo-nx supports the NTSC-U and the PAL Xbox 360 discs, each with
  its own title update 2, and nothing else. The update must be the one of your disc's media ID.

## How it works

The rest of this file is for developers.

The distribution NRO carries none of the game's assets, and none of its shaders but the 139 that no level or model file
holds. The page makes everything else from the player's files:

1. **The shaders' containers**: `py/kameo_dump.py` (kameo-nx's `tools/kameo_files.py`, in [Pyodide](https://pyodide.org)) on the
   levels and models: Rare's CAFF archives, each section one zlib stream. 4,477 containers on the disc, 5,722 with the DLC
   packs, which are read in place (`lib/stfs.js`, `lib/kameo_files.js`).
2. **Renut's translator** (`wasm/renut_hlsl`, kameo-nx's XenosRecomp in WebAssembly, with the version 0x0E containers these
   shaders use): each container's HLSL and the numbers of the NRO's shader table.
3. **GLSL for the console**, on a pool of workers (`glsl_worker.js`): `renut_early_alpha.py` for pixel shaders, DXC,
   SPIRV-Cross, `deko3d_glsl.py` and `deko3d_glsl_opt.py`, kameo-nx's Python tools unchanged in Pyodide.
4. **deko3d_glsl.bin** (`lib/package.js`): the GLSL and the shader table, which the NRO reads next to itself.
5. **deko3d_shaders.bin**: every shader variant of `release/variants.txt`, plus each shader as it is, compiled by uam in
   WebAssembly (`wasm/uam`, the console's compiler). The NRO's own 139 shaders are read out of the NRO (`lib/nro.js`) and
   compiled too. Skipped when the player lets the Switch compile.
6. **Title update 2 and the DLC**: the update's `default.xexp` goes beside `default.xex` (checked against the manifest's
   SHA-256), its language folders to `update/`, and each DLC package whole to `dlc/`.
7. **kameo-nx.zip**, streamed to a download by the service worker (`sw.js`).

The page's DXC is newer (v2025.1) than the native build's, so about a third of the shaders come out with different
temporaries, and their GLSL and DKSH are not the native bytes. Two DLC shaders need SPIRV-Cross to run more recompile passes
with this DXC's SPIR-V (`lib/chain.js`).

## Release files

`release/` is filled by `tools/make_release.py` from a kameo-nx distribution build. `manifest.json` names the supported
`default.xex` and `default.xexp` by their SHA-256 and the SHA-256 of every release file; with `--reference` also those of the
shader files a Node run made. `release/variants.txt` comes from kameo-nx's `tools/deko3d_variant_cache.py --export-variants`.

## Tests (Node 24, from this folder)

| Test | What it checks |
|---|---|
| `test/full_node.mjs <game> <kameo-nx> <out> --nro=<NRO or its GLSL package>` | everything, as the page runs it, with the shader table and caches compared |
| `test/browser.html` (with `python serve.py 8193 . --test-files <game>`) | `worker.js` in a browser, the zip read back |

Outputs of the tests (shader files, zips) are game data: never commit or share them.

## License

GPL-3.0 (see [LICENSE](LICENSE)). Third-party components are listed in [NOTICES.md](NOTICES.md). The page is built on
[renut-nx-webinstaller](https://github.com/ChanseyIsTheBest/renut-nx-webinstaller).

Kameo: Elements of Power is a trademark of Microsoft; the icon artwork is © Microsoft. This project is not affiliated with or
endorsed by Microsoft, Rare or Nintendo.
