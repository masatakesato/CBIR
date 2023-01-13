from fileinfo import FileInfo
from snapshot import Snapshot


import traceback
import pathlib
import pickle



class FileCrawler:

    def __init__( self, search_paths=[], types=[] ):
        super().__init__()

        self.__m_SearchPaths = [ pathlib.Path(r) for r in search_paths ]
        self.__m_Types = types
    

    #============= Register/Unregister search directories ==============#
    def AddRootDir( self, search_path ):
        self.__m_Types.append( search_path )
        self.__m_Types = list(set(self.__m_Types))# resolve redundancy


    def AddRootDirs( self, roots ):
        self.__m_Types += roots
        self.__m_Types = list(set(self.__m_Types))# resolve redundancy


    def RemoveRootDir( self, dir ):
        try:
            self.__m_SearchPaths.remove( dir )
        except:
            traceback.print_exc()

    
    def RemoveRootDirs( self, roots ):
        try:
            self.__m_SearchPaths = [ r for r in self.__m_SearchPaths if not r in roots ]
        except:
            traceback.print_exc()


    def ClearRootDirs( self ):
        self.__m_SearchPaths.clear()


    #============= Register/Unregister file types ==============#
    def AddType( self, type ):
        self.__m_Types.append( type )
        self.__m_Types = list(set(self.__m_Types))# resolve redundancy


    def AddTypes( self, types ):
        self.__m_Types += types
        self.__m_Types = list(set(self.__m_Types))# resolve redundancy


    def RemoveType( self, type ):
        try:
            self.__m_Types.remove( type )
        except:
            traceback.print_exc()


    def RemoveTypes( self, types ):
        try:
            self.__m_Types = [ r for r in self.__m_Types if not r in types ]
        except:
            traceback.print_exc()


    def ClearTypes( self ):
        self.__m_Types.clear()


    #============= Crawl ==============#
    def Run( self ):
        
        def unique(sequence):# remove duplications while preserving order http://www.martinbroadhurst.com/removing-duplicates-from-a-list-while-preserving-order-in-python.html
            seen = set()
            return [x for x in sequence if not (x in seen or seen.add(x))]

        fileInfos = []# FileInfo object array
        
        # Gether filepathes
        paths = []
        for path in self.__m_SearchPaths:
            for type in self.__m_Types:
                paths.extend( list( path.glob( "**/*.%s" % type ) ) )

        paths = unique(paths)
        #for i, path in enumerate(paths): print( '%d: %s' % ( i, path ) )

        # Gather FileInfo
        fileInfos = [ FileInfo(p) for p in paths ]

        
        return Snapshot( [str(p) for p in self.__m_SearchPaths], self.__m_Types, fileInfos )


    #================ Info ==============#
    def Info( self ):

        print( "//========== FileCrawler Info... ==========//" )
        print( "Registered Root Dirs:" )
        for path in self.__m_SearchPaths:
            print( '  %s' % path )

        print( "Scan data types:" )
        for type in self.__m_Types:
            print( "  %s" % type )



#======================= test code ===========================#

#if __name__=='__main__':

    
#    types = [ '**/*.*' ]
#    search_paths = [ './' ]

#    crawler = FileCrawler( search_paths=search_paths, types=types )

#    snapshot = crawler.Run()

#    #snapshot.Info()

#    snapshot.Export( './snapshot.pkl' )
    
#    snapshot_copy = Snapshot()
#    snapshot_copy.Import( './snapshot.pkl' )
#    snapshot_copy.Info()


#    snapshot2 = crawler.Run()
#    snapshot2.Export( './snapshot2.pkl' )
#    snapshot2.Compare( snapshot )