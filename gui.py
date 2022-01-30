
from PyQt5 import QtWidgets, uic, QtCore
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
from OpenGL.GL import *
from datetime import date,datetime
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import OpenGL.GL as gl
from PyQt5.QtCore import * 
from PyQt5.QtCore import pyqtSignal, QPoint, QSize, Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
import csv
from time import strftime
from PyQt5.QtWidgets import QOpenGLWidget, QApplication, QMainWindow, QSlider
from serial.serialutil import SerialException
from gl_class import GLWidget
import serial
from PyQt5.QtWebEngineWidgets import QWebEngineView
import time
import threading
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
#
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtGui import QPixmap
#
from canvas_class import CustomFigCanvas
from matplotlib.figure import Figure
from matplotlib.animation import TimedAnimation
from matplotlib.lines import Line2D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
#
from table_class import LoadTable
# Variables
q = 0
v = 0
update_period = 3
BATTERY_MIN = 0.5
BATTERY_MAX = 3.7
## Values
telemetry_values= ["<TAKIM NO>",
                       "<PAKET NUMARASI>",
                       "<GONDERME SAATI>",
                       "<BASINC>",
                       "<YUKSEKLIK>",
                       "<İNİŞ HIZI>",
                       "<SICAKLIK>",
                       "<PIL GERILIMI>",
                       "<GPS LATITUDE>",
                       "<GPS LONGITUDE>",
                       "<GPS ALTITUDE>",
                       "<UYDU STATÜSÜ>",
                       "<PITCH>",
                       "<ROLL>",
                       "<YAW>",
                       "<DÖNÜŞ SAYISI>",
                       "<VİDEO AKTARIM BİLGİSİ>"]


## Output
current_directory = os.getcwd()
ofiles_directory = os.path.join(current_directory, r'output_files')
if not os.path.exists(ofiles_directory):
    os.makedirs(ofiles_directory)
videos_files = os.path.join(current_directory, r'videos_files')
if not os.path.exists(videos_files):
    os.makedirs(videos_files)
session_directory = ""
session_time = "00 : 00 : 00"
##
class Communicate(QObject):
    data_signal = pyqtSignal(float)
###

capture = cv2.VideoCapture(0)
src = 0
frame_name = str(src)
video_file = strftime("/%Y-%m-%d_%H%M%S")
video_file_name = videos_files + strftime("/%Y-%m-%d_%H%M%S") + '.avi'
# Default resolutions of the frame are obtained (system dependent)
frame_width = int(capture.get(3))
frame_height = int(capture.get(4))
# Set up codec and output video settings
codec = cv2.VideoWriter_fourcc('M','J','P','G')
output_video = cv2.VideoWriter(video_file_name, codec, 400, (frame_width, frame_height))

class Ui(QMainWindow):
    global value
    def __init__(self):
        super(Ui, self).__init__()
        
        uic.loadUi('Telemetry.ui', self)
        self.setFixedSize(1360,768)
        self.setWindowTitle('TUGRUL Kapsül Telemetri')
        self.setWindowIcon(QIcon('logo.ico'))

        self.openGLWidget = GLWidget(parent=self.centralwidget)
        self.openGLWidget.setObjectName("openGLWidget")


       

        # Telemetry Table
        self.table = LoadTable(self.centralwidget)
        self.table.setGeometry(QtCore.QRect(0, 560, 1360, 210))
        self.tablehbox = QtWidgets.QHBoxLayout()
        self.tablehbox.addWidget(self.table)
        self.grid = QtWidgets.QGridLayout()
        self.grid.addLayout(self.tablehbox, 0, 0)   
        
        #UYDU STATUSU
        self.label_22 = QtWidgets.QLabel(self.centralwidget)
        self.label_22.setGeometry(QtCore.QRect(1180, 90, 211, 31))
        self.label_22.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.label_22.setObjectName("label_22")
        self.statu_bekleme = QtWidgets.QLabel(self.centralwidget)
        self.statu_bekleme.setGeometry(QtCore.QRect(1180, 120, 191, 31))
        self.statu_bekleme.setStyleSheet("background-color: rgb(236, 24, 24);")
        self.statu_bekleme.setObjectName("statu_bekleme")
        self.statu_yukselme = QtWidgets.QLabel(self.centralwidget)
        self.statu_yukselme.setGeometry(QtCore.QRect(1180, 150, 191, 31))
        self.statu_yukselme.setStyleSheet("background-color: rgb(236, 24, 24);")
        self.statu_yukselme.setObjectName("statu_yukselme")
        self.statu_model_uydu_inis = QtWidgets.QLabel(self.centralwidget)
        self.statu_model_uydu_inis.setGeometry(QtCore.QRect(1180, 180, 191, 31))
        self.statu_model_uydu_inis.setStyleSheet("background-color: rgb(236, 24, 24);")
        self.statu_model_uydu_inis.setObjectName("statu_model_uydu_inis")
        self.statu_ayrilma = QtWidgets.QLabel(self.centralwidget)
        self.statu_ayrilma.setGeometry(QtCore.QRect(1180, 210, 191, 31))
        self.statu_ayrilma.setStyleSheet("background-color: rgb(236, 24, 24);")
        self.statu_ayrilma.setObjectName("statu_ayrilma")
        self.statu_gorevl_yuku_inis = QtWidgets.QLabel(self.centralwidget)
        self.statu_gorevl_yuku_inis.setGeometry(QtCore.QRect(1180, 240, 191, 31))
        self.statu_gorevl_yuku_inis.setStyleSheet("background-color: rgb(236, 24, 24);")
        self.statu_gorevl_yuku_inis.setObjectName("statu_gorevl_yuku_inis")
        self.statu_bonus_gorev = QtWidgets.QLabel(self.centralwidget)
        self.statu_bonus_gorev.setGeometry(QtCore.QRect(1180, 270, 191, 31))
        self.statu_bonus_gorev.setStyleSheet("background-color: rgb(236, 24, 24);")
        self.statu_bonus_gorev.setObjectName("statu_bonus_gorev")
        self.statu_kurtarma = QtWidgets.QLabel(self.centralwidget)
        self.statu_kurtarma.setGeometry(QtCore.QRect(1180, 300, 191, 31))
        self.statu_kurtarma.setStyleSheet("background-color: rgb(236, 24, 24);")
        self.statu_kurtarma.setObjectName("statu_kurtarma")
        self.label_22.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:850;\">UYDU STATÜSÜ</span></p></body></html>")
        self.statu_bekleme.setText( "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:850;color:#ffffff;\">BEKLEMEDE</span></p></body></html>")
        self.statu_yukselme.setText( "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:850; color:#ffffff;\">YÜKSELME</span></p></body></html>")
        self.statu_model_uydu_inis.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:850;color:#ffffff;\">MODEL UYDU İNİŞ</span></p></body></html>")
        self.statu_ayrilma.setText( "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:850;color:#ffffff;\">AYRILMA</span></p></body></html>")
        self.statu_gorevl_yuku_inis.setText( "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:850;color:#ffffff;\">GÖREV YÜKÜ İNİŞ</span></p></body></html>")
        self.statu_bonus_gorev.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:850;color:#ffffff;\">BONUS GÖREV</span></p></body></html>")
        self.statu_kurtarma.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:850;color:#ffffff;\">KURTARMA</span></p></body></html>")
                

        # Connect Button
        self.connectButton = QtWidgets.QPushButton(self.centralwidget)
        self.connectButton.setGeometry(QtCore.QRect(60, 30, 75, 23))
        self.connectButton.setObjectName("connectButton")
        self.connectButton.setText("Connect")
        self.connectButton.clicked.connect(self.connect)
        # senvideo Button
        self.sendVideoButton = QtWidgets.QPushButton(self.centralwidget)
        self.sendVideoButton.setGeometry(QtCore.QRect(960, 30, 31,22))
        self.sendVideoButton.setObjectName("sendVideoButton")
        self.sendVideoButton.setText("...")
        self.sendVideoButton.clicked.connect(self.uploadVideo)
        self.sendVideoButton.setEnabled(False)
        # Disconnect Button
        self.disconnectButton = QtWidgets.QPushButton(self.centralwidget)
        self.disconnectButton.setGeometry(QtCore.QRect(60, 60, 75, 23))
        self.disconnectButton.setObjectName("disconnectButton")
        self.disconnectButton.setText("Disconnect")
        self.disconnectButton.clicked.connect(self.disconnect)
        # Session Com
        self.session_com = QtWidgets.QLineEdit(self.centralwidget)
        self.session_com.setGeometry(QtCore.QRect(10, 30, 41, 20))
        self.session_com.setObjectName("session_com")
        self.session_com.setText("COM3")
        # Port Com
        self.session_baudrate = QtWidgets.QLineEdit(self.centralwidget)
        self.session_baudrate.setGeometry(QtCore.QRect(10, 60, 41, 20))
        self.session_baudrate.setObjectName("session_baudrate")
        self.session_baudrate.setText("9600")
        # Upload video Linedit
        self.filename = QtWidgets.QLineEdit(self.centralwidget)
        self.filename.setGeometry(QtCore.QRect(880, 30, 71, 20))
        self.filename.setObjectName("filename")
        self.filename.setText("     ")
        # uptime
        self.uptimeTv = QtWidgets.QLabel(self.centralwidget)
        self.uptimeTv.setGeometry(QtCore.QRect(390, 60, 111, 31))
        self.uptimeTv.setObjectName("uptimeTv")
        self.uptimeTv.setText(session_time)
        self.uptimeTv.setStyleSheet("color: red; font-size: 16px;font-weight: bold;")
        # gps text
        self.lat_var = QtWidgets.QLabel(self.centralwidget)
        self.lat_var.setEnabled(True)
        self.lat_var.setGeometry(QtCore.QRect(1250, 480, 91, 20))
        self.lat_var.setObjectName("lat_var")
        self.lat_var.setText(" ")
        self.lat_var.setStyleSheet("color: red; font-size: 14px;font-weight: bold;")

        self.alt_var = QtWidgets.QLabel(self.centralwidget)
        self.alt_var.setEnabled(True)
        self.alt_var.setGeometry(QtCore.QRect(1250, 440, 91, 20))
        self.alt_var.setObjectName("alt_var")
        self.alt_var.setStyleSheet("color: red; font-size: 14px;font-weight: bold;")
        self.alt_var.setText(" ")

        self.long_var = QtWidgets.QLabel(self.centralwidget)
        self.long_var.setEnabled(True)
        self.long_var.setGeometry(QtCore.QRect(1260, 520, 91, 20))
        self.long_var.setObjectName("long_var")
        self.long_var.setStyleSheet("color: red; font-size: 14px;font-weight: bold;")
        self.long_var.setText(" ")


        

        # battery
        self.curr_var = QtWidgets.QLabel(self.centralwidget)
        self.curr_var.setEnabled(True)
        self.curr_var.setGeometry(QtCore.QRect(570, 30, 91, 20))
        self.curr_var.setObjectName("curr_var")
        self.curr_var.setStyleSheet("color: red; font-size: 14px;font-weight: bold;")
        self.curr_var.setText(" ")


        self.power_Tv = QtWidgets.QLabel(self.centralwidget)
        self.power_Tv.setGeometry(QtCore.QRect(570, 70, 91, 20))
        self.power_Tv.setObjectName("power_Tv")
        self.power_Tv.setStyleSheet("color: red; font-size: 14px;font-weight: bold;")
        self.power_Tv.setText(" ")

        self.volt_var = QtWidgets.QLabel(self.centralwidget)
        self.volt_var.setGeometry(QtCore.QRect(570, 50, 91, 20))
        self.volt_var.setObjectName("volt_var")
        self.volt_var.setStyleSheet("color: red; font-size: 14px;font-weight: bold;")
        self.volt_var.setText(" ")

        self.baterryProgress = QtWidgets.QProgressBar(self.centralwidget)
        self.baterryProgress.setGeometry(QtCore.QRect(660, 70, 121, 16))
        self.baterryProgress.setProperty("value", 0)
        self.baterryProgress.setObjectName("baterryProgress")
        # break command
    
        self.sendButton = QtWidgets.QPushButton(self.centralwidget)
        self.sendButton.setGeometry(QtCore.QRect(150, 40, 61, 31))
        self.sendButton.setObjectName("sendButton")
        self.sendButton.setText("Break")
        self.sendButton.clicked.connect(self.send)

        # sen video to PORT COM
        # break command
    
        self.pushVideoButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushVideoButton.setGeometry(QtCore.QRect(800, 60, 81, 20))
        self.pushVideoButton.setObjectName("pushVideoButton")
        self.pushVideoButton.setEnabled(False)
        self.pushVideoButton.setText("Send Video")
        self.pushVideoButton.clicked.connect(self.sendVideoToCarry)

        #config command
        self.configButton = QtWidgets.QPushButton(self.centralwidget)
        self.configButton.setGeometry(QtCore.QRect(240, 40, 61, 31))
        self.configButton.setObjectName("configButton")
        self.configButton.setText("Config")
        self.configButton.clicked.connect(self.config)

        # connect status
        self.connectStatusTv = QtWidgets.QLabel(self.centralwidget)
        self.connectStatusTv.setGeometry(QtCore.QRect(320, 30, 181, 21))
        self.connectStatusTv.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.connectStatusTv.setObjectName("connectStatusTv")
        self.connectStatusTv.setText("NO CONNECTION")
        self.connectStatusTv.setAlignment(QtCore.Qt.AlignCenter)
        self.connectStatusTv.setStyleSheet("color: red; font-size: 14px;font-weight: bold;")

        # video aktarim status
        self.video_aktarim_bilgisi = QtWidgets.QLabel(self.centralwidget)
        self.video_aktarim_bilgisi.setGeometry(QtCore.QRect(1000, 30, 61, 21))
        self.video_aktarim_bilgisi.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.video_aktarim_bilgisi.setObjectName("video_aktarim_bilgisi")
        self.video_aktarim_bilgisi.setText("HAYIR")
        self.video_aktarim_bilgisi.setAlignment(QtCore.Qt.AlignCenter)
        self.video_aktarim_bilgisi.setStyleSheet("color: red; font-size: 10px;font-weight: bold;")

        # pitch roll yaw
       
        self.pitchrollyaw = QtWidgets.QLabel(self.centralwidget)
        self.pitchrollyaw.setGeometry(QtCore.QRect(0,530, 300, 30))
        self.pitchrollyaw.setObjectName("pitchrollyaw")
        
        self.pitchrollyaw.setStyleSheet("color: white; font-size: 12px;font-weight: bold;background-color: rgb(148, 0, 0);")
        self.pitchrollyaw.setAlignment(QtCore.Qt.AlignCenter)
        self.pitchrollyaw.setText("PITCH               ROLL                   YAW")

        
        
        
        ## Graph 1
        self.graph_1 = CustomFigCanvas(figsize =(4,4), dpi = 70, ylim=(0,100000), ylabel="Basınç")
        
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(300, 90, 450, 155))
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.addWidget(self.graph_1, 1, 0, 1, 1)
        myDataLoop = threading.Thread(name = 'myDataLoop', target = self.dataSendLoop, daemon = True, args = (self.addData_callbackFunc,))
        myDataLoop.start()
        ## Graph 2
        self.graph_2 = CustomFigCanvas(figsize =(7,7), dpi = 70, ylim=(0,700), ylabel="Yükseklik")
        self.gridLayoutWidget2 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget2.setGeometry(QtCore.QRect(300, 235, 450, 155))
        self.gridLayout2 = QtWidgets.QGridLayout(self.gridLayoutWidget2)
        self.gridLayout2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout2.addWidget(self.graph_2, 1, 0, 1, 1)
      
        ## Graph 3

        self.graph_3 = CustomFigCanvas(figsize =(7,7), dpi = 70, ylim=(0,20), ylabel="İniş Hızı")
        self.gridLayoutWidget3 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget3.setGeometry(QtCore.QRect(300, 380, 450, 180))
        self.gridLayout3 = QtWidgets.QGridLayout(self.gridLayoutWidget3)
        self.gridLayout3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout3.addWidget(self.graph_3, 1, 0, 1, 1)
        
        ## Graph 4
       

        self.graph_4 = CustomFigCanvas(figsize =(7,7), dpi = 70, ylim=(0,50), ylabel="Sıcaklık")
        self.gridLayoutWidget4 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget4.setGeometry(QtCore.QRect(730, 380, 450, 180))
        self.gridLayout4 = QtWidgets.QGridLayout(self.gridLayoutWidget4)
        self.gridLayout4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout4.addWidget(self.graph_4, 1, 0, 1, 1)

      
        
        ## Graph 5

        self.graph_5 = CustomFigCanvas(figsize =(7,7), dpi = 70, ylim=(0,24), ylabel="Pil Gerilimi")
        self.gridLayoutWidget5 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget5.setGeometry(QtCore.QRect(730, 235, 450, 155))
        self.gridLayout5 = QtWidgets.QGridLayout(self.gridLayoutWidget5)
        self.gridLayout5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout5.addWidget(self.graph_5, 1, 0, 1, 1)
        
        ## Graph 6

        self.graph_6 = CustomFigCanvas(figsize =(7,7), dpi = 70, ylim=(0,150), ylabel="GPS ALTITUDE")
        self.gridLayoutWidget6 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget6.setGeometry(QtCore.QRect(730, 90, 450, 155))
        self.gridLayout6 = QtWidgets.QGridLayout(self.gridLayoutWidget6)
        self.gridLayout6.setContentsMargins(0, 0, 0, 0)
        self.gridLayout6.addWidget(self.graph_6, 1, 0, 1, 1)

        ## # getting available cameras
    
        self.ImgWidget = QtWidgets.QLabel(self.centralwidget)
        self.ImgWidget.setGeometry(QtCore.QRect(0,109, 301, 211))
        self.ImgWidget.setObjectName("ImgWidget")
        self.ImgWidget.resize(301,211)
        self.available_cameras = QCameraInfo.availableCameras()
        self.save_path = ""
        self.viewfinder = QCameraViewfinder(parent=self.ImgWidget)  # showing this viewfinder
        try:
            self.select_camera(0)
        except:
            print("There is no Camera")
    ########################################################################
    def update(self):
        # Read the next frame from the stream in a different thread
        while True:
            if capture.isOpened():
                (self.status, self.frame) = capture.read()

    def save_frame(self):
        # Save obtained frame into video output file
        output_video.write(self.frame)
   
    def start_recording_thread(self):
        global v 
        v = 0
        while v == 0:
            try:
                self.save_frame()
            except AttributeError:
                pass
    #upload video
    def uploadVideo(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Choose a file",
                ".", "Video Files (*.mp4 *.flv *.ts *.mts *.avi)")
     

        if fileName != '':
            self.pushVideoButton.setEnabled(True)
            print(QUrl.fromLocalFile(fileName))
           

            self.filename.setText(fileName)
    def sendVideoToCarry(self):
        print("Gönderme işlemi başarıyla başladı...")
    def compressVideo(self, video_full_path, output_file_name ,target_size):
        import ffmpeg , os
   
        min_audio_bitrate = 32000
        max_audio_bitrate = 256000

        probe = ffmpeg.probe(video_full_path)
        duration = float(probe['format']['duration'])
        # Audio bitrate, in bps.
        audio_bitrate = float(next((s for s in probe['streams'] if s['codec_type'] == 'audio'), None)['bit_rate'])
        target_total_bitrate = (target_size * 1024 * 8) / (1.073741824 * duration)

        # Target audio bitrate, in bps
        if 10 * audio_bitrate > target_total_bitrate:
            audio_bitrate = target_total_bitrate / 10
            if audio_bitrate < min_audio_bitrate < target_total_bitrate:
                audio_bitrate = min_audio_bitrate
            elif audio_bitrate > max_audio_bitrate:
                audio_bitrate = max_audio_bitrate
        # Target video bitrate, in bps.
        video_bitrate = target_total_bitrate - audio_bitrate

        i = ffmpeg.input(video_full_path)
        ffmpeg.output(i, os.devnull,
                    **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 1, 'f': 'avi'}
                    ).overwrite_output().run()
        ffmpeg.output(i, output_file_name,
                    **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 2, 'c:a': 'aac', 'b:a': audio_bitrate}
                    ).overwrite_output().run()

    ########################################################################
    def addRow(self, 
               takimno,
               paketno,
               gondermesaat,
               basinc,
               yukseklik,
               inishiz,
               sicaklik,
               gerilim,
               latitude,
               longitude,
               altitude,
               state,
               pitch,
               roll,
               yaw,
               donussayisi,
               videobilgisi):
        # Create a empty row at bottom of table
       
        numRows = self.table.rowCount() - 1 
        self.table.insertRow(numRows)
        # Add text to the row
        self.table.setItem(numRows, 0, QtWidgets.QTableWidgetItem(takimno))
        self.table.setItem(numRows, 1, QtWidgets.QTableWidgetItem(paketno))
        self.table.setItem(numRows, 2, QtWidgets.QTableWidgetItem(gondermesaat))
        self.table.setItem(numRows, 3, QtWidgets.QTableWidgetItem(basinc))
        self.table.setItem(numRows, 4, QtWidgets.QTableWidgetItem(yukseklik))
        self.table.setItem(numRows, 5, QtWidgets.QTableWidgetItem(inishiz))
        self.table.setItem(numRows, 6, QtWidgets.QTableWidgetItem(sicaklik))
        self.table.setItem(numRows, 7, QtWidgets.QTableWidgetItem(gerilim))
        self.table.setItem(numRows, 8, QtWidgets.QTableWidgetItem(latitude))
        self.table.setItem(numRows, 9, QtWidgets.QTableWidgetItem(longitude))
        self.table.setItem(numRows, 10, QtWidgets.QTableWidgetItem(altitude))
        self.table.setItem(numRows, 11, QtWidgets.QTableWidgetItem(state))
        self.table.setItem(numRows, 12, QtWidgets.QTableWidgetItem(pitch))
        self.table.setItem(numRows, 13, QtWidgets.QTableWidgetItem(roll))
        self.table.setItem(numRows, 14, QtWidgets.QTableWidgetItem(yaw))
        self.table.setItem(numRows, 15, QtWidgets.QTableWidgetItem(donussayisi))
        self.table.setItem(numRows, 16, QtWidgets.QTableWidgetItem(videobilgisi))
        self.table.scrollToBottom()
    #add data callback function
    def addData_callbackFunc(self, value):
            print("Add data: " + str(value))
            self.graph_1.addData(value)
            return
    def dataSendLoop(self,addData_callbackFunc):
        # Setup the signal-slot mechanism.
        mySrc = Communicate()
        mySrc.data_signal.connect(addData_callbackFunc)
    # method to select camera
    def select_camera(self, i=0):
        self.camera = QCamera(self.available_cameras[i])
        self.camera.setViewfinder(self.viewfinder)
        # setting capture mode to the camera
        self.camera.setCaptureMode(QCamera.CaptureStillImage)
       
        # if any error occur show the alert
        self.camera.error.connect(lambda: self.alert(self.camera.errorString()))
        # start the camera

        self.camera.start()
    def stopVideoRecording(self, stop_threads = False):
        while True:
           
            if stop_threads:
                break
    def closeEvent(self, event):
            close = QtWidgets.QMessageBox.question(self,
                                         "QUIT",
                                         "Are you sure want to stop process?",
                                         QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if close == QtWidgets.QMessageBox.Yes:
                event.accept()
                self.disconnect()
                
              
            else:
                event.ignore()
    def config(self):
        try:
            self.serial_object.write("3".encode('utf-8'))
            print('\033[93mKonfigurasyon Komutu Gönderildi.\033[93m')
        except:
            print("Something went wrong. Make sure you have connected.")
    def send(self):
        try:
            self.serial_object.write("1".encode('utf-8'))
            print('\033[93mAyrilma Komutu Gönderildi.\033[93m')
        except:
            print("Something went wrong. Make sure you have connected.")

    ######################################################################    
    def disconnect(self):
        global gps_coors
        global packets
        global q
        global v
        q= 1 
        gps_coors = 0
        packets = 0
        print('\033[93mDISCONNECTED\033[93m')
        self.connectStatusTv.setStyleSheet("color: red; font-size: 14px;font-weight: bold;text-align:center;")
        self.connectStatusTv.setAlignment(QtCore.Qt.AlignCenter)
        self.connectStatusTv.setText("DISCONNECTED")
        # video aktarim
        self.video_aktarim_bilgisi.setText("HAYIR")
        self.video_aktarim_bilgisi.setAlignment(QtCore.Qt.AlignCenter)
        self.video_aktarim_bilgisi.setStyleSheet("color: red; font-size: 10px;font-weight: bold;")
        #close_earth_file()
        try:
            self.serial_object.close()
            self.connectButton.setEnabled(True)
            print("Serial Object Closed")
            session_time = "00 : 00 : 00"
            self.uptimeTv.setText(session_time)
        except AttributeError:
            print('\033[91mPort Closed\033[91m')
        try:
            if self.recordVideo.is_alive():
                v = 1
                return v
        except AttributeError:
            print('\033[91mNo Connection\033[91m')
    def cron(self):
        for h in range (0,24):
            if ( q==1 ):
                break
            for m in range(0,60):
                if (q==1 ):
                    break
                for s in range (0,60):
                    if (q==1 ):
                        break
                    self.uptimeTv.setText("{:02d} : {:02d} : {:02d}".format(h,m,s))
                    time.sleep(1)
    def getUyduStatusu(self, veri):
        if veri == 1:
            self.statu_bekleme.setText( "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:850;color:#ffffff;\">BEKLEMEDE</span></p></body></html>")
            self.statu_bekleme.setStyleSheet("background-color: rgb(0, 128, 0);")
        if veri == 2:
            self.statu_yukselme.setText( "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:850; color:#ffffff;\">YÜKSELME</span></p></body></html>")
            self.statu_yukselme.setStyleSheet("background-color: rgb(0, 128, 0);")
        if veri == 3:
            self.statu_model_uydu_inis.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:850;color:#ffffff;\">MODEL UYDU İNİŞ</span></p></body></html>")
            self.statu_model_uydu_inis.setStyleSheet("background-color: rgb(0, 128, 0);")
        if veri == 4:
            self.statu_ayrilma.setText( "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:850;color:#ffffff;\">AYRILMA</span></p></body></html>")
            self.statu_ayrilma.setStyleSheet("background-color: rgb(0, 128, 0);")
        if veri == 5:
            self.statu_gorevl_yuku_inis.setText( "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:850;color:#ffffff;\">GÖREV YÜKÜ İNİŞ</span></p></body></html>")
            self.statu_gorevl_yuku_inis.setStyleSheet("background-color: rgb(0, 128, 0);")
        if veri == 6:
            self.statu_bonus_gorev.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:850;color:#ffffff;\">BONUS GÖREV</span></p></body></html>")
            self.statu_bonus_gorev.setStyleSheet("background-color: rgb(0, 128, 0);")
        if veri == 7:
            self.statu_kurtarma.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:850;color:#ffffff;\">KURTARMA</span></p></body></html>")
            self.statu_kurtarma.setStyleSheet("background-color: rgb(0, 128, 0);")
        return None


    def get_data(self):
        global serial_object
        global raw_serial
        global filter_data
        global sat_stream1
        global update_period
        global packets
        global writer
        e = 0
        new = time.time()
        while e !=1:   
            try:
                
                time.sleep(0.2)
                serial_data = self.serial_object.readline().decode('utf-8')
                
                if time.time() - new >= update_period:
                    self.connectStatusTv.setStyleSheet("color: red; font-size: 14px;font-weight: bold;text-align:center;")
                    self.connectStatusTv.setAlignment(QtCore.Qt.AlignCenter)
                    self.connectStatusTv.setText("OFFLINE")
                if serial_data != "" :
                    new = time.time()
                    raw_serial = serial_data
                    
                    filter_data = raw_serial.replace("\n","").replace("\r","").replace("\n\r","").replace("[","").replace("]","").replace(" ","")
                    sat_stream1 = filter_data.split(",")
                    
                    try:
                        
                        print(sat_stream1)
                        ## ADD VALUES
                        ## GYROSCOPE
                        
                       
                        #GRAPHS
                        if (sat_stream1[4] != "None"):
                            self.graph_1.addData(float(sat_stream1[4]))
                        
                        
                        if (sat_stream1[5] != "None"):
                            self.graph_2.addData(float(sat_stream1[5]))
                        if (sat_stream1[6] != "None"):
                            self.graph_3.addData(float(sat_stream1[6]))
                        if (sat_stream1[7] != "None"):
                            self.graph_4.addData(float(sat_stream1[7]))
                        if (sat_stream1[8] != "None"):
                            self.graph_5.addData(float(sat_stream1[8]))
                        if (sat_stream1[11] != "None"):
                            self.graph_6.addData(float(sat_stream1[11]))
                        # PITCH ROLL YAW

                        GLWidget.a = float(sat_stream1[13]) # PITCH
                        GLWidget.b = float(sat_stream1[14]) # ROLL
                        GLWidget.c = float(sat_stream1[15]) # YAW
                
                        self.pitchrollyaw.setText("PITCH  "+str(sat_stream1[13])+"    ROLL   "+str(sat_stream1[14])+"      YAW   "+str(sat_stream1[15]))

                        # GPS

                        self.long_var.setText(sat_stream1[10]) # LONGITUDE
                        self.lat_var.setText(sat_stream1[9]) # LATITUDE
                        self.alt_var.setText(sat_stream1[11]) # ALTITUDE

                        # Video aktarim bilgisi
                        if (float (sat_stream1[17]) == 1):
                            self.video_aktarim_bilgisi.setStyleSheet("color: green; font-size: 12px;font-weight: bold;text-align:center;")
                            self.video_aktarim_bilgisi.setText("EVET")
                            self.video_aktarim_bilgisi.setAlignment(QtCore.Qt.AlignCenter)


                        # voltage
                        self.volt_var.setStyleSheet("color: red; font-size: 14px;font-weight: bold;")
                        self.volt_var.setText(sat_stream1[8] + " V")
                        self.curr_var.setText(sat_stream1[18] + " A")
                        self.curr_var.setStyleSheet("color: red; font-size: 14px;font-weight: bold;")
                        power = ((float(sat_stream1[8])* float(sat_stream1[18])))
                        powerRounded = round(power , 2)
                        self.power_Tv.setText(str(powerRounded) + " W")
                        self.power_Tv.setStyleSheet("color: red; font-size: 14px;font-weight: bold;")
                        BATTERY_MIN = 5.0
                        BATTERY_MAX = 11.1
                        batt_percent = ((float(sat_stream1[8]) - BATTERY_MIN)*100)/(BATTERY_MAX-BATTERY_MIN)
                        intBatt = int(batt_percent)
                        self.baterryProgress.setProperty("value", str(intBatt))
    
                        
                        """
                        self.percent = ((float(self.sat_stream1[7]) - 0.4)*100)/(3.7-0.4)
                        print(str(round(self.percent) + " %"))
                        print(sat_stream1[0])   <TAKIM NO>
                        print(sat_stream1[1])   <PAKET NUMARASI>
                        print(sat_stream1[2,3])   <GONDERME SAATI>
                        print(sat_stream1[4])   <BASINC>
                        print(sat_stream1[5])   <YUKSEKLIK>
                        print(sat_stream1[6])   <İNİŞ HIZI>
                        print(sat_stream1[7])   <SICAKLIK>
                        print(sat_stream1[8])   <PIL GERILIMI>
                        print(sat_stream1[9])   <GPS LATITUDE>
                        print(sat_stream1[10])   <GPS LONGITUDE>
                        print(sat_stream1[11])   <GPS ALTITUDE>
                        print(sat_stream1[12])   <UYDU STATÜSÜ>
                        print(sat_stream1[13])   <PITCH>
                        print(sat_stream1[14])   <ROLL>
                        print(sat_stream1[15])   <YAW>
                        print(sat_stream1[16])  <DÖNÜŞ SAYISI>
                        print(sat_stream1[17])  <VİDEO AKTARIM BİLGİSİ>
                        """
                        self.getUyduStatusu(int(sat_stream1[12]))
                       
                        ## ADD TABLE TO ITEM
                       
                        self.addRow(sat_stream1[0], sat_stream1[1],
                                          sat_stream1[2] + sat_stream1[3], 
                                          sat_stream1[4] , sat_stream1[5],
                                          sat_stream1[6] , sat_stream1[7],
                                          sat_stream1[8] , sat_stream1[9],
                                          sat_stream1[10] , sat_stream1[11],
                                          sat_stream1[12] , sat_stream1[13],
                                          sat_stream1[14] , sat_stream1[15],
                                          sat_stream1[16] , sat_stream1[17]
                                          )
                        # save telemetry values
   
                        
                        Telemetry_data = [sat_stream1[0] , sat_stream1[1],
                                          sat_stream1[2] + sat_stream1[3], 
                                          sat_stream1[4] , sat_stream1[5],
                                          sat_stream1[6] , sat_stream1[7],
                                          sat_stream1[8] , sat_stream1[9],
                                          sat_stream1[10] , sat_stream1[11],
                                          sat_stream1[12] , sat_stream1[13],
                                          sat_stream1[14] , sat_stream1[15],
                                          sat_stream1[16], sat_stream1[17] ]
                        with open(session_directory + "/Telemetry.csv",'a',newline='') as file:
                            writer = csv.writer(file,delimiter = ',')
                            writer.writerow(Telemetry_data)
                        
                        
                    except IndexError:
                        print("Index Error")
                else:
                    pass
              
          
            except TypeError:
                e=1
         
            except ValueError:
                print("Value Error")
            
            
               
            except AttributeError:
                e=1
                print('Error','Unable to open serial port')
                
            except (OSError, serial.SerialException):
                print('Port','Port Closed')
                e=1

        
            
    def connect(self):
        global serial_object
        global t_up
        global session_directory
        global q
        global gps_coors
        global packets
 
        port = self.session_com.text()
        baud = self.session_baudrate.text()
        print('\033[92mConnected\033[92m', port, baud)

        try:
            self.serial_object = serial.Serial( str(port), baudrate= baud, timeout = 1)
            self.connectButton.setEnabled(False)

            
            self.connectStatusTv.setStyleSheet("color: green; font-size: 14px;font-weight: bold;text-align:center;")
            self.connectStatusTv.setText("CONNECTED")
            self.connectStatusTv.setAlignment(QtCore.Qt.AlignCenter)
            # Start the thread to read frames from the video stream
            self.sendVideoButton.setEnabled(True)

            self.thread = threading.Thread(target=self.update, args=())
            self.thread.daemon = True
            self.thread.start()
            
            self.recordVideo = threading.Thread(target=self.start_recording_thread, args =())
            self.recordVideo.daemon = True
            self.recordVideo.start()
            
            # Start another thread to show/save frames
            
            print('Video Kaydı basladi {}'.format(video_file))

            ## OUTPUT TELEMETRY VALUES
            session_directory = ofiles_directory + strftime("/%Y-%m-%d_%H%M%S")
            os.makedirs(session_directory)
            with open(session_directory + "/Telemetry.csv",'w',newline='') as file:
                writer = csv.writer(file,delimiter = ',')
                writer.writerow(telemetry_values)
        
        except SerialException:
            print('Error','Enter Baudrate and Port')
            return
        except ValueError:
            print("Enter valid name.")
        
        t1 = threading.Thread(target = self.get_data)
        #t1.daemon = True
        t1.start()
        q=0
        t_up = threading.Thread(target= self.cron)
        t_up.daemon = True
        t_up.start()
    
        
       
        
        
    
def main():
    app = QApplication(sys.argv)
    window = Ui() 
    window.show()
    app.exec_()




if __name__ == "__main__": 
    main()
   
 