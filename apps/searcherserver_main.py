import os
import argparse
import pathlib
import json
import traceback


from import_engine import *
import oreorepylib.utils.environment
import oreorepylib.network.tcp as tcp
from searchengine import SearchEngine




class SearcherServer( SearchEngine ):

    def __init__( self, *args, **kwargs ):
        super(SearcherServer, self).__init__(args, kwargs)


    def echo(self):
        return "echo"



if __name__ == '__main__':
    
    try:

        #========= Set current directory to this file's ========#
        #path_currfile = pathlib.Path(__file__).parent.resolve()
        os.chdir( package_dir )


        #========== Load server address from argumens ==========#
        parser = argparse.ArgumentParser()
        parser.add_argument( "--host", type=str, default="localhost" )
        parser.add_argument( "--port", type=int, default=8080 )

        args = parser.parse_args()

        if( not ( args.host and args.port ) ):
            print( "Abrting server startup. please specify proper --host and --port.")
            quit()


        #=========== Load index path from config.json ========#
        path_config = package_dir / "config.json"

        with open( path_config, "r", encoding="utf-8_sig" ) as f:
            settings = json.load(f)
        path_index = pathlib.Path( settings["index_path"] )


        #=============== Start searchengine server =============#
        searcher = SearcherServer()
        searcher.Init( path_index, "https://tfhub.dev/google/imagenet/inception_v3/feature_vector/5", [None, 299, 299, 3] )
 
        #server = tcp.Server( searcher )
        #server = tcp.SSLServer( searcher )
        server = tcp.ServerThreading( searcher )
        #server = tcp.ServerPrethreading( searcher )

        server.listen( args.host, args.port, backlog=10 )
        server.run()

    except KeyboardInterrupt:
        traceback.print_exc()
        server.close()






    