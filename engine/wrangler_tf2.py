import os
os.environ["TF_FORCE_GPU_ALLOW_GROWTH"] = "true"#limit tensorflow gpu memory consumption

import traceback
import math
import pathlib
import numpy as np
import skvideo.io
import tensorflow as tf




# generator version. avoiding out-of-memory.
def TF_ResizeAndCrop_gen( batch_size, img_gen ):

    out_size = (299, 299)

    def procImageBatch( img_arr ):       
        crop_size = max( img_arr.shape[1], img_arr.shape[2] )
        img_arr = tf.image.resize_with_crop_or_pad( img_arr, crop_size, crop_size )# crop
        img_arr = tf.image.resize( img_arr, out_size, method = tf.image.ResizeMethod.BILINEAR, preserve_aspect_ratio=True, antialias=True )#resize
        return img_arr

    img_array = []
    img_batches = []

    try:
        for i, frame in enumerate(img_gen):
            img_array.append( frame )
        
            if( len(img_array) % batch_size == 0 ):
                print( 'TF_ResizeAndCrop_gen...Processing videoframe batch: %d' % len(img_array) )
                img_batches.append( procImageBatch( np.stack( img_array, axis=0 ) ) )
                img_array.clear()

    except:
        traceback.print_exc()
        

    if( img_array ):
       print( 'TF_ResizeAndCrop_gen...Processing videoframe batch: %d' % len(img_array) )
       img_batches.append( procImageBatch( np.stack( img_array, axis=0 ) ) )
       img_array.clear()

    return np.concatenate( img_batches )




class MovieWrangler:

    def __init__( self, batch_size ):
        self.batch_size = batch_size



    def run( self, file_path ):
        
        try:
            print( '//========= Processing file: %s =========//' % file_path )
            video_gen = skvideo.io.vreader( file_path ) # 一括で読み込むとメモリ足りなくなる場合あり
            img_processed = TF_ResizeAndCrop_gen( self.batch_size, video_gen )

            return img_processed

        except:
            traceback.print_exc()
            return None
