import traceback
import math
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub




class FeatureExtractor:

    def __init__( self, model_path, input_shape ):

        self.__m_InputShape = input_shape

        g = tf.Graph()
        with g.as_default():
            self.__m_Model = hub.Module( model_path )
            height, width = hub.get_expected_image_size( self.__m_Model )
            x = tf.placeholder( dtype=tf.float32, shape=self.__m_InputShape )
            feature_extractor = self.__m_Model(x)
            init_op = tf.group([tf.global_variables_initializer(), tf.tables_initializer()])
        g.finalize()

        config = tf.ConfigProto()
        config.gpu_options.allow_growth=True
        self.__m_Sess = tf.Session( config=config, graph=g )
        self.__m_Sess.run( init_op )


    def InputShape( self ):
        return self.__m_InputShape


    def Run( self, images ):
        return self.__m_Sess.run( self.__m_Model["out"], feed_dict={ self.__m_FeatureExtractor["in"]: np.array( images ) } )


    def RunBatch( self, images, batch_size=50 ):
        try:

            print( "    Extracting features..." )
            num_batches = int( math.ceil( images.shape[0] / batch_size ) )
            feature_batches = []
            for batch_i in range(num_batches):
        
                start_idx = batch_i * batch_size
                end_idx = min( start_idx + batch_size, images.shape[0] )
        
                #print( '%d: %d - %d' % (batch_i, start_idx, end_idx ) )
                #feature_extractor = self.__m_Model( images[start_idx:end_idx] )
                #features = self.__m_Sess.run( feature_extractor )

                features = self.__m_Sess.run( self.__m_Model, feed_dict={ x: images[start_idx:end_idx] } )

                feature_batches.append( features )

            return np.concatenate( feature_batches )

        except:

            traceback.print_exc()
            return None