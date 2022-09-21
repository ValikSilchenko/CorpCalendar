import datetime
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from DBConnection import DBConnection


class EventDialog(QDialog):
    event_data = QtCore.pyqtSignal()
    load_events = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(EventDialog, self).__init__(parent)
        self.setup_ui()
        self.event_id = None

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
        self.buttonBox.buttons()[1].setText("Отмена")
        self.buttonBox.buttons()[0].setText("Ок")
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

        self.deleteButton = QPushButton(self)
        self.deleteButton.setObjectName(u"deleteButton")
        self.deleteButton.setText("Удалить")
        self.deleteButton.setHidden(True)

        self.editButton = QPushButton(self)
        self.editButton.setObjectName(u"editButton")
        self.editButton.setText("Изменить")
        self.editButton.setHidden(True)

        self.cancelButton = QPushButton(self)
        self.cancelButton.setObjectName(u"cancelButton")
        self.cancelButton.setText("Отмена")
        self.cancelButton.setHidden(True)

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
        self.gridLayout.addWidget(self.deleteButton, 6, 0, 1, 1)
        self.gridLayout.addWidget(self.buttonBox, 6, 0, 1, 3)
        self.gridLayout.addWidget(self.editButton, 6, 1, 1, 1)
        self.gridLayout.addWidget(self.cancelButton, 6, 2, 1, 1)

        self.buttonBox.accepted.connect(self.add_edit_event)
        self.buttonBox.rejected.connect(self.reject)

        self.cancelButton.clicked.connect(self.reject)
        self.deleteButton.clicked.connect(self.delete_event)
        self.editButton.clicked.connect(self.edit_event)

        QtCore.QMetaObject.connectSlotsByName(self)

    def switch_mode(self):
        is_hidden = self.buttonBox.isHidden()
        is_read_only = self.themeEdit.isReadOnly()

        self.buttonBox.setHidden(not is_hidden)
        self.deleteButton.setHidden(is_hidden)
        self.editButton.setHidden(is_hidden)
        self.cancelButton.setHidden(is_hidden)

        self.themeEdit.setReadOnly(not is_read_only)
        self.place.setReadOnly(not is_read_only)
        self.beginningTime.setReadOnly(not is_read_only)
        self.beginningDate.setReadOnly(not is_read_only)
        self.endingDate.setReadOnly(not is_read_only)
        self.textBrowser.setReadOnly(not is_read_only)

    def show(self, date=QtCore.QDate.currentDate()):
        self.event_id = None

        if self.buttonBox.isHidden():
            self.switch_mode()

        self.themeEdit.clear()
        self.place.clear()
        self.beginningTime.setTime(QtCore.QTime.currentTime())
        self.beginningDate.setDate(date)
        self.endingDate.setDate(date)
        self.textBrowser.clear()
        super(EventDialog, self).show()

    def show_event(self, event_id: int):
        self.event_id = event_id

        if not self.buttonBox.isHidden():
            self.switch_mode()

        event_data = DBConnection().get_event_by_id(event_id)
        self.themeEdit.setText(event_data[1])
        self.place.setText(event_data[2])
        self.beginningTime.setTime(QtCore.QTime.fromString(str(event_data[3]), "HH:mm:ss"))
        self.beginningDate.setDate(QtCore.QDate.fromString(str(event_data[4]), "yyyy-MM-dd"))
        self.endingDate.setDate(QtCore.QDate.fromString(str(event_data[5]), "yyyy-MM-dd"))
        self.textBrowser.setText(event_data[6])
        super(EventDialog, self).show()

    def add_edit_event(self):
        if not self.themeEdit.text().isspace() and self.themeEdit.text() != '':
            if self.event_id is None:
                DBConnection().add_event(
                    self.themeEdit.text(),
                    self.place.text(),
                    self.beginningTime.time().toString("HH:mm:ss"),
                    self.beginningDate.date().toString("yyyy-MM-dd"),
                    self.endingDate.date().toString("yyyy-MM-dd"),
                    self.textBrowser.toPlainText())
                self.event_data.emit()
            else:
                DBConnection().update_event(
                    self.event_id,
                    self.themeEdit.text(),
                    self.place.text(),
                    self.beginningTime.time().toString("HH:mm:ss"),
                    self.beginningDate.date().toString("yyyy-MM-dd"),
                    self.endingDate.date().toString("yyyy-MM-dd"),
                    self.textBrowser.toPlainText())
            self.load_events.emit()
            self.close()
        else:
            dial = QMessageBox(self)
            dial.setWindowTitle("Предупреждение")
            dial.setText("Заполните поле \"Тема\".")
            dial.setStandardButtons(QMessageBox.Ok)
            dial.exec()

    def edit_event(self):
        self.switch_mode()
        # DBConnection().update_event(
        #     "id",
        #     self.themeEdit.text(),
        #     self.place.text(),
        #     self.beginningTime.time().toString("HH:mm:ss"),
        #     self.beginningDate.date().toString("yyyy-MM-dd"),
        #     self.endingDate.date().toString("yyyy-MM-dd"),
        #     self.textBrowser.toPlainText())

    def delete_event(self):
        dial = QMessageBox(self)
        dial.setWindowTitle("Подтверждение")
        dial.setText("Вы уверены, что хотите удалить это мероприятие?")
        dial.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dial.buttons()[1].setText("Отмена")
        dial.buttons()[0].setText("Да")

        if dial.exec() == QMessageBox.Yes:
            DBConnection().delete_event(self.event_id)
            self.event_data.emit()
            self.load_events.emit()
            self.close()
