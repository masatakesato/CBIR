import pathlib

from import_engine import *
from thumbnailgenerator import ThumbnailGenerator


path_wrangled = pathlib.Path( "./testout/test_wrangled.npy" )
path_feature = pathlib.Path( "./testout/test_feature.npy" )
path_thumbnail = pathlib.Path( "./testout/test_thumbnail.gif" )


if __name__=="__main__":
    
    generator = ThumbnailGenerator()
    generator.Generate( path_thumbnail, path_wrangled, path_feature )