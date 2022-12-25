from Preview import Plt_Preview
from Wrangler_tf2 import MovieWrangler
import pathlib
import numpy as np


src_path = pathlib.Path( "V:/testVideoDataset/waterfall-free-video2.mp4" )
npy_path = pathlib.Path( "./test_out.npy" )



if __name__=="__main__":
    
    wrangler = MovieWrangler( 50 )
        
    np_data = wrangler.run( str(src_path) )
        
    if( np_data.any() ):
        # Save as npy
        np.save( npy_path, np_data.astype( np.uint8 ) )
        print( "    Saved result to: %s" % npy_path.name )

        # Preview        
        Plt_Preview( npy_path )