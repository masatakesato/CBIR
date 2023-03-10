import os
import pathlib
import json
import traceback

from import_engine import *
from thumbnailgenerator import ThumbnailGenerator



if __name__=="__main__":

    try:

        #========= Set current directory to this file's ========#
        os.chdir( package_dir )


        #============== Setup features directory ===============#
        path_config = package_dir / "config.json"

        with open( path_config, "r", encoding="utf-8_sig" ) as f:
            settings = json.load(f)

        path_index = pathlib.Path( settings["index_path"] )
        path_wrangled = path_index / "wrangled"
        path_features = path_index / "features"
        path_thumbnails = path_index / "thumbnails"

        if( not( path_thumbnails.exists() and path_thumbnails.is_dir() ) ):
            path_thumbnails.mkdir()


        #================= Generate thumbnails =================#
        generator = ThumbnailGenerator()
        generator.GenerateBatch( path_thumbnails, path_wrangled, path_features )
 
 
    except:

        traceback.print_exc()