"""The site's icon: an orange square, half the icon's width, centered.

Browsers ask for /favicon.ico before they read any <link>, and Safari does not use an SVG icon
at all, so the square is also written as PNGs and an ICO that holds them. Nothing here needs an
imaging library: a solid square is a few rows of pixels and zlib.
"""

from __future__ import annotations

import struct
import zlib

ORANGE = (0xFB, 0x9D, 0x61)


def png(size: int, *, background: tuple[int, int, int] | None = None) -> bytes:
    """A `size` square icon with the orange square (half the width) centered in it.

    Transparent unless `background` is given. The touch icon needs one: iOS fills a transparent
    touch icon with black.
    """
    inner = size // 2
    start = (size - inner) // 2
    rows = []
    for y in range(size):
        row = bytearray([0])
        for x in range(size):
            inside = start <= x < start + inner and start <= y < start + inner
            if inside:
                row += bytes((*ORANGE, 255))
            elif background:
                row += bytes((*background, 255))
            else:
                row += bytes((0, 0, 0, 0))
        rows.append(bytes(row))
    raw = b"".join(rows)

    def chunk(kind: bytes, body: bytes) -> bytes:
        crc = zlib.crc32(kind + body) & 0xFFFFFFFF
        return struct.pack(">I", len(body)) + kind + body + struct.pack(">I", crc)

    header = struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header)
            + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


def ico(sizes: tuple[int, ...] = (16, 32, 48)) -> bytes:
    """An ICO file holding PNG images, which every current browser reads."""
    images = [png(s) for s in sizes]
    offset = 6 + 16 * len(sizes)
    directory = b""
    for s, data in zip(sizes, images, strict=True):
        directory += struct.pack("<BBBBHHII", s, s, 0, 0, 1, 32, len(data), offset)
        offset += len(data)
    return struct.pack("<HHH", 0, 1, len(sizes)) + directory + b"".join(images)
