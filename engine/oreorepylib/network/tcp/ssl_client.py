from ..message_protocol import send_message, receive_message, SendMessageError, ReceiveMessageError
from ..serializer import Serializer

import socket
import time
import traceback

# https://qiita.com/butada/items/9450e39d8d4aac6ac1fe # SSL使ったソケット通信
# https://www.erestage.com/apache/ore_ssl_create/ # オレオレ証明書の作成方法


import ssl
import _ssl




class SSLClient():

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
                    raise socket.error#return None
                
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
    

    
    @staticmethod
    def make_connection( host_, port_, timeout_, trial_ ):
        try:
            #context = ssl.create_default_context()
            context = ssl.SSLContext( _ssl.PROTOCOL_TLS_CLIENT )
            context.load_verify_locations( './keys/server.crt' )
            context.check_hostname = False

            #sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            sock = context.wrap_socket( socket.socket( socket.AF_INET, socket.SOCK_STREAM ), server_hostname=host_ )
            sock.settimeout( timeout_ )
            sock.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
                
            sock.connect( (host_, port_) )
            print( 'Client()::make_connection...connected' )

            cert = sock.getpeercert()
            print(cert)

            return sock

        except socket.error as e:
            print( 'Error at Client::make_connection... %s' % e )
            time.sleep(1)
                
        return None