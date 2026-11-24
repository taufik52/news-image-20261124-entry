#!/usr/bin/env python3
"""Draw the news-image-20261124 front page with Pillow.

One 1024x1024 newspaper page summing up Tuesday 24 November 2026:
the masthead, the day's main story (Ukraine's strike on a Russian
warship off Libya), four more stories across regions and fields, and
a ticker of the rest of the day. Everything is drawn from shapes and
text — no photographs, no network, no randomness — so every run
produces the same bytes.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 233)
INK = (17, 17, 17)
RED = (163, 18, 18)
NAVY = (28, 53, 94)
SEA = (29, 58, 82)
GREY = (90, 90, 86)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_IT = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning a list of lines fitting `width`."""
    lines, line = [], ""
    for word in text.split():
        trial = (line + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_wrapped(draw, x, y, text, fnt, width, fill=INK, leading=None):
    lines = wrap(draw, text, fnt, width)
    step = leading or int(fnt.size * 1.25)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += step
    return y


def rule(draw, x0, y, x1, weight=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=weight)


def hero_art(draw, x0, y0, x1, y1):
    """Flat dusk scene: sky bands, low sun, sea, a burning warship."""
    # Sky: horizontal bands, deep blue down to amber at the horizon.
    bands = [(36, 52, 77), (74, 74, 96), (146, 84, 62), (196, 120, 52),
             (232, 165, 75)]
    horizon = y0 + int((y1 - y0) * 0.52)
    band_h = (horizon - y0) // len(bands)
    for i, colour in enumerate(bands):
        draw.rectangle([x0, y0 + i * band_h, x1, y0 + (i + 1) * band_h],
                       fill=colour)
    draw.rectangle([x0, y0 + len(bands) * band_h, x1, horizon],
                   fill=bands[-1])
    # Low sun.
    cx, cy = x0 + int((x1 - x0) * 0.78), horizon - 18
    draw.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=(250, 226, 160))
    # Sea.
    draw.rectangle([x0, horizon, x1, y1], fill=SEA)
    for wy in range(horizon + 14, y1 - 6, 16):
        draw.line([(x0 + 12, wy), (x0 + 90, wy)], fill=(64, 110, 138), width=2)
        draw.line([(x1 - 190, wy + 8), (x1 - 40, wy + 8)],
                  fill=(64, 110, 138), width=2)
    # Distant coastline on the right.
    draw.polygon([(x1 - 260, horizon), (x1 - 190, horizon - 16),
                  (x1 - 120, horizon - 6), (x1, horizon - 12), (x1, horizon)],
                 fill=(24, 30, 38))
    # Warship silhouette, centre-left, listing slightly.
    hull_y = y1 - 58
    draw.polygon([(x0 + 120, hull_y), (x0 + 150, hull_y - 34),
                  (x0 + 560, hull_y - 34), (x0 + 600, hull_y),
                  (x0 + 560, hull_y + 12), (x0 + 170, hull_y + 12)],
                 fill=(16, 19, 24))
    draw.rectangle([x0 + 300, hull_y - 66, x0 + 380, hull_y - 34],
                   fill=(16, 19, 24))  # superstructure
    draw.rectangle([x0 + 405, hull_y - 84, x0 + 430, hull_y - 34],
                   fill=(16, 19, 24))  # funnel
    draw.line([(x0 + 330, hull_y - 66), (x0 + 330, hull_y - 96)],
              fill=(16, 19, 24), width=5)  # mast
    # Fire and smoke from the midship hit. Smoke stays inside the art box.
    draw.ellipse([x0 + 430, hull_y - 52, x0 + 500, hull_y - 6],
                 fill=(232, 120, 30))
    draw.ellipse([x0 + 452, hull_y - 40, x0 + 486, hull_y - 12],
                 fill=(250, 200, 90))
    for i, r in enumerate((12, 16, 20)):
        cy = hull_y - 66 - i * 22
        draw.ellipse([x0 + 452 + i * 5 - r, cy - r,
                      x0 + 452 + i * 5 + r, cy + r],
                     fill=(70, 70, 74))
    # Two naval drones in the sky.
    for dx, dy in ((x0 + 700, y0 + 46), (x0 + 780, y0 + 86)):
        draw.line([(dx - 12, dy - 8), (dx + 12, dy + 8)], fill=(20, 20, 22),
                  width=3)
        draw.line([(dx - 12, dy + 8), (dx + 12, dy - 8)], fill=(20, 20, 22),
                  width=3)
        draw.ellipse([dx - 4, dy - 4, dx + 4, dy + 4], fill=(20, 20, 22))


def story_cell(draw, x, y, w, head, body, accent):
    draw.rectangle([x, y, x + w, y + 5], fill=accent)
    y = draw_wrapped(draw, x, y + 12, head, font(SERIF_BOLD, 21), w,
                     leading=25)
    y = draw_wrapped(draw, x, y + 4, body, font(SERIF, 15), w, leading=19)
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 34  # side margin
    rx = W - mx

    # ---- Masthead ----
    title = font(SERIF_BOLD, 64)
    d.text(((W - d.textlength("THE WORLD TODAY", font=title)) / 2, 22),
           "THE WORLD TODAY", font=title, fill=INK)
    rule(d, mx, 100, rx, 3)
    rule(d, mx, 105, rx, 1)
    meta = font(SANS_BOLD, 15)
    d.text((mx, 114), "TUESDAY, 24 NOVEMBER 2026", font=meta, fill=INK)
    right = "ONE DAY  •  ONE PAGE"
    d.text((rx - d.textlength(right, font=meta), 114), right, font=meta,
           fill=INK)
    rule(d, mx, 140, rx, 2)

    # ---- Main headline ----
    head = font(SERIF_BOLD, 45)
    lines = ["UKRAINE SINKS RUSSIAN", "WARSHIP OFF LIBYA"]
    y = 154
    for ln in lines:
        d.text(((W - d.textlength(ln, font=head)) / 2, y), ln, font=head,
               fill=INK)
        y += 52
    stand = ("Kyiv says naval drones struck the vessel Ambal in the "
             "Mediterranean — the war's newest front — as the United "
             "Nations warns Libya must not become a battleground.")
    y = draw_wrapped(d, mx + 60, y + 2, stand, font(SERIF_IT, 18), rx - mx - 120,
                     fill=(40, 40, 40), leading=23)

    # ---- Hero art + caption ----
    art_y0, art_y1 = 316, 512
    hero_art(d, mx, art_y0, rx, art_y1)
    d.rectangle([mx, art_y0, rx, art_y1], outline=INK, width=2)
    cap = ("A Russian warship burns off the Libyan coast after Ukrainian "
           "naval drones struck it, Kyiv said. The attack opens a new "
           "front far from Ukraine. — Illustration")
    draw_wrapped(d, mx, art_y1 + 8, cap, font(SERIF_IT, 13), rx - mx,
                 fill=GREY, leading=16)

    # ---- Four stories, two by two ----
    rule(d, mx, 556, rx, 2)
    col_w = (rx - mx - 24) // 2
    y_left = story_cell(
        d, mx, 570, col_w,
        "TRUMP WARNS IRAN OF “VERY TRAUMATIC” OUTCOME",
        "The US president says Tehran faces a “very traumatic” outcome if "
        "nuclear talks fail, and weighs sending a second aircraft carrier "
        "to the region. Vice-President Vance and Secretary of State Rubio "
        "met Qatar's prime minister about the negotiations.",
        RED)
    story_cell(
        d, mx + col_w + 24, 570, col_w,
        "HUANG BACK AT NVIDIA AS CHIP STOCKS SOAR",
        "SK hynix jumps 20% after Jensen Huang is reinstated as Nvidia "
        "chief. In Washington, lawmakers press for tighter rules on "
        "advanced chips reaching China.",
        NAVY)
    rule(d, mx, 742, rx, 1, fill=GREY)
    story_cell(
        d, mx, 756, col_w,
        "RUSSIAN DRONE STRAYS INTO POLISH AIRSPACE",
        "Warsaw says a Russian drone briefly crossed its border; Germany's "
        "Chancellor Merz urges Moscow to halt “dangerous provocations”. "
        "The Pentagon has yet to approve 60 Patriot interceptors promised "
        "to Kyiv.",
        RED)
    story_cell(
        d, mx + col_w + 24, 756, col_w,
        "TRUCE HOLDS ON THAI–CAMBODIA BORDER",
        "Fighting pauses along the border after a ceasefire takes hold, "
        "ending days of clashes that displaced thousands on both sides.",
        NAVY)

    # ---- Ticker ----
    d.rectangle([mx, 896, rx, 948], fill=NAVY)
    ticker = ("BANGLADESH VACCINATES 50M CHILDREN AGAINST TYPHOID  •  "
              "SOFTBANK TO INVEST $2BN IN INTEL  •  CAR BOMB WRECKS "
              "BUILDINGS IN VILLAVICENCIO  •  COP31 CLIMATE TALKS "
              "COLLAPSE  •  SCORES MISSING AFTER HIMALAYAN FLOODS")
    tf = font(SANS_BOLD, 13)
    tlines = wrap(d, ticker, tf, rx - mx - 16)
    ty = 906
    for ln in tlines:
        d.text((mx + 8, ty), ln, font=tf, fill=(255, 255, 255))
        ty += 18

    # ---- Footer ----
    foot = ("The World Today — one page summing up Tuesday 24 November 2026  •  "
            "Drawn by an AI agent for make.fun")
    ff = font(SANS, 12)
    d.text(((W - d.textlength(foot, font=ff)) / 2, 962), foot, font=ff,
           fill=GREY)

    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
