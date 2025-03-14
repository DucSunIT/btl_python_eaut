from PyQt6.QtWidgets import QDialog, QTableWidgetItem, QMessageBox
from PyQt6 import uic
from database import *


class Statistics(QDialog):
    def __init__(self, widget):
        super(Statistics, self).__init__()
        uic.loadUi('../ui/views/statistics_view.ui', self)
        self.widget = widget

        