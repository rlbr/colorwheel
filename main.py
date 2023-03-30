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


def draw_shape(draw, x0, y0, h, i):
    r = radius(h)
    x, y = circle_center(h, i)
    color = ImageColor.getrgb(f"hsl({360//12 * i}, {int(100 * .5 ** j)}%, 50%)")
    draw.ellipse(((x0 + x - r, y0 + y - r), (x0 + x + r, y0 + y + r)), color)


def shrink(img: Image.Image, size):

    return img.resize(size, Image.LANCZOS)


def place_img(base: Image, img: Image, x0, y0, h, i):
    working_copy = img.copy()
    r = int(radius(h))
    working_copy = shrink(working_copy, (r * 2, r * 2))
    x, y = circle_center(h, i)
    # coords = [int(v) for v in (x0 + x - r, y0 + y - r, x0 + x + r, y0 + y + r)]
    coords = tuple((int(v) for v in (x0 + x - r, y0 + y - r)))

    circle_crop(working_copy)
    base.paste(working_copy, coords, working_copy)


s = 3
img = Image.new("RGBA", (1200 * s, 1200 * s))
base = img.copy()
draw = ImageDraw.Draw(img)
h0 = 460 * s
x0 = 600 * s
y0 = 600 * s
h = h0
mf = Image.open("./middle_finder.jpg")

for j in range(11):
    for i in range(12):

        draw_shape(draw, x0, y0, h, i)
        place_img(base, mf, x0, y0, h, i)

    h = next_h(h)

with open("out.png", "wb") as im:
    img.save(im)

with open("out2.png", "wb") as im2:
    base.save(im2)
