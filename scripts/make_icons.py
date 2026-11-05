"""Draws the app icons (a dam holding back balls) with the standard library only."""
import math
import random
import struct
import zlib

GROUND = (13, 34, 41)
DEEP = (8, 24, 32)
CONCRETE = (184, 177, 162)
BALL = (255, 194, 61)


def build_shapes():
    random.seed(7)
    balls = []
    # Pile behind the dam, kept inside the central safe zone used by masked icons.
    for row in range(4):
        for col in range(9 - (row % 2)):
            balls.append((0.2 + col * 0.075 + (row % 2) * 0.0375, 0.455 - row * 0.065, 0.036))
    # Balls escaping through the gap.
    for x, y, r in [(0.5, 0.56, 0.036), (0.45, 0.63, 0.03), (0.56, 0.67, 0.03), (0.5, 0.75, 0.034), (0.41, 0.74, 0.026), (0.6, 0.77, 0.026)]:
        balls.append((x, y, r))
    return balls


def color_at(x, y, balls):
    color = GROUND if y > 0.5 else DEEP
    for bx, by, r in balls:
        if (x - bx) ** 2 + (y - by) ** 2 <= r * r:
            return BALL
    in_wall = 0.49 <= y <= 0.54 and not 0.45 <= x <= 0.55
    return CONCRETE if in_wall else color


def render(size, balls, samples=3):
    rows = []
    for py in range(size):
        row = bytearray([0])
        for px in range(size):
            total = [0, 0, 0]
            for sy in range(samples):
                for sx in range(samples):
                    c = color_at((px + (sx + 0.5) / samples) / size, (py + (sy + 0.5) / samples) / size, balls)
                    for i in range(3):
                        total[i] += c[i]
            row += bytes(t // (samples * samples) for t in total)
        rows.append(bytes(row))
    return b''.join(rows)


def write_png(path, size, raw):
    def chunk(tag, data):
        body = tag + data
        return struct.pack('>I', len(data)) + body + struct.pack('>I', zlib.crc32(body))
    header = struct.pack('>IIBBBBB', size, size, 8, 2, 0, 0, 0)
    with open(path, 'wb') as f:
        f.write(b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', header) + chunk(b'IDAT', zlib.compress(raw, 9)) + chunk(b'IEND', b''))


shapes = build_shapes()
for size in (192, 512):
    write_png(f'web/icon-{size}.png', size, render(size, shapes))
