import os
import pathlib
import json
import traceback
import numpy as np

from import_engine import *
from featureextractor_tf2 import FeatureExtractor



if __name__=='__main__':

    try:

        #========= Set current directory to this file's ========#
        os.chdir( package_dir )


        #============== Setup features directory ===============#
        path_settings = package_dir / "config.json"

        with open( path_settings, "r", encoding="utf-8_sig" ) as f:
            settings = json.load(f)

        index_path = pathlib.Path( settings["index_path"] )
        path_wrangled = index_path / "wrangled"
        path_features = index_path / "features"

        if( not( path_features.exists() and path_features.is_dir() ) ):
            path_features.mkdir()


        #===== Extract faeature vectores from wrangled image/movie data =====#
        extractor = FeatureExtractor( "https://tfhub.dev/google/imagenet/inception_v3/feature_vector/5", [ None, 299, 299, 3 ] )

        paths_img = path_wrangled.glob( "**/*.npy" )

        filepath_log = path_features / "features.log"
        batch_size = 10
        log_strings = []

        for path in paths_img:
            try:
                print( "//================ processing %s ================//" % path.name )
            
                # Load npz image array
                img_array = np.load( str(path) ).astype(np.float32) / 255.0 # must be normalized because of model specification
            
                # Extract feature vectors
                features = extractor.RunBatch( img_array, batch_size )

                # Save features to npy
                print( "    saving features to: %s" % path.name )
                np.save( path_features / path.stem, features )

            except:
                log_strings.append( traceback.format_exc() )


        filepath_log.touch()
        filepath_log.write_text( "\n".join( log_strings ), encoding="utf-8" )


    except:

        traceback.print_exc()