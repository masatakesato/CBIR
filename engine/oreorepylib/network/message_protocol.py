#import pickle
import struct
import socket
import traceback



# exception handling
class SendMessageError(Exception): pass
class ReceiveMessageError(Exception): pass



# https://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data

# |-- size(4byes) --|++++++++ data ++++++++|-- size(4bytes) --|+++++ data +++++|-- data ...


def send_message( sock, msg ):
    try:
        # Prefix each message with 4-byte length
        #data = pickle.dumps(msg)
        #sock.sendall( struct.pack( '>I', len(data) ) + data )
        #print( len(msg) )

        #msg = struct.pack( 'I', socket.htonl(len(msg)) ) + msg if msg else struct.pack( 'I', 0 )
        #msg = struct.pack( '>I', len(msg) ) + msg if msg else struct.pack( '>I', 0 )
        
        if( not msg ): return

        # Send data size first
        sock.sendall( struct.pack( 'I', socket.htonl(len(msg)) ) )

        # Send data
        sock.sendall( msg )

    except:
        #print( 'Exception occured at send_message' )
        #traceback.print_exc()
        raise SendMessageError( traceback.format_exc() )



def receive_message( sock ):
    try:
        # Extract 4-byte length
        raw_msglen = receive_all( sock, 4 )
        if( not raw_msglen ):
            return None
        
        msg_len = socket.ntohl( struct.unpack('I', raw_msglen)[0] )
        #msg_len = struct.unpack('>I', raw_msglen)[0]
    
        # Read message data
        return receive_all( sock, msg_len )
        #return pickle.loads( receive_all( sock, msg_len ), encoding='bytes' )
    except:
        #print( 'Exception occured at receive_message' )
        #traceback.print_exc()
        raise ReceiveMessageError( traceback.format_exc() )
        return None#b''


# helper function to receive n bytes or return None if EOF is hit
def receive_all( sock , n ):
    data = b''
    while( len(data) < n ):
        packet = sock.recv( n - len(data) )
        if( not packet ):
            return None
        data += packet
        #print( packet, n - len(data) )
    #print( data )
    return data





# deprecated. unstable
# https://docs.python.org/ja/3/howto/sockets.html

#BUFF_SIZE = 4096

## 先頭からしっぽまでメッセージの全パケットを受け取る
#def receive_all( sock ):
#    data = []
#    while(True):
#        packet = sock.recv( BUFF_SIZE )
#        data.append(packet)
#        if( len(packet) < BUFF_SIZE ):
#            break
#    return b''.join(data)


## メッセージ内のフレーム1個分だけ読む. ホントは複数フレームあったら全て取り出したい
#def receive_message( sock ):
#    try:
#        raw_data = receive_all(sock)
#        if( not raw_data ):
#            return None
#        msg_len = struct.unpack_from('>I', raw_data)[0]
#        print( 'receive_message()...msg_len = ', msg_len )

#        return raw_data[4: len(raw_data)]
        
#    except:
#        print( 'Exception occured at receive_message' )
#        traceback.print_exc()
#        return None