import os
import sys
import pathlib
import json

from import_engine import *
from searchengine import SearchEngine
from clientwidget import *



if __name__=='__main__':

    #========= Set current directory to this file's ========#
    os.chdir( package_dir )


    #=========== Load index path from settings.json ========#
    path_settings = package_dir / "settings.json"

    with open( path_settings, "r", encoding="utf-8_sig" ) as f:
        settings = json.load(f)
    path_index = pathlib.Path( settings["index_path"] )


    #=================== Start searchengine =================#
    searcher = SearchEngine()
    searcher.Init( path_index, "https://tfhub.dev/google/imagenet/inception_v3/feature_vector/5", [None, 299, 299, 3] )


    #====================== Start widget ====================#
    app = QApplication(sys.argv)

    mainWidget = ClientWidget( searcher )
    mainWidget.show()

    sys.exit(app.exec_())
