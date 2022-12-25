import pathlib
import subprocess
import urllib.request
from io import BytesIO
import threading
import traceback
import time

from PIL import Image, ImageGrab
from PIL.ImageQt import ImageQt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from oreorepylib.ui.pyqt5 import FlowLayout, stylesheet, Batch, MainWindow






def AlignImage( pil_img, img_size, background_color ):

    # Crop to square
    width, height = pil_img.size
    img_cropped = None

    if width == height:
        img_cropped = pil_img
    elif width > height:
        img_cropped = Image.new( pil_img.mode, (width, width), background_color )
        img_cropped.paste( pil_img, (0, (width - height) // 2) )
    else:
        img_cropped = Image.new( pil_img.mode, (height, height), background_color )
        img_cropped.paste( pil_img, ((height - width) // 2, 0) )
    
    # Resize
    return img_cropped.resize( img_size, Image.BILINEAR )# resize image






# image frame
class ImageFrame( QFrame ):

    def __init__( self, parent=None ):
        super(ImageFrame, self).__init__(parent)

        self.setAcceptDrops(True)
        self.setFocusPolicy( Qt.ClickFocus )
        self.setStyleSheet( stylesheet.g_StaticFrameStyleSheet )

        self.__m_ImageData = None

        self.__m_Label = QLabel()
        #self.__m_Label.setMinimumSize( 300, 300 )
        self.__m_Label.setText( "Put query image here." )
        self.__m_Label.setAlignment( Qt.AlignHCenter | Qt.AlignVCenter )
        self.__m_Label.setStyleSheet( "QLabel { color: rgb(128,128,128); border: none;}" )

        self.__m_PixMap = None


        self.setLayout( QGridLayout() )
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(self.__m_Label, 0, 0, Qt.AlignCenter)

        #self.setContextMenuPolicy( Qt.CustomContextMenu )
        #self.customContextMenuRequested.connect( self.openMenu )

        self.action_paste = QAction( "Paste from Clipboard" )
        self.action_paste.setShortcut( QKeySequence(Qt.CTRL + Qt.Key_V) )
        self.action_paste.triggered.connect( self.PasteFromClipboard )

        self.addAction( self.action_paste )


    def dragEnterEvent( self, event ):# QDragEnterEvent
        if( event.mimeData().hasUrls() ):
            event.accept()
        else:
            event.ignore()


    def dropEvent( self, event ):# QDropEvent
        for url in event.mimeData().urls():
            #filepath = str(url.toLocalFile())
            self.LoadImage( str(url.toLocalFile()) )


    def resizeEvent( self, event ):
        if( self.__m_PixMap ):
            self.__m_Label.setPixmap( self.__m_PixMap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation) ) 
        return super(ImageFrame, self).resizeEvent(event)


    def GetImageData( self ):
        return self.__m_ImageData


    def LoadImage( self, filepath ):
        try:
            self.__m_ImageData = Image.open( str(filepath) ).convert("RGB")
            qim = ImageQt( self.__m_ImageData )
            if( qim ):
                del self.__m_PixMap
                self.__m_PixMap = QPixmap.fromImage(qim)
                self.__m_PixMap.detach()
                self.__m_Label.setPixmap( self.__m_PixMap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation) )
                print( "Image loaded: %s" % filepath )
        except:
            traceback.print_exc()


    def PasteFromClipboard( self ):
        try:
            im = ImageGrab.grabclipboard()
            if( isinstance(im, Image.Image) ):
                self.__m_ImageData = im.convert("RGB")
                qim = ImageQt( self.__m_ImageData )
                if( qim ):
                    del self.__m_PixMap
                    self.__m_PixMap = QPixmap.fromImage(qim)
                    self.__m_PixMap.detach()
                    self.__m_Label.setPixmap( self.__m_PixMap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation) )
                    print( "Image loaded from clipboard" )
            else:
                string = QApplication.clipboard().text()

                f = BytesIO( urllib.request.urlopen(string).read() )
                self.__m_ImageData = Image.open(f).convert("RGB")
                qim = ImageQt( self.__m_ImageData )
                if( qim ):
                    del self.__m_PixMap
                    self.__m_PixMap = QPixmap.fromImage(qim)
                    self.__m_PixMap.detach()
                    self.__m_Label.setPixmap( self.__m_PixMap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation) )
                    print( "Image loaded from clipboard" )

        except:
            traceback.print_exc()


    def contextMenuEvent( self, event ):
        menu = QMenu()
        menu.addAction( self.action_paste )
        menu.exec( self.mapToGlobal( event.pos() ) )




    # TODO: deprecated. 2019.04.23
    #def LoadImage( self, filepath ):
    #    img = QImage( filepath )
    #    if( img ):
    #        del self.__m_PixMap
    #        self.__m_PixMap = QPixmap.fromImage(img)
    #        self.__m_Label.setPixmap( self.__m_PixMap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation) )
    #        print( "ImageFrame loaded: %s" % filepath )




class ThumbnailFrame(QFrame):

    stylesheet = """
    QFrame
    {
        background-color: rgb(0,0,0);
        border: 0px none;
    }

    QFrame:hover
    {
        border: 1px solid rgb(164,128,100);
    }
"""

    stylesheet_label = """
    QLabel
    {
        color: rgb(235,235,235);
        background-color: black;

        border: 0px none;
    }
"""


    def __init__( self, parent=None ):
        self.anim = None

        super(ThumbnailFrame, self).__init__(parent)
        
        #self.setMinimumSize(256, 256)
        self.setStyleSheet( self.stylesheet )
        
        self.__m_MediaPath = ""

        self.__m_Label = QLabel()

        self.__m_TextLabel = QLabel()
        self.__m_TextLabel.setStyleSheet( self.stylesheet_label )

        #self.__m_PixMap = None
        self.__m_ByteArray = None
        self.__m_Buffer = None


        self.setLayout( QGridLayout() )
        self.layout().addWidget( self.__m_Label, 0, 0, Qt.AlignCenter )
        self.layout().addWidget( self.__m_TextLabel, 1, 0, Qt.AlignCenter )

        self.setMouseTracking(True)


    def paintEvent(self, event):
        #print( "paint event...%s" % self.objectName() )
        return super(ThumbnailFrame, self).paintEvent(event)

    def resizeEvent( self, event ):
        if( self.anim ):
            self.anim.setScaledSize( self.geometry().size() )
        #if( self.__m_PixMap ):
        #    self.__m_Label.setPixmap( self.__m_PixMap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation) ) 
        return super(ThumbnailFrame, self).resizeEvent(event)


    def enterEvent( self, event ):
        #print("mouse entered")
        if( self.anim.isValid() ): self.anim.setPaused(False)
        return super(ThumbnailFrame, self).enterEvent(event)


    def leaveEvent( self, event ):
        #print("mouse leaved")
        if( self.anim.isValid() ): self.anim.setPaused(True)
        return super(ThumbnailFrame, self).leaveEvent(event)



    def LoadImage( self, path_thumbnail, path_media ):

        self.__m_MediaPath = path_media
        self.anim = QMovie( path_thumbnail )
        if( self.anim ):
            self.anim.setScaledSize( self.geometry().size() )
            self.__m_Label.setMovie( self.anim )
            self.anim.start()
            self.anim.setPaused(True)
            

        #img = QImage( path_thumbnail )
        #if( img ):
        #    del self.__m_PixMap
        #    self.__m_PixMap = QPixmap.fromImage(img)
        #    self.__m_Label.setPixmap( self.__m_PixMap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation) )
        
        #    self.__m_MediaPath = path_media
        #    #print( "ThumbnailFrame loaded: %s" % self.__m_MediaPath )


    def LoadImageFromStream( self, stream, path_media ):
            
        self.__m_MediaPath = path_media
        self.anim = QMovie()

        if( stream ):
            self.__m_ByteArray = QByteArray( stream )
            self.__m_Buffer = QBuffer( self.__m_ByteArray )
            #self.__m_Buffer.open( QIODevice.ReadOnly )
            self.anim.setDevice( self.__m_Buffer )

        if( self.anim.isValid() ):
            self.anim.setCacheMode( QMovie.CacheAll )
            self.anim.setScaledSize( self.geometry().size() )
            self.__m_Label.setMovie( self.anim )
            self.anim.start()
            self.anim.setPaused(True)
            


    def OpenFile( self ):
        print( "Open media file %s" % self.__m_MediaPath )
        cmd = "\"%s\"" % self.__m_MediaPath
        returncode = subprocess.Popen( cmd, shell=True )


    def OpenDirectory( self ):
        subprocess.run( "explorer /select, {}".format( str( pathlib.Path( self.__m_MediaPath )) ) )


# https://stackoverflow.com/questions/827371/is-there-a-way-to-list-all-the-available-drive-letters-in-python
# TODO: refactor. Gather drive letter
    def get_drives(self):
        import string
        from ctypes import windll
        drives = []
        bitmask = windll.kernel32.GetLogicalDrives()
        for letter in string.ascii_uppercase:
            if bitmask & 1:
                drives.append(letter)
            bitmask >>= 1

        return drives



#    def CopyPathToClipboard( self ):

#        drives = self.get_drives()
##        print( drives )

#        #import win32api
#        import win32wnet
        
#        #drives = win32api.GetLogicalDriveStrings()
#        #drives = drives.split("\000")[:-1]

#        path = self.__m_MediaPath
#        #print( path )
#        for drv in drives:
#            drv_letter = drv + ":"
#            try:
#                drivepath = win32wnet.WNetGetUniversalName( drv_letter, 1 )#.replace("\\","/")
#                #print( drivepath )
#                if( path.find( drivepath )==0 ):
#                    path = path.replace( drivepath, drv_letter )
#                    #print( "gfsg:", path )
#                    break
#            except:
#                pass

#        #print( path.replace("\\","/") )
#        QApplication.clipboard().setText( path ) #self.__m_MediaPath )
        

    def SetLabel( self, label_text ):
        self.__m_TextLabel.setText( label_text )


    def contextMenuEvent( self, event ):
        
        menu = QMenu()

        action_play = QAction( "Open File" )
        action_play.triggered.connect( self.OpenFile )

        action_opendir = QAction( "Open Directory" )
        action_opendir.triggered.connect( self.OpenDirectory )

        #action_copypath = QAction( "Copy Path to Clipboard" )
        #action_copypath.triggered.connect( self.CopyPathToClipboard )

        menu.addAction( action_play )
        menu.addAction( action_opendir )
        #menu.addAction( action_copypath )
        
        menu.exec( self.mapToGlobal( event.pos() ) )





class LoadingOverlay( QWidget ):

    def __init__(self, parent=None):
        super(LoadingOverlay, self).__init__(parent)

        self.setLayout( QVBoxLayout() )
        self.layout().setContentsMargins(0, 0, 0, 0)

        movie = QMovie( ":/resources/images/spinner-loading.gif" )
        movie.setScaledSize( QSize(50,50) )
        movie.start()
        movie.setPaused(True)
        self.label = QLabel( self)
        self.label.setAlignment( Qt.AlignHCenter | Qt.AlignVCenter )
        self.label.setStyleSheet( "background-color: rgba(64,64,64,127);" )
        self.label.setMovie( movie )
        
        self.layout().addWidget( self.label )


    def show(self):
        self.label.movie().setPaused(False)
        return super(LoadingOverlay, self).show()


    def hide(self):
        self.label.movie().setPaused(True)
        return super(LoadingOverlay, self).hide()


    def paintEvent(self, event):
        
        return super(LoadingOverlay, self).paintEvent(event)



class ResultFrame( QFrame ):

    def __init__(self, parent=None):
        super(ResultFrame, self).__init__(parent=parent)

        self.setStyleSheet( stylesheet.g_DarkDynamicFrameStyleSheet )
        self.setFocusPolicy( Qt.StrongFocus )
        self.nonlayoutwidgets = []


    def addChildWidget(self, w):
        w.setParent(self)
        w.setGeometry( self.geometry() )
        self.nonlayoutwidgets.append(w)


    def wheelEvent(self, event):
        rect = self.visibleRegion().boundingRect() if self.isVisible() else QRect( QPoint(),event.size() )
        for w in self.nonlayoutwidgets:
            w.setGeometry( rect )
        super(ResultFrame, self).wheelEvent(event)


    def resizeEvent(self, event):
        rect = self.visibleRegion().boundingRect() if self.isVisible() else QRect( QPoint(),event.size() )
        for w in self.nonlayoutwidgets:
            w.setGeometry( rect )
        event.accept()




# line edit
#class MyLineEdit(QLineEdit):

#    def __init__( self, str="", parent=None ):
#        super(MyLineEdit, self).__init__(str, parent)

#        self.setDragEnabled(True)
#        self.setAcceptDrops(True)


#    def dragEnterEvent( self, event ):
#        if event.mimeData().hasUrls():
#            event.accept()
#        else:
#            event.ignore()


#    def dropEvent( self, event ):
#        for url in event.mimeData().urls():
#            filepath = str(url.toLocalFile())
#            self.setText( filepath.replace("\\", "/") )
#            self.returnPressed.emit()



# main widget
class ClientWidget( MainWindow ):#QFrame):#

    sig_add_item = pyqtSignal()
    sig_add_showmore_button = pyqtSignal()
    sig_remove_showmore_button = pyqtSignal()
    sig_showloading = pyqtSignal()
    sig_hideloading = pyqtSignal()
    sig_showstatus = pyqtSignal( str, float )


    def __init__( self, searcher ):
        super(ClientWidget, self).__init__()

        self.setWindowTitle( "OreOre Visual Search" )
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
        self.__m_StatusBar.setStyleSheet( stylesheet.g_StatusBarStyleSheet )
        self.__m_StatusBar.setSizePolicy( QSizePolicy.Expanding, QSizePolicy.Fixed )
        self.setStatusBar( self.__m_StatusBar )

        # create 
        vboxlayout = QVBoxLayout()
        vboxlayout.setSpacing(0)
        vboxlayout.setContentsMargins(6, 0, 6, 6)
        vboxlayout.addWidget( self.__m_Hsplitter )

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
                self.sig_showstatus.emit( "Aborted searching: No query image specified...", 5000.0 )
                #print( "No query images..." )
                self.__m_PushButton["Search"].setEnabled(True)
                self.sig_hideloading.emit()
                return

            input_shape = self.__m_refSearcher.InputShape()# (batch_size, height, width, channels)
            if( input_shape is None ):
                self.sig_showstatus.emit( "Aborted search: Failed connecting to server...", 5000.0 )
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
            self.sig_showstatus.emit( "Done.", 5000.0 )

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
            self.sig_showstatus.emit( "Done.", 5000.0 )

        except:
            print( "Exception occured at __ShowMoreResults" )
            traceback.print_exc()
            self.__m_PushButton["Search"].setEnabled(True)
            self.sig_hideloading.emit()
            self.__m_StatusBar.clearMessage()
