import argparse
import os
import glob
import random
import shutil

def set_seed(seed):
    random.seed(seed)

def random_split(a):
    random.shuffle(a)
    size = len(a)
    i1  = int(size * 0.1)
    i2  = int(size * 0.2)

    train = a[i2:]
    valid = a[i1:i2]
    test  = a[0:i1]

    return (train, valid, test)

def create_labeled_image_dataset(outdir, filename, image_label_list):
    with open(os.path.join(outdir, filename), 'w') as f:
        for src_path, idx, label in image_label_list:
            basename = os.path.basename(src_path)
            dst_path = os.path.join(outdir, 'images', "{}_{}".format(label, basename))

            f.write("{} {}\n".format(dst_path, idx))
            shutil.copyfile(src_path, dst_path)

def create_label_txt(outdir, filename, label_idx_list):
    with open(os.path.join(outdir, filename), 'w') as f:
        for label, idx in label_idx_list:
            f.write("%d %s\n" % (idx, label))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dir')
    parser.add_argument('--out', default='.')
    parser.add_argument('--seed', default=0)
    args = parser.parse_args()

    dir = args.dir
    outdir = os.path.abspath(args.out)
    set_seed(args.seed)

    # create outdir/images dir
    if not os.path.exists(os.path.join(outdir, "images")):
        os.mkdir(os.path.join(outdir, "images"))

    # get labels as dir name
    labels = sorted(os.listdir(dir))

    # start to create dataset
    image_label_list = []
    label_idx_list = []
    for idx, label in enumerate(labels):
        image_paths = glob.glob(os.path.join(dir, label, '*.jpg'))
        image_label_list.extend([(img_path, idx, label) for img_path in image_paths])
        label_idx_list.append((label, idx))

    (train_ds, valid_ds, test_ds) = random_split(image_label_list)
    create_labeled_image_dataset(outdir, 'train.txt', train_ds)
    create_labeled_image_dataset(outdir, 'valid.txt', valid_ds)
    create_labeled_image_dataset(outdir, 'test.txt', test_ds)
    create_label_txt(outdir, 'label.txt', label_idx_list)

if __name__ == '__main__':
    main()
