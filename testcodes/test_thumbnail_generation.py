import pathlib

from thumbnailgenerator import ThumbnailGenerator


path_wrangled = pathlib.Path( "../data/wrangled" )
path_features = pathlib.Path( "../data/features" )



if __name__=="__main__":
    
    path_feature = path_features / "0.npy"
    path_thumbnail = pathlib.Path("./testout.gif")

    generator = ThumbnailGenerator()
    generator.Generate( path_thumbnail, path_wrangled / path_feature.name, path_feature )