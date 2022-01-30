import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import signal


class LoadTable(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super(LoadTable, self).__init__(1, 17, parent)
        self.setFont(QtGui.QFont("Helvetica", 10, QtGui.QFont.Normal, italic=False))   
        headertitle = ("<TAKIM NO>",
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
                       "<VİDEO AKTARIM BİLGİSİ>")
    
        style = "::section {""background-color: lightblue; border-radius:14px; font-size: 7pt; }"
        self.horizontalHeader().setStyleSheet(style)
        self.setHorizontalHeaderLabels(headertitle)
        self.verticalHeader().hide()
        self.horizontalHeader().setHighlightSections(False)

        self.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.setColumnWidth(0, 70)
       

   
                
