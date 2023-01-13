import sys
import argparse

from import_engine import *
import oreorepylib.network.tcp as tcp

from clientwidget import *



class SearcherClient( tcp.Client ):

    def __init__( self, host, port ):
        super().__init__( host, port, 60, 5 )
        #self.client = tcp.Client( host, port, 60, 5 )
    
    #def IsReady( self ):
    #    print("hshgsfd")
    #    return tcp.Client.IsReady()


    def InputShape( self, *argc, **argv ):
        #if( self.IsReady() ):
        return self.call( "InputShape" )
        #return (0, 0, 0)


    def GetThumbnailStream( self, *argc, **argv ):
        #if( self.IsReady() ):
        return self.call( "GetThumbnailStream", *argc, **argv )
        #return None


    def GetThumbnailStreams( self, *argc, **argv ):
        #if( self.IsReady() ):
        return self.call( "GetThumbnailStreams", *argc, **argv )
        #return None


    def Search( self, *argc, **argv ):
        #if( self.IsReady() ):
        return self.call( "Search", *argc, **argv )
        #return [], []





if __name__=="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument( "--host", type=str, default="localhost" )
    parser.add_argument( "--port", type=int, default=8080 )

    args = parser.parse_args() 

    host = args.host
    port = args.port

    searcher = SearcherClient( host, port )

    app = QApplication(sys.argv)

    mainWidget = ClientWidget( searcher )
    mainWidget.show()

    sys.exit(app.exec_())
