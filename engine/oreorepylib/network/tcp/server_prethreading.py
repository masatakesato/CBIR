from ..message_protocol import send_message, receive_message, SendMessageError, ReceiveMessageError
from ..serializer import Serializer
from ..proc_echo import EchoServer

import socket
import threading
import traceback






# http://www.ming5.top/?p=370



class ServerPrethreading:
    
    def __init__( self, proc=EchoServer(), numthreads=4, pack_encoding=None, unpack_encoding=None ):
        self.__m_Address = None
        self.__m_Backlog = 1
        self.__m_ProcInstance = proc
        self.__m_Socket = None
        self.__m_Serializer = Serializer( pack_encoding=pack_encoding, unpack_encoding=unpack_encoding )
        
        self.__m_NumThreads = numthreads
        self.__m_ThreadList = []
        self.__m_Lock = threading.Lock()




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
        
        for _ in range( self.__m_NumThreads ):
            thread = threading.Thread(target=self.accept, args=( self.__m_Socket, ) )
            thread.start()
            self.__m_ThreadList.append( thread )

        for thread in self.__m_ThreadList:
            thread.join()

        self.__m_Socket.close()


   
    def accept( self, sock ):
        ident = threading.currentThread().ident
        while True:
            print('<{}>Start'.format(ident))
            
            self.__m_Lock.acquire()# クライアントからの単一接続に対して複数スレッドがacceptするのを防ぐ. 必ず単一スレッドだけaccept状態になるようロックをかける
            print('<{}>Get Lock'.format(ident))
            
            conn, addr = sock.accept()
            print('<{}>Accept:{}:{}'.format(ident, addr[0], addr[1]))
            
            self.__m_Lock.release()
            print('<{}>Release Lock'.format(ident))
                
            print('<{}>Client:{}:{}'.format(ident, addr[0], addr[1]))
            self.send_recv( conn, self.__m_ProcInstance, self.__m_Serializer )
            conn.close()



    @staticmethod
    def send_recv( sock, proc_instance, serializer ):
        #with conn:
        while True:
            try:
                #remote_host, remote_remport = sock.getpeername()
                #print('<{}>Client:{}:{}'.format(ident, remote_host, remote_remport))
                # receive message from client
                recv_data = receive_message( sock )
                if( not recv_data ):
                    break
                        
                # deserealize data
                msg = serializer.Unpack( recv_data )
                proc_name = msg[0]
                args = msg[1]               
                kwargs = msg[2] if len(msg)==3 else {}

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
        print( 'ServerPrethreading::send_recv exit...' )



    def close( self ):
        if( self.__m_Socket ):
            self.__m_Socket.close()