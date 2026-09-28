"""Generate PWA icons for What's for Dinner."""

from pathlib import Path

from PIL import Image, ImageDraw

OUT = Path("static/icons")
OUT.mkdir(parents=True, exist_ok=True)

CREAM = (250, 244, 240, 255)
ROSE = (225, 161, 168, 255)
TERRACOTTA = (204, 120, 89, 255)
SAGE = (163, 181, 158, 255)
GOLD = (217, 173, 92, 255)


def draw_icon(size, maskable=False):
    """Draw a plate on a cream background. Maskable uses safe zone padding."""
    img = Image.new("RGBA", (size, size), CREAM)
    d = ImageDraw.Draw(img)

    # Maskable icons need all content within the center 80%
    safe = 0.8 if maskable else 0.92
    pad = size * (1 - safe) / 2
    usable = size - 2 * pad

    # Plate
    plate = [pad, pad, pad + usable, pad + usable]
    d.ellipse(plate, fill=(255, 255, 255, 255))

    # Rim
    rim_width = max(2, int(size * 0.015))
    d.ellipse(plate, outline=ROSE, width=rim_width)

    # Food
    food_pad = pad + usable * 0.18
    food_size = usable * 0.64
    food = [food_pad, food_pad, food_pad + food_size, food_pad + food_size]
    d.ellipse(food, fill=ROSE)

    # Garnishes
    g1_size = usable * 0.14
    g1_pos = (pad + usable * 0.28, pad + usable * 0.55)
    d.ellipse(
        [g1_pos[0], g1_pos[1], g1_pos[0] + g1_size, g1_pos[1] + g1_size],
        fill=SAGE,
    )

    g2_size = usable * 0.12
    g2_pos = (pad + usable * 0.58, pad + usable * 0.30)
    d.ellipse(
        [g2_pos[0], g2_pos[1], g2_pos[0] + g2_size, g2_pos[1] + g2_size],
        fill=TERRACOTTA,
    )

    g3_size = usable * 0.10
    g3_pos = (pad + usable * 0.50, pad + usable * 0.62)
    d.ellipse(
        [g3_pos[0], g3_pos[1], g3_pos[0] + g3_size, g3_pos[1] + g3_size],
        fill=GOLD,
    )

    return img


sizes = [
    ("icon-192.png", 192, False),
    ("icon-512.png", 512, False),
    ("maskable-192.png", 192, True),
    ("maskable-512.png", 512, True),
]

for name, size, maskable in sizes:
    img = draw_icon(size, maskable)
    path = OUT / name
    img.save(path, "PNG", optimize=True)
    print(f"wrote {path} ({path.stat().st_size} bytes)")
