import functools
import sys
import argparse

from import_engine import *
import oreorepylib.network.tcp as tcp

from clientwidget import *
from oreorepylib.ui.pyqt5.tabbedmdi import TabbedMDIManager, TabWidget, DockableFrame, Duration, InitializeTabbedMDI




class ClientWidgetMDI( QFrame ):#QWidget ):#MainWindow ):#

    sig_add_item = pyqtSignal()
    sig_add_showmore_button = pyqtSignal()
    sig_remove_showmore_button = pyqtSignal()
    sig_showloading = pyqtSignal()
    sig_hideloading = pyqtSignal()
    sig_showstatus = pyqtSignal( str, int )


    def __init__( self, searcher ):
        super().__init__()

        #self.setWindowTitle( "OreOre Visual Search" )
        self.setAcceptDrops(True)

        self.__m_PushButton = {}
        self.__m_Label = {}
        self.__m_TableWidget = {}


        self.__m_PushButton["Search"] = QPushButton( "Search" )
        self.__m_PushButton["Search"].setStyleSheet( stylesheet.g_ButtonStyleSheet )
        self.__m_PushButton["Search"].setFixedSize( 100, 25 )
        self.__m_PushButton["Search"].clicked.connect( self.__SearchProc )

       
        self.__m_PushButton["ShowMore"] = QPushButton()# "▶" )
        self.__m_PushButton["ShowMore"].setStyleSheet( stylesheet.g_ButtonStyleSheet )
        self.__m_PushButton["ShowMore"].setFixedSize( 32, 192 )
        self.__m_PushButton["ShowMore"].setIcon( QIcon(":/resources/images/arrow-right.png") )
        self.__m_PushButton["ShowMore"].clicked.connect( self.__ShowMoreResultsProc )

        
        self.__m_ButtonFrame = QFrame()
        self.__m_ButtonFrame.setStyleSheet( stylesheet.g_StaticFrameStyleSheet )
        self.__m_ButtonFrame.setFixedHeight( 50 )
        self.__m_ButtonFrame.setLayout( QHBoxLayout() )
        self.__m_ButtonFrame.layout().addWidget( self.__m_PushButton["Search"] )

        self.__m_Overlay = LoadingOverlay()
        self.__m_Overlay.hide()

        self.__m_ResultFrame = ResultFrame()#QFrame()
        self.__m_ResultFrame.setLayout( FlowLayout(mergin=20, spacing=10) ) #QGridLayout() )
        self.__m_ResultFrame.addChildWidget( self.__m_Overlay )

                
        self.__m_Scroll = QScrollArea()#flowlayout.ScrollArea()#  + stylesheet.g_DynamicFrameStyleSheet
        self.__m_Scroll.setStyleSheet( stylesheet.g_ScrollBarStyleSheet + stylesheet.g_StaticFrameStyleSheet )# TODO: ウィジェットの余白とか設定するスタイルも追加で必要. 2019.06.06
        self.__m_Scroll.setWidgetResizable(True)
        self.__m_Scroll.setWidget( self.__m_ResultFrame )

        self.__m_Vsplitter = QSplitter( Qt.Vertical )
        self.__m_Vsplitter.setStyleSheet( stylesheet.g_SplitterStyleSheet )
        self.__m_Vsplitter.addWidget( self.__m_ButtonFrame )
        self.__m_Vsplitter.addWidget( self.__m_Scroll )


        self.__m_QueryFrame = ImageFrame(self)
        self.__m_QueryFrame.setMinimumSize( 300, 300 )

        self.__m_Hsplitter = QSplitter( Qt.Horizontal )
        self.__m_Hsplitter.setContentsMargins(0, 0, 0, 0)
        self.__m_Hsplitter.setStyleSheet( stylesheet.g_SplitterStyleSheet )#css_splitter )#

        self.__m_Hsplitter.addWidget( self.__m_QueryFrame )
        self.__m_Hsplitter.addWidget( self.__m_Vsplitter )

        #self.__m_Hsplitter.setStretchFactor( 0, 0 )
        self.__m_Hsplitter.setStretchFactor( 1, 1 )


        self.__m_StatusBar = QStatusBar()
        self.__m_StatusBar.setStyleSheet( stylesheet.g_EmbeddedStatusBarStyleSheet )
        self.__m_StatusBar.setSizePolicy( QSizePolicy.Expanding, QSizePolicy.Fixed )
        self.__m_StatusBar.setSizeGripEnabled( False )
        #self.setStatusBar( self.__m_StatusBar )

        # create 
        vboxlayout = QVBoxLayout()
        vboxlayout.setSpacing(0)
        vboxlayout.setContentsMargins(6, 0, 6, 6)
        vboxlayout.addWidget( self.__m_Hsplitter )
        vboxlayout.addWidget( self.__m_StatusBar )


        self.setLayout( vboxlayout )
        self.setGeometry( 100, 100, 1200, 400 )
        

        self.__m_refSearcher = searcher

        self.__m_NumResultsPerPage = 20


        self.results = []
        self.loadpos = 0
        self.isready = False


        self.sig_add_item.connect( self.proc_additem )
        self.sig_add_showmore_button.connect( self.AddShowMoreButton )
        self.sig_remove_showmore_button.connect( self.RemoveShowMoreButton )
        self.sig_showloading.connect( self.__m_Overlay.show )
        self.sig_hideloading.connect( self.__m_Overlay.hide )

        self.sig_showstatus.connect( self.ShowStatusMessage )



    def OnItemDropped( self ):
        return self.__m_QueryFrame.OnItemDropped



    def BindSearcher( self, searcher ):
        self.__m_refSearcher = searcher



    def SetPath( self, key, path ):
        self.__m_Paths[key] = path



    def AddShowMoreButton( self ):
        if( self.loadpos < len(self.results) ):
            self.__m_ResultFrame.layout().addWidget( self.__m_PushButton["ShowMore"] )


    def RemoveShowMoreButton( self ):
        self.__m_PushButton["ShowMore"].setParent(None)


    def AddItemsToResultFrame( self ):
        
        self.isready = self.__m_refSearcher.IsReady()
        numresults = min( len(self.results) - self.loadpos, self.__m_NumResultsPerPage )

        
        thumbnail_ids = [ self.results[i][3] for i in range(self.loadpos, self.loadpos+numresults) ]
        self.streams = self.__m_refSearcher.GetThumbnailStreams( thumbnail_ids )
        #print( thumbnail_ids )


        qthread = Batch()
        qthread.AddSignal( self.sig_remove_showmore_button, 1 )
        qthread.AddSignal( self.sig_add_item, numresults )
        qthread.AddSignal( self.sig_add_showmore_button, 1 )
        qthread.run()
        qthread.wait()


    def ShowStatusMessage( self, message, timeout=0 ):
        self.__m_StatusBar.showMessage( message, timeout )



    def proc_additem( self ):
        
        result = self.results[ self.loadpos ]

        im_view = ThumbnailFrame( self.__m_ResultFrame )
        im_view.setObjectName( str(result[3]) )

        im_view.setFixedSize( 192, 192 )
        im_view.SetLabel( result[0] + result[4] )
        #stream = self.__m_refSearcher.GetThumbnailStream( result[3] ) if self.isready else None
        stream = self.streams[ self.loadpos % self.__m_NumResultsPerPage ]
        im_view.LoadImageFromStream( stream, result[2] ) #im_view.LoadImage( str(path_thumbnail), str(result[2]) )
        #im_view.LoadImageFromStream( None, result[2] ) 

        self.__m_ResultFrame.layout().addWidget( im_view )
        im_view.lower()

        self.loadpos += 1


    def ClearResultFrame( self ):
        # https://stackoverflow.com/questions/4528347/clear-all-widgets-in-a-layout-in-pyqt

        self.__m_PushButton["ShowMore"].setParent(None)

        # レイアウトに登録したウィジェットの削除方法
        layout = self.__m_ResultFrame.layout()
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().deleteLater()

        self.loadpos = 0



    def __SearchProc( self ):
        self.__m_PushButton["Search"].setEnabled(False)
        thread = threading.Thread( target=self.__Search )
        thread.start()

 
    def __ShowMoreResultsProc( self ):
        self.__m_PushButton["Search"].setEnabled(False)
        thread = threading.Thread( target=self.__ShowMoreResults )
        thread.start()


    def __Search( self ):
        try:
            #if( self.__m_refSearcher.IsReady()==False ):
            #    return
            
            self.sig_showstatus.emit( "Searching...", 0 )

            self.ClearResultFrame()
            self.sig_showloading.emit()

            query_img = self.__m_QueryFrame.GetImageData()
            if( query_img is None ):
                self.sig_showstatus.emit( "Aborted searching: No query image specified...", 5000 )
                #print( "No query images..." )
                self.__m_PushButton["Search"].setEnabled(True)
                self.sig_hideloading.emit()
                return

            input_shape = self.__m_refSearcher.InputShape()# (batch_size, height, width, channels)
            if( input_shape is None ):
                self.sig_showstatus.emit( "Aborted search: Failed connecting to server...", 5000 )
                self.__m_PushButton["Search"].setEnabled(True)
                self.sig_hideloading.emit()
                return

            img_size = ( input_shape[2], input_shape[1] )
            #print( input_shape )
            query_img = AlignImage( query_img, img_size, (0,0,0) )
            pixel_data = list( query_img.getdata() )

            #self.sig_showstatus.emit( "Searching...", 0 )
            #print( "Retrieving..." )
            self.results = self.__m_refSearcher.Search( [ pixel_data ] )# TODO: 検索処理だけ別スレッドで呼び出したい

            #self.sig_showstatus.emit( "Showing results..." )
            #print( "Updateing ResultFrame..." )
            self.AddItemsToResultFrame()

            self.__m_PushButton["Search"].setEnabled(True)
            self.sig_hideloading.emit()
            self.sig_showstatus.emit( "Done.", 5000 )

        except:
            print( "Exception occured at __Search" )
            traceback.print_exc()
            self.__m_PushButton["Search"].setEnabled(True)
            self.sig_hideloading.emit()
            self.__m_StatusBar.clearMessage()


    def __ShowMoreResults( self ):
        try:
            #print( "Updateing ResultFrame..." )
            self.sig_showstatus.emit( "Searching...", 0 )
            self.sig_showloading.emit()

            self.AddItemsToResultFrame()
            self.__m_PushButton["Search"].setEnabled(True)

            self.sig_hideloading.emit()
            self.sig_showstatus.emit( "Done.", 5000 )

        except:
            print( "Exception occured at __ShowMoreResults" )
            traceback.print_exc()
            self.__m_PushButton["Search"].setEnabled(True)
            self.sig_hideloading.emit()
            self.__m_StatusBar.clearMessage()







class App:

    def __init__( self, host: str, port: str ):

        self.__m_Host = host
        self.__m_Port = port

        self.__m_TabbedMDIManager = TabbedMDIManager()
        self.__m_TabbedMDIManager.EnableAddTabButtonByDefault( lambda: self.CreateContentWidgetFunc( "New Tab" ) )
        self.__m_TabbedMDIManager.EnableDynamicTitleByDefault( False )

        self.__m_DockableID = self.__m_TabbedMDIManager.AddDockable( DockableFrame, Duration.Persistent, None, False )

        dockable = self.__m_TabbedMDIManager.GetDockable( self.__m_DockableID )
        dockable.setWindowTitle( "OreOre Visual Search" )
        #dockable.EnableDynamicTitle( True )
        dockable.setGeometry( 100, 100, 1200, 600 )
        self.CreateNewTab( "New Tab" )

        self.__m_TabbedMDIManager.Show()



    def CreateContentWidgetFunc( self, title: str ):
        searcher = SearcherClient( self.__m_Host, self.__m_Port )
        newContentWidget = ClientWidgetMDI( searcher )
        newContentWidget.setWindowTitle( title )
        newContentWidget.OnItemDropped().connect( functools.partial( self.__UpdateTabTitle, widget_id=id(newContentWidget) ) )

        return newContentWidget, newContentWidget.windowTitle(), id(newContentWidget)



    def CreateNewTab( self, title: str ):
        self.__m_TabbedMDIManager.AddTab( self.__m_DockableID, *self.CreateContentWidgetFunc(title) )
        


    def __UpdateTabTitle( self, title: str, widget_id: any ):

        print( "__UpdateTabTitle", title )
        self.__m_TabbedMDIManager.SetTabTitle( widget_id, title )





class SearcherClient( tcp.Client ):

    def __init__( self, host, port ):
        super().__init__( host, port, 60, 5 )
        #self.client = tcp.Client( host, port, 60, 5 )
    
    #def IsReady( self ):
    #    print("hshgsfd")
    #    return tcp.Client.IsReady()


    def InputShape( self, *argc, **argv ):
        #if( self.IsReady() ):
        return self.call( "InputShape" )
        #return (0, 0, 0)


    def GetThumbnailStream( self, *argc, **argv ):
        #if( self.IsReady() ):
        return self.call( "GetThumbnailStream", *argc, **argv )
        #return None


    def GetThumbnailStreams( self, *argc, **argv ):
        #if( self.IsReady() ):
        return self.call( "GetThumbnailStreams", *argc, **argv )
        #return None


    def Search( self, *argc, **argv ):
        #if( self.IsReady() ):
        return self.call( "Search", *argc, **argv )
        #return [], []





if __name__=="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument( "--host", type=str, default="localhost" )
    parser.add_argument( "--port", type=int, default=8080 )

    args = parser.parse_args() 

    host = args.host
    port = args.port


    app = QApplication(sys.argv)

    InitializeTabbedMDI()

    a = App( host, port )


    sys.exit(app.exec_())
