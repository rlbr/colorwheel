import math
from PIL import Image, ImageDraw, ImageColor, ImageOps, ExifTags
from load_images import image_paths


def fix_rotation(image):
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == "Orientation":
                break

        exif = image.getexif()

        if exif[orientation] == 3:
            image = image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image = image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image = image.rotate(90, expand=True)

    except (AttributeError, KeyError, IndexError):
        pass
    return image


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


s = 6
img = Image.new("RGBA", (1200 * s, 1200 * s))
base = Image.new("RGBA", (1200 * s, 1200 * s))
draw = ImageDraw.Draw(img)
h0 = 460 * s
x0 = 600 * s
y0 = 600 * s
h = h0


for j in range(11):
    tier = j % 4
    for i in range(12):
        print(f"j={j},i={i}")

        images = image_paths[tier]
        image_no = i % len(images)
        image_path = images[image_no]

        loaded_image = Image.open(image_path)
        roation_fixed = fix_rotation(loaded_image)
        gs = ImageOps.grayscale(loaded_image).convert("RGBA")
        draw_shape(draw, x0, y0, h, i)
        place_img(base, gs, x0, y0, h, i)
        loaded_image.close()

    h = next_h(h)

with open("out.png", "wb") as im:
    img.save(im)

with open("out2.png", "wb") as im2:
    base.save(im2)

blended = Image.blend(base, img, 0.5)

with open("out3.png", "wb") as im3:
    blended.save(im3)
