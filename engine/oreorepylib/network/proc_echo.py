
class EchoServer:
    def Echo( self, *args, **kwargs ):
        print( 'args: ', args )
        print( 'kwargs: ', kwargs )
        return args, kwargs
