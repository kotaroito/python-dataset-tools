import argparse
import os
import glob
import random
import shutil

'''
Caltech-101:
Follow the procedure of (Fei-feiet al., 2006) and randomly select 30 images perclass for training and test on up to 50 images per class.
'''

def set_seed(seed):
    random.seed(seed)

def split_train_valid(a):
    random.shuffle(a)

    train = a[0:30]
    valid = a[30:80]

    return (train, valid)

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

    # get object categories
    labels = sorted([d for d in os.listdir(dir) if not d == 'BACKGROUND_Google'])

    train_ds = []
    valid_ds = []
    label_ds = []

    # select train/valid set
    for i, label in enumerate(labels):
        image_paths = glob.glob(os.path.join(dir, label, '*.jpg'))
        t, v = split_train_valid([(img_path, i, label) for img_path in image_paths])
        train_ds.extend(t)
        valid_ds.extend(v)
        label_ds.append((label, i))


    # shuffle train dataset
    random.shuffle(train_ds)

    # create txt files
    create_labeled_image_dataset(outdir, 'train.txt', train_ds)
    create_labeled_image_dataset(outdir, 'valid.txt', valid_ds)
    create_label_txt(outdir, 'label.txt', label_ds)

if __name__ == '__main__':
    main()
