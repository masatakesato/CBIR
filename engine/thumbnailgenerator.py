import traceback
import pathlib
import numpy as np
from PIL import Image



class ThumbnailGenerator:

    __window_size = 2


    def Generate( self, thumbnail_path, wrangled_image_path, feature_path ):
        try:

            print( "Generating thumbnail %s ..." % str(thumbnail_path), end="" )

            feature_batch = np.load( feature_path )

            #print( feature_batch )
            #print( feature_batch[:,1] )# これで列成分だけ取得できる

            #================= 移動平均を出す ================#
            vec_mvavg = []
            b = np.ones( self.__window_size ) / self.__window_size
            for dim in range(feature_batch.shape[1]):
                vec_mvavg.append( np.convolve( feature_batch[:,dim], b, "same" ) )

            vv = np.array( vec_mvavg ).transpose()

            #========= 隣接特徴量間の距離順にソートする =======#
            norms = np.linalg.norm( vv, axis=-1 )
    
            ds = []
            for i in range( vv.shape[0]-1 ):
                i_next = min( i+1, vv.shape[0]-1 )
                i_prev = max( i-1, 0 )
                forward = np.dot( vv[i], vv[i_next]) / np.fmax( norms[i] * norms[i_next], 1e-6 )
                backward = np.dot( vv[i], vv[i_prev]) / np.fmax( norms[i] * norms[i_prev], 1e-6 )
                ds.append( np.fmin(forward, backward) )

            dists = np.array( ds )
            order = np.argsort( dists )
            frame_idx = max( order[0]-self.__window_size, 0 )
    
            #============== フレームを抜き出す ================#
            imgarray = np.load( wrangled_image_path )

            imgs = []
            for i in range(15):
                frame_num = frame_idx + i
                if( frame_num>=imgarray.shape[0] ): break
                img = Image.fromarray( imgarray[frame_num] ).resize( (256, 256), Image.BILINEAR )
                imgs.append( img )

            imgs[0].save( thumbnail_path, save_all=True, append_images=imgs[1:], duration=100, loop=0 ) 
            print( "done." )


        except:

            traceback.print_exc()
            print( "failed." )



    def GenerateBatch( self, thumbnailDirPath, wrangledDirPath, featuresDirPath ):
        try:
            if( not ( isinstance(thumbnailDirPath, pathlib.Path) and isinstance(wrangledDirPath, pathlib.Path) and isinstance(featuresDirPath, pathlib.Path) ) ):
                print( "Aborting thumbnail generation. Paths not specified." )
                return

            featurePaths = featuresDirPath.glob( "**/*.npy" )
            for feature_path in featurePaths:
                thumbnail_name = feature_path.stem + ".gif"
                self.Generate( thumbnailDirPath / thumbnail_name, wrangledDirPath / feature_path.name, feature_path )

        except:
            traceback.print_exc()
