import msgpack
import traceback


#class PackError(Exception): pass
#class UnpackError(Exception): pass



class Serializer:

    def __init__( self, pack_encoding, unpack_encoding ):
        print( "Serializer msgpack ver..." )
        ##self.__m_Encode = encode
        self.__m_Pakcer = msgpack.Packer(use_bin_type=True)# encoding=pack_encoding )
        self.__m_Unpackcer = msgpack.Unpacker(raw=False)# encoding=unpack_encoding )



    def Pack( self, data ):
        try:
            return self.__m_Pakcer.pack( data )

        except:
            print( 'Exception occured at Serializer::Pack ')
            traceback.print_exc()
            #raise PackError( traceback.format_exc() )
            return None


    def Unpack( self, data ):
        try:
            self.__m_Unpackcer.feed( data[:len(data)] )
            for o in self.__m_Unpackcer:
                return o

        except:
            print( 'Exception occured at Serializer::Unpack ')
            traceback.print_exc()
            #raise UnpackError( traceback.format_exc() )
            return None