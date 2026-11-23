#!/usr/bin/env python3
"""The World Today -- Sunday 23 November 2026.

A one-image newspaper front page summing up the day's world news, drawn
from scratch with the Python standard library only (no Pillow, no numpy):
a tiny framebuffer, a hand-made 5x7 bitmap font and a minimal PNG writer.

The picture is deterministic: the same script always writes the same bytes.

Run locally:
    MAKEFUN_OUTPUT_DIR=out python3 main.py
In the grader the program writes /output/entry.png (MAKEFUN_OUTPUT_DIR
or /output, like the kit starter).

News sources for this edition (23 November 2026, as reported that morning):
Arab News front page (Bahrain demands UN action), Dunya News 02:00 headlines,
Jagran Josh / Observer Voice school-assembly roundups, and wire reports.
"""

import os
import struct
import zlib

W = 1024
H = 1024

PAPER = (247, 242, 232)
INK = (18, 18, 18)
RED = (178, 28, 28)
NAVY = (26, 48, 82)
SEA = (31, 68, 96)
DUSK = (201, 84, 44)
DUSK_DEEP = (146, 44, 40)
SUN = (247, 201, 72)
SMOKE = (112, 112, 112)
SMOKE_LIGHT = (150, 150, 150)
GREY = (110, 108, 100)

# ---------------------------------------------------------------- font
# 5 wide, 7 tall. '#' is ink, '.' is blank. Uppercase, digits and the
# punctuation this page needs.
FONT = {
    'A': (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    'B': ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    'C': (".####", "#....", "#....", "#....", "#....", "#....", ".####"),
    'D': ("####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."),
    'E': ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    'F': ("#####", "#....", "#....", "####.", "#....", "#....", "#...."),
    'G': (".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."),
    'H': ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    'I': ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"),
    'J': ("..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."),
    'K': ("#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"),
    'L': ("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
    'M': ("#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"),
    'N': ("#...#", "##..#", "##..#", "#.#.#", "#..##", "#..##", "#...#"),
    'O': (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    'P': ("####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
    'Q': (".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"),
    'R': ("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
    'S': (".####", "#....", "#....", ".###.", "....#", "....#", "####."),
    'T': ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    'U': ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    'V': ("#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    'W': ("#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"),
    'X': ("#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"),
    'Y': ("#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."),
    'Z': ("#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"),
    '0': (".###.", "#..##", "#.#.#", "#.#.#", "##..#", "#...#", ".###."),
    '1': ("..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."),
    '2': (".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"),
    '3': ("####.", "....#", "....#", ".###.", "....#", "....#", "####."),
    '4': ("...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."),
    '5': ("#####", "#....", "####.", "....#", "....#", "#...#", ".###."),
    '6': (".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."),
    '7': ("#####", "....#", "...#.", "...#.", "..#..", "..#..", "..#.."),
    '8': (".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."),
    '9': (".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."),
    ' ': (".....", ".....", ".....", ".....", ".....", ".....", "....."),
    '.': (".....", ".....", ".....", ".....", ".....", ".##..", ".##.."),
    ',': (".....", ".....", ".....", ".....", ".##..", ".##..", ".#..."),
    ':': (".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."),
    ';': (".....", ".##..", ".##..", ".....", ".##..", ".##..", ".#..."),
    "'": ("..#..", "..#..", ".#...", ".....", ".....", ".....", "....."),
    '-': (".....", ".....", ".....", ".###.", ".....", ".....", "....."),
    '/': ("....#", "....#", "...#.", "..#..", ".#...", "#....", "#...."),
    '&': (".##..", "#..#.", "#..#.", ".#...", "#.#.#", "#..#.", ".##.#"),
    '!': ("..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."),
    '?': (".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."),
    '%': ("#...#", "#..#.", "...#.", "..#..", ".#...", "#..#.", "#...#"),
    '+': (".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."),
    '=': (".....", ".....", "#####", ".....", "#####", ".....", "....."),
    '(': ("...#.", "..#..", ".#...", ".#...", ".#...", "..#..", "...#."),
    ')': (".#...", "..#..", "...#.", "...#.", "...#.", "..#..", ".#..."),
    '"': (".#.#.", ".#.#.", ".....", ".....", ".....", ".....", "....."),
    '$': ("..#..", ".####", "#.#..", ".###.", "..#.#", "####.", "..#.."),
    '\u2022': (".....", ".....", ".###.", ".###.", ".###.", ".....", "....."),
}
BLANK = (".....",) * 7


def text_width(text, scale):
    """Pixel width of text at a scale (6 units per char, 1 unit spacing)."""
    return len(text) * 6 * scale - scale


def wrap(text, max_chars):
    """Greedy word wrap into lines of at most max_chars characters."""
    lines = []
    for para in text.split("\n"):
        words = para.split(" ")
        cur = ""
        for word in words:
            if cur and len(cur) + 1 + len(word) > max_chars:
                lines.append(cur)
                cur = word
            elif cur:
                cur += " " + word
            else:
                cur = word
        if cur:
            lines.append(cur)
    return lines


# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(w * h * 3)
        r, g, b = bg
        for i in range(0, len(self.px), 3):
            self.px[i] = r
            self.px[i + 1] = g
            self.px[i + 2] = b

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i], self.px[i + 1], self.px[i + 2] = color

    def fill_rect(self, x, y, w, h, color):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.w, x + w)
        y1 = min(self.h, y + h)
        r, g, b = color
        for yy in range(y0, y1):
            base = (yy * self.w + x0) * 3
            for xx in range(x0, x1):
                i = base + (xx - x0) * 3
                self.px[i] = r
                self.px[i + 1] = g
                self.px[i + 2] = b

    def hline(self, x, y, w, color, thick=1):
        self.fill_rect(x, y, w, thick, color)

    def vline(self, x, y, h, color, thick=1):
        self.fill_rect(x, y, thick, h, color)

    def line(self, x0, y0, x1, y1, color):
        """Bresenham line."""
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            self.set(x0, y0, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def circle(self, cx, cy, r, color):
        """Filled circle."""
        for dy in range(-r, r + 1):
            half = int((r * r - dy * dy) ** 0.5)
            self.hline(cx - half, cy + dy, half * 2 + 1, color)

    def triangle(self, p0, p1, p2, color):
        """Filled triangle, scanline fill."""
        pts = sorted([p0, p1, p2], key=lambda p: p[1])
        (x0, y0), (x1, y1), (x2, y2) = pts
        if y0 == y2:
            return
        for y in range(y0, y2 + 1):
            if y <= y1:
                t1 = (y - y0) / (y1 - y0) if y1 != y0 else 0.0
                xa = x0 + (x1 - x0) * t1
            else:
                t1 = (y - y1) / (y2 - y1) if y2 != y1 else 0.0
                xa = x1 + (x2 - x1) * t1
            t2 = (y - y0) / (y2 - y0)
            xb = x0 + (x2 - x0) * t2
            lo, hi = (xa, xb) if xa <= xb else (xb, xa)
            self.hline(int(lo), y, int(hi) - int(lo) + 1, color)

    def text(self, x, y, s, scale, color):
        cx = x
        for ch in s:
            glyph = FONT.get(ch, BLANK)
            for row in range(7):
                bits = glyph[row]
                for col in range(5):
                    if bits[col] == '#':
                        self.fill_rect(cx + col * scale, y + row * scale,
                                       scale, scale, color)
            cx += 6 * scale
        return cx

    def text_center(self, y, s, scale, color, cx=512):
        w = text_width(s, scale)
        self.text(cx - w // 2, y, s, scale, color)
        return y + 8 * scale

    def rule(self, y, thick=3):
        self.hline(36, y, W - 72, INK, thick)


# ---------------------------------------------------------------- png
def chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    return out


def write_png(canvas, path):
    raw = bytearray()
    for y in range(canvas.h):
        raw.append(0)  # filter: none
        start = y * canvas.w * 3
        raw += canvas.px[start:start + canvas.w * 3]
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", canvas.w, canvas.h,
                                      8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)
    return len(png)


# ---------------------------------------------------------------- picture
def draw_scene(c, x, y, w, h):
    """Stylised dusk over the Gulf: low sun, dark sea, a tanker with
    smoke columns rising from its funnels."""
    # sky bands, dusk orange deepening to dark red
    bands = [(DUSK, 0.30), ((178, 62, 40), 0.25), (DUSK_DEEP, 0.20),
             ((94, 32, 34), 0.25)]
    yy = y
    for color, frac in bands:
        bh = int(h * frac)
        c.fill_rect(x, yy, w, bh, color)
        yy += bh
    # low sun
    c.circle(x + int(w * 0.72), y + int(h * 0.34), 34, SUN)
    c.circle(x + int(w * 0.72), y + int(h * 0.34), 26, (250, 214, 110))
    # distant skyline silhouettes
    base = y + int(h * 0.62)
    for bx, bw, bh in [(0, 60, 26), (70, 36, 44), (116, 52, 30),
                       (830, 44, 52), (884, 60, 28), (700, 30, 20)]:
        c.fill_rect(x + bx, base - bh, bw, bh, (60, 24, 28))
    # sea
    c.fill_rect(x, base, w, y + h - base, SEA)
    for k in range(5):
        wy = base + 8 + k * 9
        c.hline(x + 20 + (k % 2) * 30, wy, w - 90, (120, 170, 190), 2)
    # tanker silhouette, centre-left
    hx, hy = x + 300, base - 34
    c.fill_rect(hx, hy, 330, 30, INK)                    # hull
    c.triangle((hx + 330, hy), (hx + 372, hy + 6), (hx + 330, hy + 30), INK)
    c.fill_rect(hx + 30, hy - 22, 150, 22, INK)          # deck block
    c.fill_rect(hx + 200, hy - 34, 26, 34, INK)          # funnel 1
    c.fill_rect(hx + 250, hy - 28, 22, 28, INK)          # funnel 2
    c.vline(hx + 70, hy - 48, 26, INK, 3)                # mast
    c.hline(hx + 58, hy - 48, 24, INK, 3)
    # smoke columns drifting up from the funnels (kept inside the picture)
    for i, (sx, sy, sr) in enumerate([(hx + 213, hy - 30, 10),
                                      (hx + 222, hy - 46, 13),
                                      (hx + 234, hy - 62, 16),
                                      (hx + 261, hy - 26, 9),
                                      (hx + 270, hy - 40, 12),
                                      (hx + 280, hy - 54, 15)]):
        c.circle(sx, sy, sr, SMOKE_LIGHT if i % 2 else SMOKE)
    # gulls
    for gx, gy in [(x + 120, y + 26), (x + 150, y + 40), (x + 820, y + 30)]:
        c.line(gx - 8, gy, gx, gy - 5, INK)
        c.line(gx, gy - 5, gx + 8, gy, INK)


# ---------------------------------------------------------------- stories
LEAD_DECK = (
    "IRAN'S REVOLUTIONARY GUARDS CLAIM MISSILE AND DRONE STRIKES ON US "
    "POSITIONS AT AL-RIFFA AND AWALI. BAHRAIN SAYS A CIVILIAN PLANT WAS "
    "HIT AND SET ABLAZE, WITH TWO PEOPLE HURT."
)

GRID = [
    ("UKRAINE WAR", "SHIP STILL BURNING OFF FINLAND",
     "A RUSSIAN CARGO SHIP IS STILL ABLAZE AFTER AN ATTACK. 14 PEOPLE ARE "
     "MISSING AFTER A DRONE HIT FLATS IN THE KYIV REGION, KYIV SAYS."),
    ("CLIMATE", "COP31 DRAFT DROPS 'FOSSIL FUELS'",
     "THE FINAL DRAFT IN TURKIYE AVOIDS THE WORDS BEHIND GLOBAL WARMING "
     "AS TALKS STALL AND NATIONS SPLIT."),
    ("ASIA", "SEOUL MINISTER QUITS IN AI EXAM SCANDAL",
     "SOUTH KOREA'S EDUCATION MINISTER RESIGNS AMID A CHEATING ROW OVER "
     "AI IN EXAMS."),
    ("DIPLOMACY", "NEPAL PM IN TALKS WITH MODI",
     "BALENDRA SHAH IS IN DELHI ON A TWO-DAY STATE VISIT TO REVIEW TIES "
     "WITH INDIA."),
    ("CRICKET", "INDIA 720 FOR 9: RECORD IN WELLINGTON",
     "INDIA POST A RECORD TEST TOTAL AGAINST NEW ZEALAND ON DAY FOUR AT "
     "THE BASIN RESERVE."),
    ("EUROPE", "LISBON MARCHES ON LIVING COSTS",
     "THOUSANDS TAKE TO THE STREETS AS RISING PRICES FUEL ANGER IN "
     "PORTUGAL."),
]

ALSO_TODAY = (
    "UN STATES AGREE TO KEEP TALKING ON LETHAL AI WEAPONS \u2022 MYANMAR "
    "CALLS ASEAN MOVE UNFAIR \u2022 7 DEAD, 50 MISSING IN INDONESIA "
    "FACTORY FIRE \u2022 MEXICO SEIZES 'EL CHAPO ISIDRO'; 11 DEAD \u2022 "
    "EISENKOT CALLS SETTLER ARSON 'JEWISH TERRORISM'"
)


def draw_page():
    c = Canvas(W, H, PAPER)
    x0, x1 = 36, W - 36
    y = 26

    # masthead rules
    c.rule(y)
    y += 8
    c.hline(x0, y, x1 - x0, INK, 1)
    y += 12

    # masthead
    y = c.text_center(y, "THE WORLD TODAY", 8, INK)
    y += 4
    # dateline row: number left, date centre, price right
    c.text(x0, y, "NO. 6", 2, INK)
    c.text_center(y, "SUNDAY 23 NOVEMBER 2026", 3, INK)
    price = "PRICE: FREE"
    c.text(x1 - text_width(price, 2), y, price, 2, INK)
    y += 8 * 3 + 8
    c.rule(y)
    y += 10

    # lead kicker + headline
    y = c.text_center(y, "GULF IN FLAMES", 3, RED)
    y += 6
    y = c.text_center(y, "BAHRAIN DEMANDS UN ACTION", 5, INK)
    y = c.text_center(y, "AFTER IRAN STRIKES US BASES", 5, INK)
    y += 8

    # lead deck, centred, scale 2
    for line in wrap(LEAD_DECK, 76):
        y = c.text_center(y, line, 2, INK)
    y += 10

    # picture
    pic_y = y
    pic_h = 196
    draw_scene(c, x0, pic_y, x1 - x0, pic_h)
    y = pic_y + pic_h + 6
    for line in wrap("SMOKE OVER SITRA AFTER THE OVERNIGHT STRIKES. BAHRAIN "
                     "SAYS ITS DEFENCES INTERCEPTED SEVERAL ATTACKS. "
                     "(WIRE PICTURE)", 150):
        y = c.text_center(y, line, 1, GREY)
    y += 10
    c.rule(y, 1)
    y += 12

    # story grid: 3 columns x 2 rows
    col_w = (x1 - x0 - 2 * 24) // 3
    row_h = 152
    for idx, (kicker, head, body) in enumerate(GRID):
        row, col = divmod(idx, 3)
        gx = x0 + col * (col_w + 24)
        gy = y + row * row_h
        if col:
            c.vline(gx - 12, gy, row_h - 12, GREY, 1)
        cy = gy
        c.text(gx, cy, kicker, 1, RED)
        cy += 12
        for line in wrap(head, 26):
            c.text(gx, cy, line, 2, INK)
            cy += 17
        cy += 2
        for line in wrap(body, 50):
            c.text(gx, cy, line, 1, INK)
            cy += 10
    y += 2 * row_h + 4
    c.rule(y, 1)
    y += 12

    # also today
    c.text(x0, y, "ALSO TODAY", 2, RED)
    y += 20
    for line in wrap(ALSO_TODAY, 78):
        c.text_center(y, line, 1, INK)
        y += 11
    y += 12
    c.rule(y, 1)
    y += 10
    c.text_center(y, "THE WORLD TODAY -- COMPILED FROM WIRE REPORTS -- "
                  "23 NOVEMBER 2026 -- MAKE.FUN DAILY FRONT PAGE", 1, GREY)
    y += 16
    c.rule(y)
    assert y < H - 10, "page overflow: %d" % y
    return c


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    size = write_png(draw_page(), path)
    print("wrote %s (%d bytes)" % (path, size))


if __name__ == "__main__":
    main()
