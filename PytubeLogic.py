############## Logic.py ########################
from PytubeUI import Ui_MainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from pytube import YouTube
import Function as F
import os
from pytube import Playlist
import ssl
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
import Function as F
from Setting import Ui_Dialog

import re
import subprocess

dwurl,CBCT="",""
SaveFolderPath=""

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        global SaveFolderPath

        super(MainWindow, self).__init__(parent)
        self.setupUi(self)                            # 父類做好UI

        datas=F.ReadData()
        SaveFolderPath=datas["path"]

        self.thread = Thread(self.pushButton)
        self.thread.breakSignal.connect(self.update)

    def update(self,message):
        self.Result_PTE.appendPlainText(message)
        QApplication.processEvents()  # 实时显示内容到TExtEdit控件上

    def StartDownload(self):
        global dwurl
        global CBCT
        dwurl=self.plainTextEdit.toPlainText()
        CBCT=self.comboBox.currentText()

        if dwurl !="" :
            self.Result_PTE.appendPlainText("Start")
            QApplication.processEvents() # 实时显示内容到TExtEdit控件上
            print(self.comboBox.currentText())

            if self.comboBox.currentText() == "Video" or self.comboBox.currentText() == "Music":
                print(dwurl)
                url=str(dwurl)
                try :
                    yt = YouTube(url)
                except:
                    self.Result_PTE.appendPlainText("Error url")
                    QApplication.processEvents()  # 实时显示内容到TExtEdit控件上
                else:
                    video = yt.streams.get_highest_resolution()

                    self.Result_PTE.appendPlainText("Start Download : "+video.default_filename)
                    QApplication.processEvents()  # 实时显示内容到TExtEdit控件上
                    w_path=os.path.join(os.getcwd(), "Downloadfile", video.default_filename)
                    try:
                        os.remove(w_path)
                    except:
                        pass
                    # Download
                    video.download(os.path.join(os.getcwd(), "Downloadfile"))

                    if self.comboBox.currentText() == "Music":
                        F.mp4tomp3(w_path)
                    self.Result_PTE.appendPlainText("End Download...")

            elif self.comboBox.currentText() == "You-Get" :

                if not self.thread.isRunning():    # "You-Get"
                    self.pushButton.setEnabled(False)
                    self.thread.start()
            else:                                  # Pylist
                if not self.thread.isRunning():
                    self.pushButton.setEnabled(False)
                    self.thread.start()

    def Setting(self):
        s=DialogTEST()
        ret = s.exec_()

        print(ret)  # accepted1 or reject0

        ######################################
        # self.Dialog = QtWidgets.QDialog()
        # self.s = Ui_Dialog()
        # self.s.setupUi(self.Dialog)
        #
        # self.Dialog.exec_()
        # # self.Dialog.show()
        # # # Dialog.open()
        ######################################


##################################


class DialogTEST(QtWidgets.QDialog,Ui_Dialog):
    def __init__(self, parent=None):
        global SaveFolderPath  # By declaring it global inside the function that accesses it:
        super(DialogTEST, self).__init__(parent)
        self.setupUi(self)
        self.foldernames=""
        self.textEdit.setText(SaveFolderPath)
    def test(self):
        print("123")
    def slot1(self):  # self.toolButton.clicked.connect(Dialog.slot1)
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.DirectoryOnly) # https://doc.qt.io/qt-5/qfiledialog.html
        if dlg.exec_():
            self.textEdit.setText(str(dlg.selectedFiles()[0]))           # Ui_Dialog
    def accept(self):  # OK buttom
        global SaveFolderPath
        super().accept()
        self.foldernames=self.textEdit.toPlainText()
        SaveFolderPath=self.foldernames
        F.WriteData("path",SaveFolderPath)
##################################

class Thread(QtCore.QThread):

    # 定義訊號,定義引數為str型別
    breakSignal = pyqtSignal(str)   # 為了發射訊號更新 UI

    def __init__(self,BTN):
        super(Thread, self).__init__()  # 執行父類init
        self.BTN=BTN

    def run(self):
        # QtCore.QThread.sleep(2)

        print("CBCT=",CBCT)
        if CBCT == "You-Get":  # https://you-get.org/#getting-started
            w_path = os.path.join(os.getcwd(), "Downloadfile1")
            self.breakSignal.emit("Start Download by You-Get: ")
            #########Download############
            try:
                info = subprocess.Popen(
                    "you-get --output-dir " + w_path +" "+ dwurl,
                    shell=True, stdout=subprocess.PIPE).stdout.read()
            except:
                self.breakSignal.emit("error url")
            else:
                #########################
                info = info.decode("utf-8", "ignore")
                title=info.partition("\r\n")[2].partition("\r\n")[0].partition(":")[2].replace(" ", "")
                print(title) # 这首【七里香】，是初恋的感觉吗？庆祝周杰伦出道21周年！
                #########################
                self.breakSignal.emit("End Download : " + title)
                self.BTN.setEnabled(True)
        else:
            ssl._create_default_https_context = ssl._create_unverified_context
            p = Playlist(dwurl)

            try:
                p.title
            except:
                self.breakSignal.emit("error url")
            else:
                print(f'Downloading: {p.title}')
                for video in p.videos:
                    print(video.title)
                    video = video.streams.get_highest_resolution()

                    self.breakSignal.emit("Start Download : " + video.title)

                    QApplication.processEvents()  # 实时显示内容到TExtEdit控件上
                    w_path = os.path.join(os.getcwd(), "Downloadfile1", video.title)
                    try:
                        os.remove(w_path)
                    except:
                        pass
                    # Download
                    video.download(os.path.join(os.getcwd(), "Downloadfile1"))
                self.breakSignal.emit("List download finished")
                self.BTN.setEnabled(True)


