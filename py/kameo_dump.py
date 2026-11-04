"""kameo-nx-installer: kameo-nx's tools/kameo_files.py on one game file, the page holding the file. Kameo keeps almost all of its
shaders in its levels and models, Rare's CAFF 28.01.05.0031 archives: each section is one zlib stream (the format as
Kameo: RePowered's tools/modkit/kameo_modkit/caff.py, MaxDeadBear and BiRabittoh, MIT, reads it). Every section is unpacked
and scanned for version 0x0E shader containers, whole and valid by zuma-nx's container_0e.h rule.

dump_file(path) -> (list of (kind, blob), list of problems), as reNut's dump_shaders.py gives them in banjo-nx-installer.
"""
import re
import struct
import zlib

MAGIC = re.compile(rb'\x10\x2a\x0e[\x00\x01]', re.S)


def sections(blob):
    """(name, unpacked bytes) of a CAFF archive."""
    if blob[:4] != b'CAFF':
        return
    cursor = struct.unpack_from('>I', blob, 0x38)[0]
    for i in range(blob[0x3D]):
        base = 0x40 + 40 * i
        name = blob[base:base + 8].rstrip(b'\0').decode('latin-1')
        values = struct.unpack_from('>8I', blob, base + 8)
        packed = values[7]
        if packed:
            yield name, zlib.decompress(blob[cursor:cursor + packed])
            cursor += packed


def containers(data):
    """Each valid container in data: any byte offset."""
    for m in MAGIC.finditer(data):
        o = m.start()
        if o + 0x18 > len(data):
            continue
        flags, virt, phys, defs, consts, info = struct.unpack_from('>6I', data, o)
        if not (0x18 <= virt < 0x10000 and 0 < phys < 0x100000 and o + virt + phys <= len(data)):
            continue
        if defs >= virt or consts >= virt or not 0x18 <= info < virt:
            continue
        yield data[o:o + virt + phys]


def dump_bytes(blob):
    results, problems = [], []
    try:
        for _, data in sections(blob):
            for shader in containers(data):
                results.append(('vs' if shader[3] & 1 else 'ps', bytes(shader)))
    except (zlib.error, struct.error) as e:
        problems.append(str(e))
    return results, problems


def dump_file(path):
    with open(path, 'rb') as f:
        return dump_bytes(f.read())
