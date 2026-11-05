#!/usr/bin/env python3
"""kameo-nx-installer (from renut-nx-webinstaller): fills release/ from a kameo-nx distribution build.

    python tools/make_release.py --nro <distribution NRO> --banjo <kameo-nx root> --xex <the game's default.xex>
        --xexp <title update 2's default.xexp> [--edition <name> <default.xex> <default.xexp> ...]
        [--toml <renut.toml>] [--pipelines <pipeline_list.bin>] [--reference <folder of test/full_node.mjs's output>]

The NRO must be a distribution build (banjo-nx: tools/renut_switch_shader_cache.py --only and
tools/deko3d_shader_package.py --only --raw): it carries none of the game's shaders but the ones the game makes at
runtime. release/ then holds the NRO, its settings and pipeline list, the translator's shader_common.h, and
manifest.json naming each file's SHA-256 and the supported default.xex (its SHA-256 only): --xex and --xexp are the
NTSC-U disc's, and each --edition adds another disc's pair, which the same NRO runs (2026-11-04: the PAL disc, whose
title update 2 is the same build). With --reference, the
SHA-256 of the deko3d_glsl.bin and deko3d_shaders.bin a run of the whole build made (they are the same bytes in every
browser): the page then says whether its own are identical. release/variants.txt is written by banjo-nx's
tools/deko3d_variant_cache.py --export-variants.
"""
import argparse
import hashlib
import json
import os
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--nro', required=True)
    ap.add_argument('--banjo', required=True)
    ap.add_argument('--xex', required=True)
    ap.add_argument('--xexp', required=True)  # 2026-11-01: title update 3's default.xexp (the page checks it)
    ap.add_argument('--edition', nargs=3, action='append', default=[], metavar=('NAME', 'XEX', 'XEXP'))
    ap.add_argument('--toml')
    ap.add_argument('--pipelines')
    ap.add_argument('--reference')
    a = ap.parse_args()
    release = os.path.join(ROOT, 'release')
    os.makedirs(release, exist_ok=True)
    toml = a.toml or os.path.join(a.banjo, 'app', 'kameo_switch.toml')
    pipelines = a.pipelines or os.path.join(a.banjo, 'out', 'kameo_pipeline_list.bin')
    copies = [(a.nro, 'kameo-nx.nro'), (toml, 'kameo.toml'), (pipelines, 'pipeline_list.bin'),
              (os.path.join(a.banjo, 'app', 'thirdparty', 'reblue-XenosRecomp', 'XenosRecomp', 'shader_common.h'),
               'shader_common.h')]
    for src, name in copies:
        shutil.copyfile(src, os.path.join(release, name))
    builds = []
    for edition, xex, xexp in [('Xbox 360 disc, NTSC-U, title update 2', a.xex, a.xexp)] + a.edition:
        build = {
            'edition': edition,
            'xex_sha256': sha256(xex),
            'xexp_sha256': sha256(xexp),
            'nro': 'kameo-nx.nro',
            'nro_sha256': sha256(os.path.join(release, 'kameo-nx.nro')),
            'files': [{'path': name, 'source': name, 'sha256': sha256(os.path.join(release, name))}
                      for name in ('kameo.toml', 'pipeline_list.bin')],
        }
        if a.reference:
            build['deko3d_glsl_sha256'] = sha256(os.path.join(a.reference, 'deko3d_glsl.bin'))
            build['deko3d_shaders_sha256'] = sha256(os.path.join(a.reference, 'deko3d_shaders.bin'))
        builds.append(build)
    with open(os.path.join(release, 'manifest.json'), 'w', encoding='utf-8') as f:
        json.dump({'version': 1, 'builds': builds}, f, indent=2)
        f.write('\n')
    print(json.dumps(builds, indent=2))


if __name__ == '__main__':
    main()
