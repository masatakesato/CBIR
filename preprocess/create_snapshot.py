import os
import json
import traceback

from import_engine import *
from crawler import FileCrawler



if __name__=="__main__":

    try:

        #========= Set current directory to this file's ========#
        os.chdir( package_dir )


        #=========== Load Crawl config from json ===============#
        path_settings = package_dir / "settings.json"

        # https://qiita.com/Yuu94/items/9ffdfcb2c26d6b33792e windowsだとエンコードで引っかかる
        with open( path_settings, "r", encoding="utf-8_sig" ) as f:
            settings = json.load(f)

        search_paths = settings["search_paths"]
        types = settings["types"]

        print( search_paths )
        print( types )



        #========= Crawl directory and gather fileinfo =========#
        dirCrawler = FileCrawler( search_paths, types )
        snapshot = dirCrawler.Run()
        snapshot.Info()


        #==================== Output snapshot ==================#

        # Create index directory if not exists.
        index_path = pathlib.Path( settings["index_path"] )
        print( index_path )
        if( not( index_path.exists() and index_path.is_dir() ) ):
            index_path.mkdir()

        # Save snapshot file
        out_path = index_path / "snapshot.pkl"#"%s/%s.pkl" % (path_output, snapshot.DateTime().strftime("%Y%m%d-%H%M%S") )
        snapshot.Export( out_path )


    except:

        traceback.print_exc()