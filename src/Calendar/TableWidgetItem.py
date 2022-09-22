from PyQt5.QtWidgets import QTableWidgetItem


class TableWidgetItem(QTableWidgetItem):
    def __init__(self, event_id: int, text):
        super(TableWidgetItem, self).__init__(text)
        self.id = event_id
