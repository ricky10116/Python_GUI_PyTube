############## Logic.py ########################
from PytubeUI import Ui_MainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from pytube import YouTube
import os
from pytube import Playlist
import ssl
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
import Function as F
from Setting import Ui_Dialog
import shlex
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
        self.thread.breakSignal_PB.connect(self.update_PB)

        self.Thread_VideoMusic = Thread_VideoMusic(self.comboBox,self.pushButton)
        self.Thread_VideoMusic.breakSignal.connect(self.update)
        self.Thread_VideoMusic.breakSignal_PB.connect(self.update_PB)

    def update(self,message):
        self.Result_PTE.appendPlainText(message)
        QApplication.processEvents()  # 实时显示内容到TExtEdit控件上

    def update_PB(self,number):
        self.progressBar.setValue(number)
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
                if not self.Thread_VideoMusic.isRunning():
                    self.pushButton.setEnabled(False)
                    self.Thread_VideoMusic.start()

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
    breakSignal_PB = pyqtSignal(int)  # 為了發射訊號更新 UI

    def __init__(self,BTN):
        super(Thread, self).__init__()  # 執行父類init
        self.BTN=BTN                    # pass

    def run(self):
        # QtCore.QThread.sleep(2)
        if CBCT == "You-Get":  # https://you-get.org/#getting-started
            w_path = SaveFolderPath
            self.breakSignal_PB.emit(0)

            #########Download############

            try:
                process2 = subprocess.Popen(shlex.split("you-get -i " + dwurl), stdout=subprocess.PIPE, shell=True)
            except:
                self.breakSignal.emit("error url")
                self.BTN.setEnabled(True)
            else:
                title = process2.stdout.read().decode().partition("streams")[0].partition("title:")[2].strip()
                self.breakSignal.emit("Start Download " + title + " by You-Get:")

                command = "you-get --output-dir " + w_path + " " + dwurl
                process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, shell=True)

                count = -1
                while True:
                    # output = process.stdout.readline() run_command("you-get https://www.youtube.com/watch?v=rzR9TM8Td5g")
                    output = process.stdout.readline(50).decode('utf-8', 'ignore')
                    if output == '' and process.poll() is not None:
                        break
                    if output:
                        if "%" in output:
                            output1 = output.strip().partition("% (")[0][-5:] + "%"
                            output1 = output1.replace("\n", "")
                            try:  # readline(50) will output error cut 1. cannot convert float or convert wrong number
                                float(output1[:-1]) # %
                            except:
                                continue
                            else:  # 如果没有异常执行这块代码
                                if float(output1[:-1]) > count:
                                    count = float(output1[:-3])
                                    print(output1)
                                    self.breakSignal_PB.emit(count)

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

##################################
class Thread_VideoMusic(QtCore.QThread):

    # 定義訊號,定義引數為str型別
    breakSignal = pyqtSignal(str)   # 為了發射訊號更新 UI
    breakSignal_PB = pyqtSignal(int)  # 為了發射訊號更新 UI

    def __init__(self,cbct,BTN):
        # super(Thread_VideoMusic, self).__init__()  # 執行父類init
        super().__init__()  # new
        self.comboBox = cbct
        self.BTN=BTN

    def run(self):
        url = str(dwurl)
        try:
            yt = YouTube(url)
        except:
            self.breakSignal.emit("Error url")
            self.BTN.setEnabled(True)
        else:
            video = yt.streams.get_highest_resolution()
            self.breakSignal.emit("Start Download : " + video.default_filename)
            w_path = os.path.join(os.getcwd(), "Downloadfile", video.default_filename)
            try:
                os.remove(w_path)
            except:
                pass
            # Download
            video.download(os.path.join(os.getcwd(), "Downloadfile"))

            if self.comboBox.currentText() == "Music":
                F.mp4tomp3(w_path)
            self.breakSignal.emit("End Download...")
            self.BTN.setEnabled(True)