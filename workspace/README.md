# CBIR

Content-based image/video retrieval apllication using pre-trained CNN.

<p align="center" >
  <video width="100%" controls src="https://github.com/masatakesato/CBIR/blob/main/media/VisualSearchDemo.mp4?raw=true">
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

Python environment with following configurations is required to run the program. Please refer to [**tf250gpu.yml**](https://github.com/masatakesato/CBIR/blob/main/tf250gpu.yml).

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

## Setup

Before running visual search application, you need to set up index data. All the required procedures are included in [**preprocess**](https://github.com/masatakesato/CBIR/tree/main/preprocess) directory. Below figure shows a preprocess flow.

<p align="center" >
  <img width="70%" src="https://raw.githubusercontent.com/masatakesato/CBIR/main/media/preprocess_flow.svg">
</p>

### Path cofiguration

Open "config.json" and edit the following values. Please refer to [**preprocess/config.json**](https://github.com/masatakesato/CBIR/blob/main/preprocess/config.json).

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

Application scrips are stored in [**apps**](https://github.com/masatakesato/CBIR/tree/main/apps) directory.

### Path configuration

Open "config.json" and edit the following values. Please refer to [**apps/config.json**](https://github.com/masatakesato/CBIR/blob/main/apps/config.json).

- index_path: Path to the index directory ( created in "Setup" step )

### Run standalone version

Please execute following python script.

- searcherstandalone_main.py

### Run server-client version

Another implementation example using tcp client-server model. The client deals with query through GUI operation. The server runs retrieval process. Please execute following scripts separately.

- searcherserver_main.py

- searcherclient_main.py
