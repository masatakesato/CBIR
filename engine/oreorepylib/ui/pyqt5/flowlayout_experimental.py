# https://stackoverflow.com/questions/46681266/qscrollarea-with-flowlayout-widgets-not-resizing-properly

import traceback

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *




class ScrollBar( QScrollBar ):

    signal_maxlimit = pyqtSignal()
    signal_minlmit = pyqtSignal()


    def __init__( self, parent=None ):
        super( ScrollBar, self ).__init__( parent )


    def wheelEvent( self, event ):
        super(ScrollBar, self).wheelEvent(event)

        if( self.isEnabled() ):
            if( self.value() == self.maximum() and event.angleDelta().y() < -10 ):
                print( 'scrollbar at max limit' )
                self.signal_maxlimit.emit()

            elif( self.value() == self.minimum() and event.angleDelta().y() > +10 ):
                print( 'scrollbar at min limit' )
                self.signal_minlmit.emit()


    def mouseMoveEvent(self, QMouseEvent):
        super(ScrollBar, self).mouseMoveEvent(QMouseEvent)

        if( self.isEnabled() ):
            if( self.value() == self.maximum() ):
                print( 'scrollbar at max limit' )
                self.signal_maxlimit.emit()

            elif( self.value() == self.minimum() ):
                print( 'scrollbar at min limit' )
                self.signal_minlmit.emit()


    def mousePressEvent( self, QMouseEvent ):
        super(ScrollBar, self).mousePressEvent(QMouseEvent)

        if( self.isEnabled() ):
            if( self.value() == self.maximum() ):
                print( 'scrollbar at max limit' )
                self.signal_maxlimit.emit()

            elif( self.value() == self.minimum() ):
                print( 'scrollbar at min limit' )
                self.signal_minlmit.emit()




class ScrollArea( QScrollArea ):
    
    def __init__( self, parent=None ):
        super(ScrollArea, self).__init__(parent=parent)

        self.setVerticalScrollBar( ScrollBar(self) ) 
        self.setHorizontalScrollBar( ScrollBar(self) )
        self.signal_v = self.verticalScrollBar().signal_maxlimit
        self.signal_h = self.horizontalScrollBar().signal_maxlimit





class FlowLayout( QLayout ):

    widthChanged = pyqtSignal(int)
    heightChanged = pyqtSignal(int)



    def __init__( self, orientation: Qt.Orientation, parent=None, mergin=0, spacing=-1 ):
        super(QLayout, self).__init__(parent)
        
        self.__m_ItemList = []
        self.__m_Orientation = orientation

        self.__m_refDoLayout = None
        self.__m_refAddSpacing = None
        self.__m_refMinimumSize = None

        if( self.__m_Orientation == Qt.Horizontal ):
            self.__m_refDoLayout = self.__DoLayoutImpl_H
            self.__m_refAddSpacing = self.__AddSpacing_H
            self.__m_refMinimumSize = self.__MinimumSize_H

        elif( self.__m_Orientation == Qt.Vertical ):
            self.__m_refDoLayout = self.__DoLayoutImpl_V
            self.__m_refAddSpacing = self.__AddSpacing_V
            self.__m_refMinimumSize = self.__MinimumSize_V


        self.setSpacing( spacing )



    def __del__( self ):
        while self.count():
            self.takeAt(0)

        self.__m_refDoLayout = None
        self.__m_refAddSpacing = None
        self.__m_refMinimumSize = None



    def Orientation( self ) -> Qt.Orientation:
        return self.__m_Orientation



    def SetOrientation( self, orientation: Qt.Orientation ):

        self.__m_Orientation = orientation

        if( self.__m_Orientation == Qt.Horizontal ):
            self.__m_refDoLayout = self.__DoLayoutImpl_H
            self.__m_refAddSpacing = self.__AddSpacing_H
            self.__m_refMinimumSize = self.__MinimumSize_H

        elif( self.__m_Orientation == Qt.Vertical ):
            self.__m_refDoLayout = self.__DoLayoutImpl_V
            self.__m_refAddSpacing = self.__AddSpacing_V
            self.__m_refMinimumSize = self.__MinimumSize_V



    def addSpacing( self, size ):
        self.__m_refAddSpacing( size )



    def addItem( self, item ):
        self.__m_ItemList.append( item )


    
    def count( self ):
        return len( self.__m_ItemList )

    

    def itemAt( self, index ):
        if( 0 <= index < len(self.__m_ItemList) ):
            return self.__m_ItemList[index]
        return None


    
    def takeAt( self, index ):
        if( 0 <= index < len(self.__m_ItemList) ):
            return self.__m_ItemList.pop(index)
        return None



    def expandingDirections( self ):
        return Qt.Orientations( Qt.Orientation(0) )



    def hasHeightForWidth( self ):
        return True



    def heightForWidth( self, width ):
        height = self.__DoLayoutImpl_H( QRect(0, 0, width, 0), True )
        return height



    def setGeometry( self, rect ):
        super(FlowLayout, self).setGeometry(rect)
        self.__m_refDoLayout( rect )



    def sizeHint(self):
        return self.minimumSize()



    def minimumSize( self ):
        return self.__m_refMinimumSize()


    #def minimumSize( self ):
    #    size = QSize()

    #    for item in self.__m_ItemList:
    #        minsize = item.minimumSize()
    #        extent = item.geometry().bottomRight()
    #        size = size.expandedTo( QSize(minsize.width(), extent.y()) )

    #    margin = self.contentsMargins().left()
    #    size += QSize( 2*margin, 2*margin )

    #    print(size)
    #    return size



    def __AddSpacing_H( self, size ):
        self.addItem( QSpacerItem(size, 0, QSizePolicy.Fixed, QSizePolicy.Minimum) )



    def __AddSpacing_V( self, size ):
        self.addItem( QSpacerItem(0, size, QSizePolicy.Minimum, QSizePolicy.Fixed) )



    def __DoLayoutImpl_H( self, rect, test_only=False ):
        m = self.contentsMargins()
        effective_rect = rect.adjusted( +m.left(), +m.top(), -m.right(), -m.bottom() )
        x = effective_rect.x()
        y = effective_rect.y()
        line_height = 0

        for item in self.__m_ItemList:
            wid = item.widget()

            space_x = self.spacing()
            space_y = self.spacing()
            if( wid is not None ):
                space_x += wid.style().layoutSpacing( QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Horizontal )
                space_y += wid.style().layoutSpacing( QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Vertical )
            
            next_x = x + item.sizeHint().width() + space_x
            if( next_x - space_x > effective_rect.right() and line_height > 0 ):
                x = effective_rect.x()
                y = y + line_height + space_y
                next_x = x + item.sizeHint().width() + space_x
                line_height = 0

            if( not test_only ):
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

            x = next_x
            line_height = max(line_height, item.sizeHint().height())

        new_height = y + line_height - rect.y()
        self.heightChanged.emit(new_height)
        
        return new_height



    def __DoLayoutImpl_V( self, rect, test_only=False ):
        m = self.contentsMargins()
        effective_rect = rect.adjusted( +m.left(), +m.top(), -m.right(), -m.bottom() )
        x = effective_rect.x()
        y = effective_rect.y()
        line_width = 0

        for item in self.__m_ItemList:
            wid = item.widget()

            space_x = self.spacing()
            space_y = self.spacing()
            if( wid is not None ):
                space_x += wid.style().layoutSpacing( QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Horizontal )
                space_y += wid.style().layoutSpacing( QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Vertical )
            
            next_y = y + item.sizeHint().height() + space_y
            if( next_y - space_y > effective_rect.bottom() and line_width > 0 ):
                y = effective_rect.y()
                x = x + line_width + space_x
                next_y = y + item.sizeHint().height() + space_y
                line_width = 0

            if( not test_only ):
                item.setGeometry( QRect( QPoint(x, y), item.sizeHint() ) )

            y = next_y
            line_width = max( line_width, item.sizeHint().width() )

        new_width = x + line_width - rect.x()
        self.widthChanged.emit( new_width )

        return new_width



    def __MinimumSize_H( self ):
        size = QSize()

        for item in self.__m_ItemList:
            minsize = item.minimumSize()
            extent = item.geometry().bottomRight()
            size = size.expandedTo( QSize(minsize.width(), extent.y()) )

        margin = self.contentsMargins().left()
        size += QSize( 2*margin, 2*margin )

        return size


    def __MinimumSize_V( self ):
        size = QSize()

        for item in self.__m_ItemList:
            minsize = item.minimumSize()
            extent = item.geometry().bottomRight()
            size = size.expandedTo( QSize(extent.x(), minsize.height() ) )

        margin = self.contentsMargins().left()
        size += QSize( 2*margin, 2*margin )

        return size
