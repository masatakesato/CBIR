# preview numpy images
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation



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