from PyQt5.QtWidgets import QCalendarWidget
from PyQt5.QtGui import QPainter, QBrush, QColor, QTextCharFormat
from PyQt5.QtCore import QRect, QDate
from DBConnection import DBConnection


class CalendarWidget(QCalendarWidget):
    def __init__(self, parent=None):
        super(CalendarWidget, self).__init__(parent)
        self.dates_with_events = DBConnection().get_dates_with_events()

    def paintCell(self, painter: QPainter, rect: QRect, date: QDate):
        super().paintCell(painter, rect, date)
        cell_format = QTextCharFormat()
        cell_format.setBackground(QColor(0, 0, 150, 50))
        if date.toString("yyyy-MM-dd") in self.dates_with_events:
            self.setDateTextFormat(date, cell_format)

            # painter.fillRect(rect, QColor(0, 0, 150, 50))
        # else:
        #     painter.fillRect(rect, QColor(255, 255, 255, 20))
        
