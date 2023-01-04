import os
import json
import pathlib
from PIL import Image

from import_engine import *
from searchengine import SearchEngine



def AlignImage( pil_img, img_size, background_color ):

    # Crop to square
    width, height = pil_img.size
    img_cropped = None

    if width == height:
        img_cropped = pil_img
    elif width > height:
        img_cropped = Image.new( pil_img.mode, (width, width), background_color )
        img_cropped.paste( pil_img, (0, (width - height) // 2) )
    else:
        img_cropped = Image.new( pil_img.mode, (height, height), background_color )
        img_cropped.paste( pil_img, ((height - width) // 2, 0) )
    
    # Resize
    return img_cropped.resize( img_size, Image.BILINEAR )# resize image



path_query = pathlib.Path( "./data/query.png" )
path_config = pathlib.Path( "./config.json" )
path_index = pathlib.Path( "../index" )


if __name__ == '__main__':

    #============= Initialize search engine ================#
    searcher = SearchEngine()
    searcher.Init( path_index, "https://tfhub.dev/google/imagenet/inception_v3/feature_vector/5", [None, 299, 299, 3] )


    #============= Setup query image data ==================#
    input_shape = searcher.InputShape()
    img_size = ( input_shape[2], input_shape[1] )

    query_img = Image.open( str(path_query) ).convert("RGB")
    query_img = AlignImage( query_img, img_size, (0,0,0) )
        
    pixel_data = list( query_img.getdata() )


    #============= Setup query image data ==================#
    results = searcher.Search( [ pixel_data ] )
    for i in range(10):
        p = pathlib.Path( results[i][2] )
        print( p )

    