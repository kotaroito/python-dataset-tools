import argparse
import os
import glob
import random
from PIL import Image

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('src_dir')
    parser.add_argument('dst_dir')
    parser.add_argument("--crop", action="store_true")
    parser.add_argument("--resize", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    src_dir = os.path.abspath(args.src_dir)
    dst_dir = os.path.abspath(args.dst_dir)

    src_paths = glob.glob("{}/*.jpg".format(src_dir))
    for src_path in src_paths:
        im = Image.open(src_path)
        if args.crop:
            im = crop_max_square(im)
        if args.resize:
            im = im.resize((256, 256))
        im = im.convert('RGB')

        dst_path = os.path.join(dst_dir, os.path.basename(src_path))
        im.save(dst_path)

        if args.verbose:
            print("{} -> {}".format(src_path, dst_path))


'''
The following code references https://github.com/nkmk/python-tools .
'''
def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))

def crop_max_square(pil_img):
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))

if __name__ == '__main__':
    main()
