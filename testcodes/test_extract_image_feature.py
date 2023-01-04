import os
import pathlib
import json
import traceback
import numpy as np

from import_engine import *
from featureextractor_tf2 import FeatureExtractor



path_wrangled = pathlib.Path( "./testout/test_wrangled.npy" )
path_feature = pathlib.Path( "./testout/test_feature.npy" )


if __name__=='__main__':

    try:

        #========= Set current directory to this file's ========#
        os.chdir( package_dir )


        #===== Extract faeature vectores from wrangled image/movie data =====#
        extractor = FeatureExtractor( "https://tfhub.dev/google/imagenet/inception_v3/feature_vector/5", [ None, 299, 299, 3 ] )
            
        # Load npy image array
        img_array = np.load( str(path_wrangled) ).astype(np.float32) / 255.0 # must be normalized because of model specification
            
        # Extract feature vectors
        features = extractor.RunBatch( img_array )

        # Save features to npy
        print( "    saving features to: %s" % path_feature.name )
        np.save( path_feature, features )




    except:

        traceback.print_exc()