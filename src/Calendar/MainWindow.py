from PyQt5 import QtCore, QtWidgets, QtGui
from EventDialog import EventDialog
from CalendarWidget import CalendarWidget


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.dialog = EventDialog(self)
        self.dialog.event_data[str, str, str, str, str, str].connect(self.create_event)

    def setup_ui(self):
        self.setObjectName("MainWindow")
        self.resize(802, 460)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 0, 1, 1)

        spacerItem = QtWidgets.QSpacerItem(210, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 3)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setObjectName("radioButton")
        self.horizontalLayout.addWidget(self.radioButton)

        self.radioButton_2 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_2.setObjectName("radioButton_2")
        self.horizontalLayout.addWidget(self.radioButton_2)

        self.buttonGroup = QtWidgets.QButtonGroup(self)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.radioButton)
        self.buttonGroup.addButton(self.radioButton_2)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 4, 1, 1)

        spacerItem1 = QtWidgets.QSpacerItem(170, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 5, 1, 1)

        self.calendarWidget = CalendarWidget(self.centralwidget)
        self.calendarWidget.setMinimumSize(QtCore.QSize(410, 370))
        self.calendarWidget.setObjectName("calendarWidget")
        self.calendarWidget.setStyleSheet("""selection-background-color: rgba(50, 50, 50, 80);
        hover: rgba(120, 185, 180, 50);""")
        self.gridLayout.addWidget(self.calendarWidget, 1, 0, 1, 2)

        spacerItem2 = QtWidgets.QSpacerItem(310, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 2, 1, 1)

        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setMinimumSize(QtCore.QSize(360, 370))
        self.listWidget.setObjectName("listWidget")
        self.gridLayout.addWidget(self.listWidget, 1, 3, 1, 3)
        self.listWidget.itemClicked.connect()

        self.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 20))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)

        self.pushButton.clicked.connect(self.show_event_dialog)

        self.setWindowTitle("CorpCalendar")
        self.pushButton.setText("PushButton")
        self.radioButton.setText("RadioButton")
        self.radioButton_2.setText("RadioButton")

        QtCore.QMetaObject.connectSlotsByName(self)

    def show_event_dialog(self):
        if self.dialog.isHidden():
            self.dialog.show(self.calendarWidget.selectedDate())

    def create_event(
            self, theme: str, place: str, beginning_time: str, beginning_date: str, ending_date: str, comment: str
    ):
        self.calendarWidget.db.add_to_db(theme, place, beginning_time, beginning_date, ending_date, comment)
        cell_format = QtGui.QTextCharFormat()
        cell_format.setBackground(QtGui.QColor(0, 0, 150, 50))
        self.calendarWidget.setDateTextFormat(QtCore.QDate.fromString(beginning_date, "yyyy-MM-dd"), cell_format)
        self.calendarWidget.setSelectedDate(self.calendarWidget.selectedDate())

