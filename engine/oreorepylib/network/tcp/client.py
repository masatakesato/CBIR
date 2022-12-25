from ..message_protocol import send_message, receive_message, SendMessageError, ReceiveMessageError
from ..serializer import Serializer

import socket
import time
import traceback

# https://github.com/msgpack-rpc/msgpack-rpc-python


# https://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data

#with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#    # サーバを指定
#    s.connect(('127.0.0.1', 50007))
#    # サーバにメッセージを送る
#    s.sendall(b'hello')
#    # ネットワークのバッファサイズは1024。サーバからの文字列を取得する
#    data = s.recv(1024)
#    #
#    print(repr(data))








class Client():

    def __init__( self, host, port, timeout, trial, pack_encoding=None, unpack_encoding=None ):
        self.__m_host = host
        self.__m_port = port
        self.__m_timeout = timeout
        self.__m_trial = trial

        self.__m_Serializer = Serializer( pack_encoding=pack_encoding, unpack_encoding=unpack_encoding )
        
        self.__m_socket = self.make_connection( self.__m_host, self.__m_port, self.__m_timeout, self.__m_trial )
        


    def call( self, proc_name, *args, **kwargs ):
        
        #print( 'client.call...' )
        #print( '    args: ', args )
        #print( '    kwargs: ', kwargs )
        trial = 0

        while True:
            try:
                # serialize data
                send_data = self.__m_Serializer.Pack( ( proc_name, args, kwargs ) )

                # send message to server
                send_message( self.__m_socket, send_data )
                
                # receive data from server
                recv_data = receive_message( self.__m_socket )

                if( not recv_data ):
                    print( 'Client::call()... received data is None!' )
                    break#raise socket.error#
                
                # deserialize and return
                return self.__m_Serializer.Unpack( recv_data )


            except SendMessageError as e:
                print( 'Client::call()... SendMessageError occured.' )
                #print( 'Error at Client::call()...%s' % e )
                trial+=1
                if( trial >= self.__m_trial ): break
                #print( '   trying to reconnect[%d]' % trial )
                self.__m_socket = self.make_connection( self.__m_host, self.__m_port, self.__m_timeout, self.__m_trial )# 接続が切れたらリトライ


            except ReceiveMessageError as e:
                print( 'Client::call()... ReceiveMessageError occured.' )
                break

        return None
    
    

    def IsReady( self ):
        try:
            send_data = self.__m_Serializer.Pack( ( 'echo', (), {} ) )
            send_message( self.__m_socket, send_data )
            #print( 'connection is active.' )
            return True
        except:
            #print( 'connection is NOT active.' )
            return False
        

    
    @staticmethod
    def make_connection( host_, port_, timeout_, trial_ ):
        try:
            sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            sock.settimeout( timeout_ )
            sock.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
            sock.connect( (host_, port_) )
            print( 'Client()::make_connection...connected' )
            return sock

        except socket.error as e:
            print( 'Error at Client::make_connection... %s' % e )
            #time.sleep(1)
                
        return None