import math
from PIL import Image, ImageDraw, ImageColor


def radius(h):
    return h * math.sin(math.pi / 12)


def circle_center(h, n):
    x = math.cos(math.pi / 6 * n) * h
    y = math.sin(math.pi / 6 * n) * h
    return (x, y)


def next_h(h):
    r = radius(h)
    return h - r - r * 0.6


def circle_crop(image: Image):
    size = image.size
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)
    image.putalpha(mask)


s = 6
img = Image.new("RGBA", (1200 * s, 1200 * s))
draw = ImageDraw.Draw(img)
h0 = 460 * s
x0 = 600 * s
y0 = 600 * s
h = h0
for j in range(11):
    for i in range(12):
        r = radius(h)
        x, y = circle_center(h, i)
        color = ImageColor.getrgb(f"hsl({360//12 * i}, {int(100 * .5 ** j)}%, 50%)")
        draw.ellipse(((x0 + x - r, y0 + y - r), (x0 + x + r, y0 + y + r)), color)
    h = next_h(h)

with open("out.png", "wb") as im:
    img.save(im)
