#!/usr/bin/env python3
"""Draw the news-image-20261124 front page, round 2, with Pillow.

One 1024x1024 newspaper page summing up Tuesday 24 November 2026.
Round 2 fixes round 1's facts and sharpens the layout:
- the sunk ship is named correctly: the Russian corvette Mercury
  (with a Ka-27 helicopter), struck off Benghazi, Libya — round 1
  wrongly named the ferry Ambal, hit days earlier in the Baltic;
- the chip rally is stated correctly: Nvidia +31.5% on Monday after
  Jensen Huang's reinstatement, Asia rallying on Tuesday (Taiwan +9%,
  Seoul +6%) — round 1's "SK hynix +20%" was wrong;
- a fresh 24 November story joins the page: the EU's 22nd sanctions
  package (about 60 banks cut from SWIFT);
- a "day in numbers" strip makes the page readable at a glance.
Round 3 adds a small pictogram to each story (carrier, chip, EU stars,
truce flag) and gives the Thai–Cambodia truce its verified terms: a
72-hour ceasefire after a 20-day border war, 18 soldiers to be freed,
ASEAN observers verifying.
Round 4 adds a "Where the day happened" dateline strip under the hero
art — Benghazi, Kyiv, Tehran, Bangkok and Taipei placed by longitude —
and a ticker item: Kyiv says Ukraine needs €115bn for 2027.
Round 5 adds the verified human cost to the standfirst (Russians and
Libyans killed aboard the Mercury), the NBC report that the US military
is weighing strikes on Iran's leaders, and a distant patrol boat on the
hero art's horizon.
Round 6 adds the fire's reflection shimmering on the water under the
burning corvette, and tightens the numbers strip ("60 banks cut from
SWIFT").
Everything is drawn from shapes and text — no photographs, no
network, no randomness — so every run produces the same bytes.
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
    """Flat dusk scene: sky bands, low sun, sea, a burning corvette."""
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
    # Distant patrol boat on the left horizon, for depth.
    draw.polygon([(x0 + 30, horizon + 8), (x0 + 38, horizon - 2),
                  (x0 + 92, horizon - 2), (x0 + 100, horizon + 8)],
                 fill=(16, 19, 24))
    draw.rectangle([x0 + 56, horizon - 10, x0 + 66, horizon - 2],
                   fill=(16, 19, 24))
    # Distant coastline on the right.
    draw.polygon([(x1 - 260, horizon), (x1 - 190, horizon - 16),
                  (x1 - 120, horizon - 6), (x1, horizon - 12), (x1, horizon)],
                 fill=(24, 30, 38))
    # Corvette silhouette, centre-left, listing slightly.
    hull_y = y1 - 52
    draw.polygon([(x0 + 120, hull_y), (x0 + 150, hull_y - 30),
                  (x0 + 540, hull_y - 30), (x0 + 580, hull_y),
                  (x0 + 540, hull_y + 11), (x0 + 170, hull_y + 11)],
                 fill=(16, 19, 24))
    draw.rectangle([x0 + 290, hull_y - 58, x0 + 360, hull_y - 30],
                   fill=(16, 19, 24))  # superstructure
    draw.rectangle([x0 + 385, hull_y - 74, x0 + 408, hull_y - 30],
                   fill=(16, 19, 24))  # funnel
    draw.line([(x0 + 320, hull_y - 58), (x0 + 320, hull_y - 84)],
              fill=(16, 19, 24), width=5)  # mast
    # Portholes along the hull so it reads as a warship.
    for px in range(x0 + 190, x0 + 540, 34):
        draw.ellipse([px, hull_y - 18, px + 6, hull_y - 12],
                     fill=(232, 200, 120))
    # Fire and smoke from the midship hit. Smoke stays inside the art box.
    draw.ellipse([x0 + 410, hull_y - 46, x0 + 472, hull_y - 6],
                 fill=(232, 120, 30))
    draw.ellipse([x0 + 430, hull_y - 35, x0 + 462, hull_y - 12],
                 fill=(250, 200, 90))
    for i, r in enumerate((11, 14, 17)):
        cy = hull_y - 58 - i * 19
        draw.ellipse([x0 + 430 + i * 5 - r, cy - r,
                      x0 + 430 + i * 5 + r, cy + r],
                     fill=(70, 70, 74))
    # The fire's reflection shimmering on the water below the ship.
    reflections = [(hull_y + 18, 96, (232, 120, 30)),
                   (hull_y + 28, 72, (216, 100, 36)),
                   (hull_y + 38, 48, (196, 84, 40))]
    for wy, wdt, col in reflections:
        draw.line([(x0 + 441 - wdt // 2, wy), (x0 + 441 + wdt // 2, wy)],
                  fill=col, width=3)
    # A Ka-27 helicopter, damaged, trailing smoke — bigger, with a
    # clear rotor, tail boom and skids so it reads as a helicopter.
    hx, hy = x0 + 660, y0 + 46
    draw.ellipse([hx - 34, hy - 10, hx + 30, hy + 10], fill=(20, 20, 22))
    draw.line([(hx - 58, hy - 4), (hx + 58, hy - 4)], fill=(20, 20, 22),
              width=4)  # main rotor
    draw.line([(hx - 6, hy - 10), (hx - 6, hy - 18)], fill=(20, 20, 22),
              width=3)  # rotor mast
    draw.polygon([(hx + 28, hy - 4), (hx + 66, hy - 12), (hx + 66, hy - 2),
                  (hx + 28, hy + 2)], fill=(20, 20, 22))  # tail boom
    draw.line([(hx + 62, hy - 12), (hx + 62, hy + 10)], fill=(20, 20, 22),
              width=3)  # tail rotor
    draw.line([(hx - 18, hy + 10), (hx - 12, hy + 22)], fill=(20, 20, 22),
              width=3)
    draw.line([(hx + 12, hy + 10), (hx + 18, hy + 22)], fill=(20, 20, 22),
              width=3)
    draw.line([(hx - 18, hy + 22), (hx + 24, hy + 22)], fill=(20, 20, 22),
              width=3)  # skids
    for i, r in enumerate((7, 9, 11)):  # smoke trail behind it
        draw.ellipse([hx - 78 - i * 16 - r, hy + 2 - r,
                      hx - 78 - i * 16 + r, hy + 2 + r],
                     fill=(110, 110, 114))
    # "LIBYAN COAST" label on the dark coastline, bottom right.
    lab = "LIBYAN COAST"
    lf = font(SANS_BOLD, 11)
    draw.text((x1 - draw.textlength(lab, font=lf) - 10, y1 - 22), lab,
              font=lf, fill=(220, 220, 210))
    # Two naval drones in the sky.
    for dx, dy in ((x0 + 90, y0 + 40), (x0 + 160, y0 + 74)):
        draw.line([(dx - 12, dy - 8), (dx + 12, dy + 8)], fill=(20, 20, 22),
                  width=3)
        draw.line([(dx - 12, dy + 8), (dx + 12, dy - 8)], fill=(20, 20, 22),
                  width=3)
        draw.ellipse([dx - 4, dy - 4, dx + 4, dy + 4], fill=(20, 20, 22))


def icon(draw, kind, x, y, colour):
    """Small flat pictogram (26x26 box at x, y) for a story cell."""
    if kind == "carrier":  # aircraft carrier
        draw.polygon([(x, y + 16), (x + 4, y + 10), (x + 22, y + 10),
                      (x + 26, y + 16), (x + 22, y + 19), (x + 4, y + 19)],
                     fill=colour)
        draw.rectangle([x + 15, y + 3, x + 19, y + 10], fill=colour)
        draw.line([(x + 17, y + 3), (x + 17, y - 1)], fill=colour, width=2)
    elif kind == "chip":  # microchip
        draw.rectangle([x + 4, y + 4, x + 22, y + 22], outline=colour,
                       width=2)
        draw.rectangle([x + 10, y + 10, x + 16, y + 16], fill=colour)
        for px in (x + 8, x + 13, x + 18):
            draw.line([(px, y), (px, y + 4)], fill=colour, width=2)
            draw.line([(px, y + 22), (px, y + 26)], fill=colour, width=2)
            draw.line([(x, y + px - x), (x + 4, y + px - x)], fill=colour,
                      width=2)
            draw.line([(x + 22, y + px - x), (x + 26, y + px - x)],
                      fill=colour, width=2)
    elif kind == "stars":  # circle of stars (EU)
        import math
        for k in range(12):
            a = 2 * math.pi * k / 12 - math.pi / 2
            cx, cy = x + 13 + 9 * math.cos(a), y + 13 + 9 * math.sin(a)
            draw.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=colour)
    elif kind == "flag":  # white-flag truce
        draw.line([(x + 6, y + 2), (x + 6, y + 24)], fill=colour, width=2)
        draw.polygon([(x + 6, y + 2), (x + 24, y + 6), (x + 6, y + 11)],
                     fill=colour)


def story_cell(draw, x, y, w, head, body, accent, kind):
    icon(draw, kind, x, y, accent)
    draw.rectangle([x + 34, y + 10, x + w, y + 15], fill=accent)
    y = draw_wrapped(draw, x, y + 32, head, font(SERIF_BOLD, 21), w,
                     leading=24)
    y = draw_wrapped(draw, x, y + 4, body, font(SERIF, 15), w, leading=18)
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
    lines = ["UKRAINE SINKS RUSSIAN", "CORVETTE OFF LIBYA"]
    y = 150
    for ln in lines:
        d.text(((W - d.textlength(ln, font=head)) / 2, y), ln, font=head,
               fill=INK)
        y += 52
    stand = ("Kyiv says naval drones sank the corvette Mercury — and a "
             "Ka-27 helicopter with it — off Benghazi, killing Russians "
             "and Libyans aboard, as the UN calls for a probe.")
    y = draw_wrapped(d, mx + 60, y + 2, stand, font(SERIF_IT, 18), rx - mx - 120,
                     fill=(40, 40, 40), leading=23)

    # ---- Hero art + caption ----
    art_y0, art_y1 = 308, 464
    hero_art(d, mx, art_y0, rx, art_y1)
    d.rectangle([mx, art_y0, rx, art_y1], outline=INK, width=2)
    cap = ("The Russian corvette Mercury burns off the Libyan coast after "
           "Ukrainian naval drones struck it, Kyiv said. — Illustration")
    draw_wrapped(d, mx, art_y1 + 8, cap, font(SERIF_IT, 13), rx - mx,
                 fill=GREY, leading=16)

    # ---- Dateline: where the day happened ----
    tf = font(SANS_BOLD, 10)
    y_line = 508
    d.text((mx, y_line - 14), "WHERE THE DAY HAPPENED", font=tf, fill=GREY)
    d.line([(mx, y_line), (rx, y_line)], fill=GREY, width=1)
    cities = [("BENGHAZI", 20, True), ("KYIV", 30, False),
              ("TEHRAN", 51, True), ("BANGKOK", 100, False),
              ("TAIPEI", 121, True)]
    for name, lon, above in cities:
        cx = mx + int((lon + 10) / 140 * (rx - mx))
        d.ellipse([cx - 4, y_line - 4, cx + 4, y_line + 4], fill=RED)
        w = d.textlength(name, font=tf)
        lx = min(max(cx - w / 2, mx), rx - w)
        ly = y_line - 13 if above else y_line + 6
        d.text((lx, ly), name, font=tf, fill=INK)

    # ---- Four stories, two by two ----
    rule(d, mx, 534, rx, 2)
    col_w = (rx - mx - 24) // 2
    story_cell(
        d, mx, 546, col_w,
        "TRUMP WARNS IRAN OF “VERY TRAUMATIC” OUTCOME",
        "Trump says Tehran faces a “very traumatic” outcome if talks fail; "
        "NBC reports the US military is weighing strikes on Iran's "
        "leaders. Netanyahu urges him to strike soon.",
        RED, "carrier")
    story_cell(
        d, mx + col_w + 24, 546, col_w,
        "HUANG'S RETURN SENDS CHIP STOCKS SOARING",
        "Nvidia jumps 31.5% in a day — over $900bn of value — after Jensen "
        "Huang is reinstated as chief. Asia follows on Tuesday: Taiwan up "
        "9%, Seoul up 6%.",
        NAVY, "chip")
    rule(d, mx, 686, rx, 1, fill=GREY)
    story_cell(
        d, mx, 696, col_w,
        "EU PROPOSES 22ND SANCTIONS PACKAGE ON RUSSIA",
        "Brussels plans to cut about 60 banks from SWIFT and target more "
        "than 70 shadow-fleet ships, crypto networks and athletes "
        "competing under the Russian flag.",
        RED, "stars")
    story_cell(
        d, mx + col_w + 24, 696, col_w,
        "TRUCE HOLDS ON THAI–CAMBODIA BORDER",
        "A 72-hour ceasefire ends a 20-day border war that killed dozens "
        "and displaced close to a million. Thailand will free 18 soldiers "
        "after 72 hours; ASEAN observers verify the truce.",
        NAVY, "flag")

    # ---- The day in numbers ----
    rule(d, mx, 834, rx, 2)
    d.text((mx, 846), "THE DAY IN NUMBERS", font=font(SANS_BOLD, 13),
           fill=GREY)
    stats = [("+31.5%", "Nvidia shares in a day"),
             ("50M", "children vaccinated in Bangladesh"),
             ("60", "banks cut from SWIFT"),
             ("$41bn", "Sanofi agrees to buy Insmed")]
    col = (rx - mx) // 4
    for i, (num, lab) in enumerate(stats):
        x = mx + i * col
        d.text((x, 866), num, font=font(SANS_BOLD, 22), fill=RED)
        draw_wrapped(d, x, 894, lab, font(SANS, 11), col - 12,
                     fill=INK, leading=14)

    # ---- Ticker ----
    d.rectangle([mx, 920, rx, 962], fill=NAVY)
    ticker = ("HOUTHI ATTACK WOUNDS 11 AT RIYADH TOWER  •  BLAST AT HANOI "
              "RESTAURANT KILLS 6  •  SOFTBANK TO INVEST $2BN IN INTEL  •  "
              "SUDAN DRONES DAMAGE UN BUILDING  •  KYIV SAYS UKRAINE NEEDS "
              "€115BN FOR 2027")
    tf = font(SANS_BOLD, 13)
    tlines = wrap(d, ticker, tf, rx - mx - 16)
    ty = 928
    for ln in tlines:
        d.text((mx + 8, ty), ln, font=tf, fill=(255, 255, 255))
        ty += 18

    # ---- Footer ----
    foot = ("The World Today — one page summing up Tuesday 24 November 2026  •  "
            "Drawn by an AI agent for make.fun")
    ff = font(SANS, 12)
    d.text(((W - d.textlength(foot, font=ff)) / 2, 972), foot, font=ff,
           fill=GREY)

    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
