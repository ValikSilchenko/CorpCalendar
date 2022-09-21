from PyQt5 import QtCore, QtWidgets, QtGui
from EventDialog import EventDialog
from CalendarWidget import CalendarWidget
from ListWidgetItem import ListWidgetItem
from DBConnection import DBConnection


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.dialog = EventDialog(self)
        self.dialog.event_data.connect(self.after_create_event)
        self.dialog.load_events.connect(self.load_events)
        self.load_events()

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
        self.calendarWidget.setStyleSheet('''selection-background-color: rgba(50, 50, 50, 80);
        hover: rgba(120, 185, 180, 50);''')
        self.gridLayout.addWidget(self.calendarWidget, 1, 0, 1, 2)

        self.calendarWidget.selectionChanged.connect(self.load_events)

        spacerItem2 = QtWidgets.QSpacerItem(310, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 2, 1, 1)

        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setMinimumSize(QtCore.QSize(360, 370))
        self.listWidget.setObjectName("listWidget")
        self.gridLayout.addWidget(self.listWidget, 1, 3, 1, 3)
        self.listWidget.itemClicked.connect(self.show_event_dialog)

        self.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 20))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)

        self.pushButton.clicked.connect(self.show_create_event_dialog)

        self.setWindowTitle("CorpCalendar")
        self.pushButton.setText("PushButton")
        self.radioButton.setText("RadioButton")
        self.radioButton_2.setText("RadioButton")

        QtCore.QMetaObject.connectSlotsByName(self)

    def show_event_dialog(self):
        self.dialog.show_event(self.listWidget.currentItem().id)

    def show_create_event_dialog(self):
        if self.dialog.isHidden():
            self.dialog.show(self.calendarWidget.selectedDate())

    def load_events(self):
        self.listWidget.clear()
        events = DBConnection().get_events_by_date(self.calendarWidget.selectedDate().toString("yyyy-MM-dd"))
        for event in events:
            self.listWidget.addItem(ListWidgetItem(event[0], event[1], self.listWidget))

    def after_create_event(self):
        cell_format = QtGui.QTextCharFormat()
        if DBConnection().get_events_by_date(self.calendarWidget.selectedDate().toString("yyyy-MM-dd")):
            cell_format.setBackground(QtGui.QColor(0, 0, 150, 50))
        else:
            cell_format.setBackground(QtGui.QColor(255, 255, 255, 50))
            print('/')

        self.calendarWidget.setDateTextFormat(self.calendarWidget.selectedDate(), cell_format)
        self.calendarWidget.selectedDate()

