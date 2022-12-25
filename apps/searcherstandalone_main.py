import sys
import pathlib

from searchengine import SearchEngine
from clientwidget import *


path_root = pathlib.Path('../data')



if __name__=='__main__':

    searcher = SearchEngine()
    searcher.Init( path_root, "https://tfhub.dev/google/imagenet/inception_v3/feature_vector/5", [None, 299, 299, 3] )

    app = QApplication(sys.argv)

    mainWidget = ClientWidget( searcher )
    mainWidget.show()

    sys.exit(app.exec_())
