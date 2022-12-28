# CBIR

Content-based image/video retrieval apllication using pre-trained CNN.

<p align="center" >
  <video width="100%" controls src="https://user-images.githubusercontent.com/12041845/209619219-ab8e239e-98aa-42d4-a085-6ac181cebc42.mp4">
  </video>
</p>

Images by ["TinySets development team" - "LEGO Minifigures".](https://www.kaggle.com/datasets/ihelon/lego-minifigures-classification) / Adapted.
Videos by ["Cafi Net" - "waterfall-free_video".](https://japanism.info/photo-rule.html#rule)

## About

This repository contains experimental implementation of image/video visual search application. The application retrieves images/videos similar to query from database. I used feature vectors extracted from pre-trained CNN( convolutional neural network ) for similarity measurement.

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

<p align="center" >
  <img width="70%" src="https://user-images.githubusercontent.com/12041845/209782968-c0402a44-3240-4cf4-aeb7-bc1a2c50d576.svg">
</p>

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
