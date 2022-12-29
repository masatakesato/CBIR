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

- Image and video similarity search

- Feature extraction using pre-trained CNN

- tcp server/client model

- Pyqt client application

## Requirements

Python environment with following configurations is required to run the program. Please refer to **<u>tf250gpu.yml</u>**.

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

## Building application

Before running visual search application, you need to set up index data. All the required procedures are included in "preprocess" directory. Below figure shows an brief flow of  preprocessing.

<p align="center" >
  <img width="70%" src="https://user-images.githubusercontent.com/12041845/209782968-c0402a44-3240-4cf4-aeb7-bc1a2c50d576.svg">
</p>

### Path cofiguration

Open "config.json" and edit the following values. Please refer to **<u>preprocess/config.json</u>**.

- search_paths: Directories to be include in retrieval

- types: File extensions to be included in retrieval

- index_path: Directory to output indexing result

### Preprocessing

After finishing config.json setup, you need to execute python scripts in the following order.

1. create_snapshot.py
2. wrangle_images.py
3. extract_image_features.py
4. create_thumbnails.py

## Running application

Application scrips are stored in "apps" directory.

### Path configuration

Open "config.json" and edit the following values. Please refer to **<u>apps/config.json</u>**.

- index_path: Path to the index directory ( created in "Building apllication" step )

### Run standalone version

Please execute following python script.

- searcherstandalone_main.py

### Run server-client version

Another implementation example using tcp client-server model. The client deals with query through GUI operation. The server runs retrieval process. Please execute following scripts separately.

- searcherserver_main.py

- searcherclient_main.py
