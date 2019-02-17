# Caltech 101 dataset

## Download

First of all, let's  download the original dataset.

```bash
curl -LO http://www.vision.caltech.edu/Image_Datasets/Caltech101/101_ObjectCategories.tar.gz
tar zxvf 101_ObjectCategories.tar.gz
```

## Create dataset files for chainer

```bash
python caltech101/create_dataset.py 101_ObjectCategories --out [out_dir]
```

After that, you will get the following files.

```bash
$ ls [out_dir]
images    label.txt test.txt  train.txt valid.txt
```

## Crop images

Then, crop images.

```bash
python caltech101/crop_image.py [out_dir] [out_dir]
```
