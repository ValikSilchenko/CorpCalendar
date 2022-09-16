from PyQt5 import QtCore
from PyQt5.QtWidgets import *


class EventDialog(QDialog):
    event_data = QtCore.pyqtSignal(str, str, str, str, str, str)

    def __init__(self, parent=None):
        super(EventDialog, self).__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        if self.objectName():
            self.setObjectName(u"EventDialog")
        self.setWindowTitle("Create event")
        self.resize(365, 385)

        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName(u"gridLayout")

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)

        self.textBrowser = QTextBrowser(self)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setReadOnly(False)

        self.themeEdit = QLineEdit(self)
        self.themeEdit.setObjectName(u"themeEdit")

        self.beginningDate = QDateEdit(self)
        self.beginningDate.setObjectName(u"beginningDate")
        self.beginningDate.setCalendarPopup(True)

        self.endingDate = QDateEdit(self)
        self.endingDate.setObjectName(u"endingDate")
        self.endingDate.setCalendarPopup(True)

        self.beginningTime = QTimeEdit(self)
        self.beginningTime.setObjectName(u"beginningTime")

        self.place = QLineEdit(self)
        self.place.setObjectName(u"place")

        self.themeLabel = QLabel(self)
        self.themeLabel.setObjectName(u"themeLabel")
        self.themeLabel.setGeometry(QtCore.QRect(5, 10, 60, 20))
        self.themeLabel.setText("Тема")

        self.beginningLabel = QLabel(self)
        self.beginningLabel.setObjectName(u"beginningLabel")
        self.beginningLabel.setGeometry(QtCore.QRect(5, 50, 60, 20))
        self.beginningLabel.setText("Начало")

        self.endingLabel = QLabel(self)
        self.endingLabel.setObjectName(u"endingLabel")
        self.endingLabel.setGeometry(QtCore.QRect(5, 80, 60, 20))
        self.endingLabel.setText("Окончание")

        self.placeLabel = QLabel(self)
        self.placeLabel.setObjectName(u"placeLabel")
        self.placeLabel.setText("Место")

        self.commentLabel = QLabel(self)
        self.commentLabel.setObjectName(u"commentLabel")
        self.commentLabel.setGeometry(QtCore.QRect(150, 110, 70, 15))
        self.commentLabel.setText("Комментарий")

        self.gridLayout.addWidget(self.themeLabel, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.themeEdit, 0, 1, 1, 2)
        self.gridLayout.addWidget(self.beginningLabel, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.beginningDate, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.beginningTime, 1, 2, 1, 1)
        self.gridLayout.addWidget(self.endingLabel, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.endingDate, 2, 1, 1, 1)
        self.gridLayout.addWidget(self.placeLabel, 3, 0, 1, 1)
        self.gridLayout.addWidget(self.place, 3, 1, 1, 2)
        self.gridLayout.addWidget(self.commentLabel, 4, 1, 1, 2)
        self.gridLayout.addWidget(self.textBrowser, 5, 0, 1, 3)
        self.gridLayout.addWidget(self.buttonBox, 6, 0, 1, 3)

        self.buttonBox.accepted.connect(self.send_to_main)
        self.buttonBox.rejected.connect(self.reject)

        QtCore.QMetaObject.connectSlotsByName(self)

    def show(self, date=QtCore.QDate.currentDate()):
        self.themeEdit.clear()
        self.place.clear()
        self.beginningTime.setTime(QtCore.QTime.currentTime())
        self.beginningDate.setDate(date)
        self.endingDate.setDate(date)
        self.textBrowser.clear()
        super(EventDialog, self).show()

    def send_to_main(self):
        self.event_data.emit(
            self.themeEdit.text(),
            self.place.text(),
            self.beginningTime.time().toString("HH:mm:ss"),
            self.beginningDate.date().toString("yyyy-MM-dd"),
            self.endingDate.date().toString("yyyy-MM-dd"),
            self.textBrowser.toPlainText()
        )
        self.close()
