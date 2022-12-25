import os
import pathlib
import json
import traceback
import numpy as np

from snapshot import Snapshot
from wrangler_tf2 import MovieWrangler



if __name__=='__main__':
    
    try:

        #========= Set current directory to this file's ========#
        path_currfile = pathlib.Path(__file__).parent.resolve()
        os.chdir( path_currfile )


        #================ Setup wrangled directory =============#
        path_settings = path_currfile / "settings.json"

        with open( path_settings, "r", encoding="utf-8_sig" ) as f:
            settings = json.load(f)

        index_path = pathlib.Path( settings["index_path"] )
        wrangled_path = index_path / "wrangled"

        if( not( wrangled_path.exists() and wrangled_path.is_dir() ) ):
            wrangled_path.mkdir()


        #==== Create wrangled media data and store to "wrangled" directory. =====#
        snapshot = Snapshot()
        snapshot.Import( index_path / "snapshot.pkl" )

        wrangler = MovieWrangler( 50 )
    
        filepath_log = wrangled_path / "wrangled.log"
        log_strings = [ "[ Wrangling failed at... ]" ]


        for i, info in enumerate( snapshot.FileInfos() ):
            # wrangle video data
            np_data = wrangler.run( info.FilePath() )

            if( np_data is None ):
                log_strings.append( "%d: %s" % ( i, str(info.FilePath()) ) )
                continue

            # Save wrangled date to npy
            file_name = "%s.npz" % i
            print( "    Saving result to: %d.npy" % i )
            np.save( wrangled_path / str(i), np_data.astype( np.uint8 ) )


        filepath_log.touch()
        filepath_log.write_text( "\n".join( log_strings ), encoding="utf-8" )


    except:
        traceback.print_exc()
        quit()