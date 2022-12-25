from ..message_protocol import send_message, receive_message, SendMessageError, ReceiveMessageError
from ..serializer import Serializer
from ..proc_echo import EchoServer

import socket
import traceback


# http://blog.fujimisakari.com/network_programing_with_python/
# http://www.ming5.top/?p=370





class Server:
    
    def __init__( self, proc=EchoServer(), pack_encoding=None, unpack_encoding=None ):
        self.__m_Address = None
        self.__m_Backlog = 1
        self.__m_ProcInstance = proc
        self.__m_Socket = None
        self.__m_Serializer = Serializer( pack_encoding=pack_encoding, unpack_encoding=unpack_encoding )
        


    def listen( self, host, port, backlog=1 ):
        try:
            self.__m_Address = ( host, port )
            self.__m_Backlog = backlog

            self.__m_Socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            self.__m_Socket.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
            self.__m_Socket.bind( self.__m_Address )

            self.__m_Socket.listen( self.__m_Backlog )
            print( 'Waiting for connection...' )

        except socket.error as e:
            traceback.print_exc()
            


    def run( self ):

        # connection するまで待つ
        while True:
            conn, addr = self.__m_Socket.accept()
            print( 'Established connection.' )
            
            self.send_recv( conn, self.__m_ProcInstance, self.__m_Serializer )



    @staticmethod
    def send_recv( sock, proc_instance, serializer ):
        #with sock:
        while True:
            try:
                # receive message from client
                recv_data = receive_message( sock )
                if( not recv_data ):
                    break
                        
                # deserealize data
                msg = serializer.Unpack( recv_data )
                proc_name = msg[0]
                args = msg[1]               
                kwargs = msg[2] if len(msg)==3 else {}
                #proc_name, args, kwargs = serializer.Unpack( recv_data )

                # do something
                ret = getattr( proc_instance, proc_name )( *args, **kwargs )

                # send back result to client
                if( proc_name!='echo' ): send_message( sock, serializer.Pack( ret ) )

            except socket.error as e:
                print( 'Server::send_recv()... socket error...%s' % e )
                break

            except SendMessageError as e:
                print( 'Server::send_recv()... SendMessageError occured.' )
                break

            except ReceiveMessageError as e:
                print( 'Server::send_recv()... ReceiveMessageError occured.' )
                break

            except:
                print( 'Callback exception occured at Server::run()...%s' % traceback.format_exc() )
                send_message( sock, serializer.Pack( traceback.format_exc() ) )

        sock.close()
        print( 'Server::send_recv exit...' )



    def close( self ):
        if( self.__m_Socket ):
            self.__m_Socket.close()



#import signal
#import sys


#if __name__=='__main__':

#    #signal.signal( signal.SIGINT, signal_handler )

#    # AF = IPv4 という意味
#    # TCP/IP の場合は、SOCK_STREAM を使う
    
#    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    s.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
#    s.bind((host, port))
    
#    s.listen(1)
#    print( 'Waiting for connection...' )

#    # connection するまで待つ
#    while True:
#        conn, addr = s.accept()
#        print( 'Established connection.' )

#        with conn:
#            while True:
#                try:
#                    # receive message from client
#                    recv_data = receive_message( conn )
#                    if not recv_data:
#                        break
#                    print( 'server received: {}'.format(recv_data) )

#                    # TODO: Do something here
                    
                    
#                    # send message to client
#                    send_message( conn, b'Received: ' + recv_data )# クライアントにデータを返す(b -> byte でないといけない)

#                    #time.sleep(1)
#                except socket.error:
#                    traceback.print_exc()
#                    conn.close()
#                    break
