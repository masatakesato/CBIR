import os
os.environ["TF_FORCE_GPU_ALLOW_GROWTH"] = "true"#limit tensorflow gpu memory consumption

import traceback
import math
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub




class FeatureExtractor:

    def __init__( self, model_path, input_shape ):

        self.__m_InputShape = input_shape
        self.__m_Model  = tf.keras.Sequential([
            hub.KerasLayer( model_path, trainable=False ),  # Can be True, see below.
        ])
        self.__m_Model.build( self.__m_InputShape )  # Batch input shape.


    def InputShape( self ):
        return self.__m_InputShape


    def Run( self, images ):
        return self.__m_Model.predict( images )



    def RunBatch( self, images, batch_size=50 ):
        try:

            print( "    Extracting features..." )
            num_batches = int( math.ceil( images.shape[0] / batch_size ) )
            feature_batches = []
            for batch_i in range(num_batches):
        
                start_idx = batch_i * batch_size
                end_idx = min( start_idx + batch_size, images.shape[0] )
        
                #print( '%d: %d - %d' % (batch_i, start_idx, end_idx ) )
                features = self.__m_Model.predict( images[start_idx:end_idx] )

                feature_batches.append( features )

            return np.concatenate( feature_batches )

        except:

            traceback.print_exc()
            return None