import glob
from PIL import Image

covers = glob.glob('covers/*.jpg')

for cover in covers:
    with Image.open(cover) as image:

        # Get image_size
        image_size = image.size

        # Print image size
        print(f'{image_size} of "{cover}"')
        print(f'{image_size[0]} x {image_size[1]}')
        width = image_size[0]
        height = image_size[1]

        (left, upper, right, lower) = (100, 190, width-105, height-15)

        im_crop = image.crop((left, upper, right, lower))

        im_crop.save(f'normalized-{cover}')