"""
Render the README teaser PNG as a faithful static composition of
Figure 4 from docs/index.html.

Output: docs/assets/dim_figure4_teaser.png

The layout mirrors the .face-grid figure in the press release:

    [ Identity A | FaceMorpher | OpenCV | DiM (ours) | StyleGAN2 | MIPGAN-II | Identity B ]
      row 1: FRLL pair 043 x 114
      row 2: FRLL pair 128 x 105

The DiM column is highlighted with a mauve ring and an "ours" ribbon,
and an italic-serif Figure 4 caption sits below the grid.
"""

import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter


# ── paths ────────────────────────────────────────────────────────────
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # docs/
TILES = os.path.join(ROOT, "assets", "figures", "comparison")
OUT_PATH = os.path.join(ROOT, "assets", "dim_figure4_teaser.png")


# ── palette (matches the press-release :root) ────────────────────────
BG_DEEP        = (255, 255, 248)   # parchment
PAPER_SOFT     = (255, 255, 251)
INK            = (13, 23, 38)
TEXT_PRIMARY   = (22, 30, 45)
TEXT_SECONDARY = (58, 65, 80)
TEXT_DIM       = (138, 145, 160)
RULE           = (207, 210, 216)
HAIRLINE       = (235, 235, 235)
MAUVE          = (26, 95, 158)
MAUVE_DEEP     = (10, 58, 107)
MAUVE_LIGHT    = (221, 233, 243)
CELL_BG        = (10, 14, 22)


# ── fonts ────────────────────────────────────────────────────────────
def f(path, size):
    return ImageFont.truetype(path, size)

# Helvetica is a close enough sans for the column headers/labels;
# Georgia Italic stands in for et-book italic in the caption.
SANS         = "/System/Library/Fonts/Helvetica.ttc"
MONO         = "/System/Library/Fonts/Menlo.ttc"
SERIF_ITALIC = "/System/Library/Fonts/Supplemental/Georgia Italic.ttf"
SERIF_BOLD   = "/System/Library/Fonts/Supplemental/Georgia.ttf"


# ── layout constants ─────────────────────────────────────────────────
COLS = 7
CELL = 200                   # face tile edge (px) — slightly smaller for a leaner README hero
GAP  = 14                    # gap between tiles
PAD_X = 56                   # left/right canvas padding
PAD_TOP = 24                 # top of the title strip
TITLE_H = 64                 # title strip ("DIFFUSION MORPHS · FIGURE 4 …")
HEADER_H = 64                # column-header band height
PAIR_LABEL_H = 34            # "Pair N — FRLL subjects A & B" strip height
ROW_GAP = 6                  # spacing inside a row (between pair-label and tiles)
ROWS_VGAP = 24               # spacing between Pair 1 and Pair 2
CAPTION_H = 150              # bottom italic-serif caption strip


GRID_W = COLS * CELL + (COLS - 1) * GAP
CANVAS_W = GRID_W + 2 * PAD_X
ROW_H = PAIR_LABEL_H + ROW_GAP + CELL
CANVAS_H = (PAD_TOP + TITLE_H + HEADER_H
            + ROW_H + ROWS_VGAP + ROW_H
            + CAPTION_H)


COLUMN_HEADERS = [
    ("Identity A",   None,       "bona"),
    ("FaceMorpher",  "landmark", None),
    ("OpenCV",       "landmark", None),
    ("DiM",          "ours",     "dim"),
    ("StyleGAN2",    "GAN",      None),
    ("MIPGAN-II",    "GAN",      None),
    ("Identity B",   None,       "bona"),
]

PAIRS = [
    {
        "label": "Pair 1 — FRLL subjects 043 & 114",
        "files": [
            "bonafide_043.png",
            "facemorpher_043_114.png",
            "opencv_043_114.png",
            "dim_043_114.png",
            "stylegan_043_114.png",
            "mipgan_043_114.png",
            "bonafide_114.png",
        ],
    },
    {
        "label": "Pair 2 — FRLL subjects 128 & 105",
        "files": [
            "bonafide_128.png",
            "facemorpher_128_105.png",
            "opencv_128_105.png",
            "dim_128_105.png",
            "stylegan_128_105.png",
            "mipgan_128_105.png",
            "bonafide_105.png",
        ],
    },
]


# ── helpers ──────────────────────────────────────────────────────────
def col_x(idx):
    return PAD_X + idx * (CELL + GAP)


def measure(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def load_tile(name, size):
    """Open one of the comparison tiles and resize/crop-center to a
    square of edge `size`."""
    p = os.path.join(TILES, name)
    im = Image.open(p).convert("RGB")
    w, h = im.size
    # center-crop to a square
    s = min(w, h)
    im = im.crop(((w - s) // 2, (h - s) // 2, (w + s) // 2, (h + s) // 2))
    im = im.resize((size, size), Image.LANCZOS)
    return im


def rounded_mask(size, radius):
    """Build an L-mode mask the same size as a tile with rounded corners."""
    m = Image.new("L", size, 0)
    d = ImageDraw.Draw(m)
    d.rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], radius=radius, fill=255)
    return m


def paste_rounded(canvas, im, xy, radius=10):
    """Paste `im` onto `canvas` at xy with a rounded mask + 1px shadow."""
    mask = rounded_mask(im.size, radius)

    # subtle shadow underlay
    shadow = Image.new("RGBA", (im.size[0] + 8, im.size[1] + 8), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle([4, 4, im.size[0] + 3, im.size[1] + 3],
                         radius=radius, fill=(10, 58, 107, 36))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=3))
    canvas.alpha_composite(shadow, (xy[0] - 4, xy[1] - 4))

    # the tile, masked
    tile_rgba = im.convert("RGBA")
    tile_rgba.putalpha(mask)
    canvas.alpha_composite(tile_rgba, xy)


# ── main render ──────────────────────────────────────────────────────
def render():
    canvas = Image.new("RGBA", (CANVAS_W, CANVAS_H), BG_DEEP + (255,))
    draw = ImageDraw.Draw(canvas)

    # ───── title strip ─────
    # mirrors the press release's eyebrow/venue/title idiom: a tracked
    # mono "DIFFUSION MORPHS · FIGURE 4" line over a serif-italic
    # subtitle, separated by a thin gilt rule. Reads as the banner of
    # the figure rather than a free-floating grid.
    eyebrow_font = f(MONO, 12)
    title_font   = f(SERIF_ITALIC, 24)

    eyebrow_text = "D I F F U S I O N   M O R P H S   ·   F I G U R E   4"
    title_text   = "Two FRLL identity pairs · six morphing pipelines"

    ew, eh = measure(draw, eyebrow_text, eyebrow_font)
    tw, th = measure(draw, title_text, title_font)
    draw.text((PAD_X, PAD_TOP), eyebrow_text,
              font=eyebrow_font, fill=MAUVE)
    draw.text((PAD_X, PAD_TOP + eh + 8), title_text,
              font=title_font, fill=INK)

    # thin gilt rule under the title — fades toward the right edge,
    # matching h2::after in the press release
    rule_y = PAD_TOP + eh + 8 + th + 14
    for i in range(GRID_W):
        # gradient: mauve-deep at left → mauve at 20% → rule at 55% → transparent
        t = i / max(GRID_W - 1, 1)
        if t < 0.20:
            k = t / 0.20
            r = int(MAUVE_DEEP[0] * (1 - k) + MAUVE[0] * k)
            g = int(MAUVE_DEEP[1] * (1 - k) + MAUVE[1] * k)
            b = int(MAUVE_DEEP[2] * (1 - k) + MAUVE[2] * k)
            a = 165
        elif t < 0.55:
            k = (t - 0.20) / 0.35
            r = int(MAUVE[0] * (1 - k) + RULE[0] * k)
            g = int(MAUVE[1] * (1 - k) + RULE[1] * k)
            b = int(MAUVE[2] * (1 - k) + RULE[2] * k)
            a = int(165 * (1 - k) + 110 * k)
        else:
            k = (t - 0.55) / 0.45
            r, g, b = RULE
            a = int(110 * (1 - k))
        canvas.putpixel((PAD_X + i, rule_y), (r, g, b, a))

    # ───── column-header band ─────
    band_top = PAD_TOP + TITLE_H
    label_font   = f(SANS, 16)
    label_dim_font = f(SANS, 16)         # same; bolded by drawing twice
    sub_font     = f(SANS, 12)

    for i, (name, sub, kind) in enumerate(COLUMN_HEADERS):
        cx = col_x(i) + CELL // 2

        # main label
        if kind == "dim":
            font = label_dim_font
            color = MAUVE
        elif kind == "bona":
            font = label_font
            color = TEXT_SECONDARY
        else:
            font = label_font
            color = TEXT_DIM

        w_, h_ = measure(draw, name.upper(), font)
        ly = band_top + 6
        # tracked / uppercase to match the press-release `.face-col-label`
        # PIL has no letter-spacing, so we render char-by-char with a kerning offset.
        tracked = "  ".join(list(name.upper()))
        wt, _ = measure(draw, tracked, font)
        tx = cx - wt // 2
        if kind == "dim":
            # bold-faking: draw twice with 1px x offset
            draw.text((tx, ly), tracked, font=font, fill=color)
            draw.text((tx + 1, ly), tracked, font=font, fill=color)
        else:
            draw.text((tx, ly), tracked, font=font, fill=color)

        # sublabel (landmark / GAN / ours)
        if sub:
            sw, sh = measure(draw, sub, sub_font)
            sx = cx - sw // 2
            sy = ly + h_ + 6
            sub_color = MAUVE if kind == "dim" else TEXT_DIM
            draw.text((sx, sy), sub, font=sub_font, fill=sub_color)

        # hairline under each header — mauve for DiM, faint elsewhere
        line_y = band_top + HEADER_H - 6
        line_x0 = col_x(i) + 4
        line_x1 = col_x(i) + CELL - 4
        if kind == "dim":
            draw.line([(line_x0, line_y), (line_x1, line_y)], fill=MAUVE, width=2)
        else:
            draw.line([(line_x0, line_y), (line_x1, line_y)], fill=RULE, width=1)

    # ───── tile rows ─────
    rows_top = band_top + HEADER_H + 10
    pair_label_font = f(MONO, 13)
    rule_color = (215, 218, 224)

    for ridx, pair in enumerate(PAIRS):
        row_top = rows_top + ridx * (ROW_H + ROWS_VGAP)

        # ── pair label strip ──
        # left rule short stub, then label, then rule fills to right edge
        label_text = pair["label"]
        lw, lh = measure(draw, label_text, pair_label_font)

        ly = row_top + (PAIR_LABEL_H - lh) // 2
        # left short rule
        stub_w = 28
        rule_y = row_top + PAIR_LABEL_H // 2
        draw.line([(PAD_X, rule_y), (PAD_X + stub_w, rule_y)],
                  fill=(180, 184, 192), width=1)
        # label
        lx = PAD_X + stub_w + 14
        draw.text((lx, ly), label_text, font=pair_label_font, fill=TEXT_DIM)
        # right long rule
        rule_x0 = lx + lw + 14
        rule_x1 = PAD_X + GRID_W
        draw.line([(rule_x0, rule_y), (rule_x1, rule_y)], fill=rule_color, width=1)

        # ── tile row ──
        tile_top = row_top + PAIR_LABEL_H + ROW_GAP
        for cidx, fname in enumerate(pair["files"]):
            tile = load_tile(fname, CELL)
            tx = col_x(cidx)
            paste_rounded(canvas, tile, (tx, tile_top), radius=10)

            kind = COLUMN_HEADERS[cidx][2]
            if kind == "dim":
                # mauve ring around the DiM tile
                ring = Image.new("RGBA", (CELL + 10, CELL + 10), (0, 0, 0, 0))
                rd = ImageDraw.Draw(ring)
                rd.rounded_rectangle([1, 1, CELL + 8, CELL + 8],
                                     radius=12, outline=MAUVE + (255,), width=3)
                canvas.alpha_composite(ring, (tx - 5, tile_top - 5))

                # "ours" ribbon in the top-right corner of the tile
                ribbon_text = "OURS"
                rib_font = f(SANS, 10)
                rw, rh = measure(draw, ribbon_text, rib_font)
                pad_x = 7
                pad_y = 4
                rib_w = rw + 2 * pad_x
                rib_h = rh + 2 * pad_y
                rib = Image.new("RGBA", (rib_w, rib_h), MAUVE + (255,))
                rd2 = ImageDraw.Draw(rib)
                # tracked "OURS"
                rd2.text((pad_x, pad_y - 1), ribbon_text,
                         font=rib_font, fill=(255, 255, 255))
                canvas.alpha_composite(rib, (tx + CELL - rib_w, tile_top))

            # caption tag at bottom of the tile (white-on-dark for non-DiM,
            # mauve-deep for DiM)
            tag_text = COLUMN_HEADERS[cidx][0] if kind != "bona" else "Bona fide"
            tag_font = f(SANS, 11)
            tw, th = measure(draw, tag_text.upper(), tag_font)
            tag_pad_x = 8
            tag_pad_y = 4
            tag_w = tw + 2 * tag_pad_x
            tag_h = th + 2 * tag_pad_y
            tag_x = tx + (CELL - tag_w) // 2
            tag_y = tile_top + CELL - tag_h - 8
            if kind == "dim":
                bg_color = MAUVE_DEEP + (235,)
                fg_color = (255, 255, 255)
            else:
                bg_color = (8, 14, 22, 200)
                fg_color = (255, 255, 255, 235)
            tag = Image.new("RGBA", (tag_w, tag_h), (0, 0, 0, 0))
            td = ImageDraw.Draw(tag)
            td.rounded_rectangle([0, 0, tag_w - 1, tag_h - 1],
                                 radius=3, fill=bg_color)
            td.text((tag_pad_x, tag_pad_y - 1), tag_text.upper(),
                    font=tag_font, fill=fg_color)
            canvas.alpha_composite(tag, (tag_x, tag_y))

    # ───── caption ─────
    cap_top = rows_top + 2 * ROW_H + ROWS_VGAP + 24
    # "Figure 4." pill (sans bold in mauve) + italic-serif body
    label_font = f(SERIF_BOLD, 16)
    body_font = f(SERIF_ITALIC, 16)

    cap_label = "Figure 4."
    lw, lh = measure(draw, cap_label, label_font)

    body_text = (
        "Two FRLL identity pairs through six morphing pipelines. "
        "Landmark methods (FaceMorpher, OpenCV) leave ghosting and "
        "pixel-average smearing; GAN methods (StyleGAN2, MIPGAN-II) "
        "introduce identity-bleed artefacts. DiM's morphs sit "
        "in-distribution with the diffusion autoencoder, leaving no "
        "obvious tell."
    )

    # word-wrap to canvas content width
    max_w = CANVAS_W - 2 * PAD_X
    words = body_text.split(" ")
    lines = []
    cur = ""
    for w in words:
        trial = cur + (" " if cur else "") + w
        tw, _ = measure(draw, trial, body_font)
        if tw + lw + 10 > max_w and not lines and cur:
            lines.append(cur)
            cur = w
        elif tw > max_w and cur and lines:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(cur)

    # draw the label on line 1, then body lines
    y = cap_top
    line_h = 22
    if lines:
        draw.text((PAD_X, y), cap_label, font=label_font, fill=MAUVE)
        # first line continues after the label
        first = lines[0]
        draw.text((PAD_X + lw + 6, y), first, font=body_font, fill=TEXT_SECONDARY)
        y += line_h
        for ln in lines[1:]:
            draw.text((PAD_X, y), ln, font=body_font, fill=TEXT_SECONDARY)
            y += line_h

    # final flatten + save
    out = Image.new("RGB", canvas.size, BG_DEEP)
    out.paste(canvas, mask=canvas.split()[3])
    out.save(OUT_PATH, optimize=True)
    print(f"wrote {OUT_PATH}  ({out.size[0]}x{out.size[1]})")


if __name__ == "__main__":
    render()
