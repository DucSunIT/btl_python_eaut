from PyQt6.QtWidgets import QDialog, QTableWidgetItem, QMessageBox
from PyQt6 import uic
from connect import db_connect
from edit_dialog import EditDialog
from staff_dialog import StaffDialog

class Booking(QDialog):
    def __init__(self, widget):
        super(Booking, self).__init__()
        uic.loadUi('../ui/booking_view.ui', self)
        self.widget = widget

        