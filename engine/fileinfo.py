import os
#import pathlib
from datetime import datetime
import time



class FileInfo:

    def __init__( self, p ):

        self.__m_FileName = p.stem#p.name# filename
        self.__m_FilePath = str( p.resolve() )# file fullpath
        self.__m_DirName = p.parent.name# parent directory name
        self.__m_DirPath = str( p.parent )# parent directory path
        self.__m_Size = os.path.getsize( str(p) )# file size
        self.__m_Extension = ''.join( p.suffixes )# extension
        self.__m_CreationTime = datetime( *time.localtime( os.path.getctime(p) )[:6] )# creation datetime
        self.__m_AccessTime = datetime( *time.localtime( os.path.getatime(p) )[:6] )# access datetime
        self.__m_UpdateTime = datetime( *time.localtime( os.path.getmtime(p) )[:6] )# update time


    def FileName( self ):
        return self.__m_FileName
    

    def FilePath( self ):
        return self.__m_FilePath#pathlib.Path( self.__m_FilePath )


    def DirectoryName( self ):
        return self.__m_DirName


    def DirectoryPath( self ):
        return self.__m_DirPath#pathlib.Path( self.__m_DirPath )


    def Size( self ):
        return self.__m_Size


    def Extension( self ):
        return self.__m_Extension


    def CreationTime( self ):
        return self.__m_CreationTime


    def AccessTime( self ):
        return self.__m_AccessTime


    def UpdateTime( self ):
        return self.__m_UpdateTime
