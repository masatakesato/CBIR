# CBIR

A Simple visual search application prototyping content-based retrieval apllication.

https://user-images.githubusercontent.com/12041845/209619219-ab8e239e-98aa-42d4-a085-6ac181cebc42.mp4
Images by ["TinySets development team" - "LEGO Minifigures".](https://www.kaggle.com/datasets/ihelon/lego-minifigures-classification) / Adapted.
Videos by ["Cafi Net" - "waterfall-free_video".](https://japanism.info/photo-rule.html#rule)

## About

Purpose: Investigating unstructured data retrieval system. Get accustomed to TF2 programming.

## Features

- image and video similarity search

- feature extraction using pretrained convolutional neural networks

- tcp server/client model

- Pyqt client application

## Requirements

Python environment with following configurations is required to run the program. Please refer to "tf250gpu.yml".

- ffmpeg 4.3.1

- matplotlib 3.6.2

- msgpack-python 1.0.4

- numpy 1.22.4

- pillow 9.3.0

- pyqt 5.12.3

- python 3.9.15

- scikit-learn 1.1.2

- sk-video 1.1.10

- tensorflow 2.5.0(gpu version)

- tensorflow-hub 0.12.0

## Running application

Setup
  指定ディレクトリ内をスキャンして、画像/動画ファイルのインデックスを作成する
　preprocessディレクトリ内、下記順番に

- Configuring preprocess
  -config.json、
  　
- Creating directory snapshot
  　python create_snapshot.py
- Data wrangling
  　python wrangle_images.py
- Feature extraction
  　python extract_image_features.py
- Thumbnail creation
  　python create_thumbnails.py

+++++ Running application +++++

- Specifying Index path
- Run standalone version
- Run server-client version
  　separately

++++ References ++++
