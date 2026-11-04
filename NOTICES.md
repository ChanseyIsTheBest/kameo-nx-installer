# Third-party notices

kameo-nx-installer is built on [renut-nx-webinstaller](https://github.com/ChanseyIsTheBest/renut-nx-webinstaller) (GPL-3.0).

| Component | Where | License |
|---|---|---|
| [bejeweled3-nx-installer](https://github.com/ChanseyIsTheBest/bejeweled3-nx-installer), [sa2-nx-installer](https://github.com/ChanseyIsTheBest/sa2-nx-installer) and peggle2-nx by ChanseyIsTheBest: this page's starting point (the worker, the zip writer, the raw zstd frames of the GLSL package, the translator's front end, the test server) | `worker.js`, `app.js`, `lib/zip.js`, `lib/package.js`, `wasm/src/translator/`, `serve.py` | GPL-3.0 |
| [nfsmw-nx-installer](https://github.com/StevensND/nfsmw-nx-installer) by StevensND: the download service worker and the worker's download stream (through bejeweled3-nx-installer), the zip writer | `sw.js`, `worker.js`, `lib/zip.js` | GPL-3.0 |
| keflings-nx-installer (a fork of this installer, for A Kingdom for Keflings): the Xbox 360 STFS package reader (itself a port of sa2-nx's tools/stfs_extract.py) and the way the title update and DLC packages are mapped into the zip | `lib/stfs.js`, `lib/kameo_files.js` | GPL-3.0 |
| kameo-nx's shader tools (from banjo-nx), run unchanged in Pyodide: `tools/deko3d_glsl.py`, `tools/deko3d_glsl_opt.py` (and its shader lists), `tools/early_alpha.py`, `tools/renut_early_alpha.py` | `py/` | GPL-3.0 |
| [reNut](https://github.com/masterspike52/reNut) by masterspike52: the renderer whose shader chain this page runs, reused with its author's permission | throughout the chain | as its repository states |
| [Kameo: RePowered](https://github.com/MaxDeadBear/KameoRePowered) by MaxDeadBear and BiRabittoh: the CAFF archive layout `py/kameo_dump.py` reads, through kameo-nx's `tools/kameo_files.py` | `py/kameo_dump.py` | MIT |
| XenosRecomp ([hedge-dev](https://github.com/hedge-dev/XenosRecomp) and contributors), in reNut's version as kameo-nx carries it | `wasm/renut_hlsl.*`, `release/shader_common.h` | MIT |
| [uam](https://github.com/devkitPro/uam) by fincs (with Mesa's GLSL compiler and the nouveau codegen in `mesa-imported/`), with SwitchWakerHD's patches and banjo-nx's passes, as banjo-nx's `app/thirdparty/uam` | `wasm/uam.*`, `wasm/src/uam/` | uam: zlib License; Mesa: MIT and others (see its sources) |
| [DirectXShaderCompiler](https://github.com/microsoft/DirectXShaderCompiler) v2025.1 with SPIRV-Tools and SPIRV-Headers, and the `dxc_web.cpp` wrapper, as built by nfsmw-nx-installer (from bejeweled3-nx-installer) | `wasm/dxc_web.*` | NCSA (LLVM); SPIRV-Tools: Apache-2.0; SPIRV-Headers: MIT; the wrapper: GPL-3.0 |
| [SPIRV-Cross](https://github.com/KhronosGroup/SPIRV-Cross) (commit `22b22f56`), unmodified (from bejeweled3-nx-installer) | `wasm/spirv_cross.*` | Apache-2.0 |
| [Pyodide](https://pyodide.org) 0.27.7 (CPython 3.12 for WebAssembly) and its numpy 2.0.2 wheel, unmodified | `vendor/pyodide/` | Pyodide: MPL-2.0; CPython: PSF License; numpy: BSD-3-Clause |
| [xxHash](https://github.com/Cyan4973/xxHash) and [{fmt}](https://github.com/fmtlib/fmt), in the translator | `wasm/renut_hlsl.*` | BSD-2-Clause; MIT |
| [Emscripten](https://emscripten.org) 6.0.11 runtime and the musl libc it links | `wasm/*.mjs`, `wasm/*.wasm` | MIT and NCSA |

`wasm/uam.*` is built by `wasm/src/uam/build_wasm_uam.sh` and `wasm/renut_hlsl.*` by
`wasm/src/translator/build_wasm_translator.sh` (Emscripten 6.0.11) from the kameo-nx sources.

The licenses of the software in the NRO are listed in kameo-nx's repository, with its source code.
