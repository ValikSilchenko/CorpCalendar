from PyQt5 import QtCore, QtWidgets, QtGui
from EventDialog import EventDialog
from CalendarWidget import CalendarWidget
from ListWidgetItem import ListWidgetItem
from TableWidgetItem import TableWidgetItem
from DBConnection import DBConnection


class MainWindow(QtWidgets.QMainWindow):
    """

    Класс основного окна
    self.dialog - дочернее окно

    """
    def __init__(self):
        """Конструктор"""
        super().__init__()
        self.setup_ui()
        self.dialog = EventDialog(self)
        self.dialog.event_data[QtCore.QDate].connect(self.after_create_event)
        self.dialog.load_events.connect(self.load_events)
        self.load_events()

    def setup_ui(self):
        """Функция создания объектов окна (виджетов)"""
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

        self.listViewButton = QtWidgets.QRadioButton(self.centralwidget)
        self.listViewButton.setObjectName("listViewButton")
        self.listViewButton.setChecked(True)
        self.horizontalLayout.addWidget(self.listViewButton)

        self.tableViewButton = QtWidgets.QRadioButton(self.centralwidget)
        self.tableViewButton.setObjectName("tableViewButton")
        self.horizontalLayout.addWidget(self.tableViewButton)

        self.buttonGroup = QtWidgets.QButtonGroup(self)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.listViewButton)
        self.buttonGroup.addButton(self.tableViewButton)
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
        self.listWidget.setFont(QtGui.QFont("MS Shell Dlg 2", 12))
        self.gridLayout.addWidget(self.listWidget, 1, 3, 1, 3)
        self.listWidget.itemClicked.connect(self.show_event_dialog)  # регистрирование нажатия на элемент списка

        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setMinimumSize(QtCore.QSize(360, 370))
        self.tableWidget.setSortingEnabled(self.tableWidget.isSortingEnabled())
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem("Тема"))
        self.tableWidget.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem("Место"))
        self.tableWidget.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem("Время"))
        self.tableWidget.setHorizontalHeaderItem(3, QtWidgets.QTableWidgetItem("Дата начала"))
        self.tableWidget.setHorizontalHeaderItem(4, QtWidgets.QTableWidgetItem("Дата окончания"))
        self.tableWidget.setHorizontalHeaderItem(5, QtWidgets.QTableWidgetItem("Комментарий"))
        self.tableWidget.setFont(QtGui.QFont("MS Shell Dlg 2", 12))
        self.tableWidget.itemClicked.connect(self.show_event_dialog)  # регистрирование нажатия на элемент таблицы
        self.tableWidget.setHidden(True)

        self.gridLayout.addWidget(self.tableWidget, 1, 3, 1, 3)

        self.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 20))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)

        self.pushButton.clicked.connect(self.show_create_event_dialog)   # регистрирование нажатия на кнопку "Создать"
        self.buttonGroup.buttonClicked.connect(self.change_items_view)  # регистрирование нажатия на кнопки "Список" и "Таблица"

        self.setWindowTitle("Календарь мероприятий")
        self.pushButton.setText("Создать")
        self.listViewButton.setText("Список")
        self.tableViewButton.setText("Таблица")

        QtCore.QMetaObject.connectSlotsByName(self)

    def show_event_dialog(self):
        """Показ диалога с данными о мероприятии"""
        if self.listViewButton.isChecked():
            self.dialog.show_event(self.listWidget.currentItem().id)
        else:
            self.dialog.show_event(self.tableWidget.currentItem().id)

    def show_create_event_dialog(self):
        """Показ пустого диалога для создания мероприятия"""
        if self.dialog.isHidden():
            self.dialog.show(self.calendarWidget.selectedDate())

    def load_events(self):
        """Загрузка всех мероприятий на выбранную в календаре дату"""
        self.listWidget.clear()
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        events = DBConnection().get_events_by_date(self.calendarWidget.selectedDate().toString("yyyy-MM-dd"))
        for event in events:
            rows = self.tableWidget.rowCount()
            self.listWidget.addItem(ListWidgetItem(event[0], event[1], self.listWidget))

            self.tableWidget.setRowCount(rows + 1)
            self.tableWidget.setVerticalHeaderItem(rows, QtWidgets.QTableWidgetItem(rows + 1))

            self.tableWidget.setItem(rows, 0, TableWidgetItem(event[0], event[1]))
            self.tableWidget.item(rows, 0).setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)

            self.tableWidget.setItem(rows, 1, TableWidgetItem(event[0], event[2]))
            self.tableWidget.item(rows, 1).setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)

            self.tableWidget.setItem(rows, 2, TableWidgetItem(event[0], event[3].strftime("%H:%M:%H")))
            self.tableWidget.item(rows, 2).setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)

            self.tableWidget.setItem(rows, 3, TableWidgetItem(event[0], event[4].strftime("%Y-%m-%d")))
            self.tableWidget.item(rows, 3).setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)

            self.tableWidget.setItem(rows, 4, TableWidgetItem(event[0], event[5].strftime("%Y-%m-%d")))
            self.tableWidget.item(rows, 4).setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)

            self.tableWidget.setItem(rows, 5, TableWidgetItem(event[0], event[6]))
            self.tableWidget.item(rows, 5).setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)

    def change_items_view(self):
        """Изменение способа отображения мероприятий (список или таблица)"""
        if self.listViewButton.isChecked():
            self.listWidget.setHidden(False)
            self.tableWidget.setHidden(True)
        else:
            self.listWidget.setHidden(True)
            self.tableWidget.setHidden(False)

    def after_create_event(self, date: QtCore.QDate):
        """Перекрашивание ячеек после действий с мероприятиями"""
        cell_format = QtGui.QTextCharFormat()
        if DBConnection().get_events_by_date(date.toString("yyyy-MM-dd")):
            cell_format.setBackground(QtGui.QColor(0, 0, 150, 50))
        else:
            cell_format.setBackground(QtGui.QColor(255, 255, 255, 100))

        self.calendarWidget.setDateTextFormat(date, cell_format)
