from PyQt5.QtCore import *



# https://fereria.github.io/reincarnation_tech/11_PySide/02_Tips/06_qthread_01/

class Worker( QThread ):

    __Signal = pyqtSignal()

    def __init__( self, parent=None ):
        super(Worker, self).__init__( parent=parent )

        self.__m_Running = False
        self.__m_Interval = 15000# polling interval in microseconds


    def __del__( self ):
        self.Stop()
        self.wait()


    def BindCallback( self, callback ):
        self.__Signal.connect( callback )


    def Start( self ):
        self.__m_Running = True
        self.start()


    def Stop( self ):
        self.__m_Running = False


    def Resume( self ):
        self.__m_Running = True
        if( self.isRunning() == False ):
            self.start()


    def SetInterval( self, microseconds ):
        self.__m_Interval = microseconds


    ###################### virtual function override ####################
    def run( self ):
        while( self.__m_Running ):
            try:
                self.__Signal.emit()
                self.usleep( self.__m_Interval )# Sleep is required to avoid entire cpu time consumption.
            except:
                traceback.print_exc()
                break




class GenericWorker( QThread ):

    __Signal = pyqtSignal( tuple, dict )# 一旦tuple, dictを受け取る
    __args = tuple()
    __kwargs = dict()
    __refCallback = None


    def __init__(self, parent=None):
        super(GenericWorker, self).__init__( parent=parent )

        self.__m_Running = False
        self.__m_Interval = 15000# polling interval in microseconds

        self.__Signal.connect( self.__Slotfunc )


    def BindCallback( self, callback ):
        self.__refCallback = callback


    def BindArguments( self, *args, **kwargs ):
        self.__args = args
        self.__kwargs = kwargs


    def Start( self ):
        self.__m_Running = True
        self.start()


    def Stop( self ):
        self.__m_Running = False


    def Resume( self ):
        self.__m_Running = True
        if( self.isRunning() == False ):
            self.start()


    def SetInterval( self, microseconds ):
        self.__m_Interval = microseconds


    def __Slotfunc( self, args, kwargs ):
        self.__refCallback( *args, **kwargs )


    ###################### virtual function override ####################
    def run( self ):
        while( self.__m_Running ):
            try:
                self.__Signal.emit( self.__args, self.__kwargs )
                self.usleep( self.__m_Interval )# Sleep is required to avoid entire cpu time consumption.
            except:
                traceback.print_exc()
                break







# TODO: Refactor
class Batch( QThread ):

    def __init__(self, parent=None):
        super(Batch, self).__init__(parent=parent)

        self.iters = []
        self.sig_exec = []



    def AddSignal( self, sig, numiter ):
        self.sig_exec.append( sig )
        self.iters.append(numiter)



    def run( self ):
        self.running = True
        for i, sig in enumerate(self.sig_exec):
            for j in range(self.iters[i]):
                if( self.running==False ): return
                sig.emit()
                self.usleep(1)# sleepしないとウィジェットのビジー状態が開放されない
                #time.sleep(0.005)# time.sleepしないとウィジェットのビジー状態が開放されない
        self.running = False