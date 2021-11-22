
############### Main.py#######################

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QCoreApplication
from PytubeLogic import MainWindow


from pytube import YouTube
import Function as F


if __name__ == "__main__":
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)


    F.makefolder()

    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())

########################


# Note 按鈕執行 長時間操作 要使用 thread 另開，不然按鈕會有問題
# Note 長時間操作另開thread，如要更新主畫面要自定義訊號來更新畫面