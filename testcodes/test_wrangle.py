import pathlib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from import_engine import *
from wrangler_tf2 import MovieWrangler



src_path = pathlib.Path( "./data/test.mp4" )
npy_path = pathlib.Path( "./testout/test_wrangled.npy" )


def Plt_Preview( path ):

    fig = plt.figure()
    img_array = np.load( str(path) )
    
    #print( "%f [GB]" % ( img_array.size * img_array.itemsize / 1024**3 ) )

    imgs = []
    for img in img_array:
        im = plt.imshow( img )
        imgs.append( [im] )
   
    anim = animation.ArtistAnimation( fig, imgs, interval=1 )
    plt.show()#plt.pause(5)


#import matplotlib.pyplot as plt
#from matplotlib.animation import ArtistAnimation
#import numpy as np
#fig, ax = plt.subplots()
#artists = []
#x = np.arange(10)
#for i in range(10):
#    y = np.random.rand(10)
#    im = ax.plot(x, y)
#    artists.append(im)
#anim = ArtistAnimation(fig, artists, interval=1000)
#plt.show()






if __name__=="__main__":
    
    wrangler = MovieWrangler( 50 )
        
    np_data = wrangler.run( str(src_path) )
        
    if( np_data.any() ):
        # Save as npy
        np.save( npy_path, np_data.astype( np.uint8 ) )
        print( "    Saved result to: %s" % npy_path.name )

        # Preview
        Plt_Preview( npy_path )