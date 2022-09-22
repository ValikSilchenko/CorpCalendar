from PyQt5.QtWidgets import QListWidgetItem


class ListWidgetItem(QListWidgetItem):
    def __init__(self, event_id: str, text: str, parent=None):
        super(ListWidgetItem, self).__init__(text, parent)
        self.id = event_id
