from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication
import sys
from login import Login_w
from main_window import Main_w
from controller import *
from database import *
from dialog import *

app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()

Login_f = Login_w(widget)
Main_f = Main_w(widget)
Staff_f = Staff(widget)
Customers_f = Customer(widget)
Tours_f = Tour(widget)
Bookings_f = Booking(widget)
Statistics_f = Statistics(widget)


widget.addWidget(Login_f) #0
widget.addWidget(Main_f) #1

# Thêm các view vào QStackedWidget trong Main_w
Main_f.stackedWidget.addWidget(Staff_f) #0
Main_f.stackedWidget.addWidget(Customers_f) #1
Main_f.stackedWidget.addWidget(Tours_f) #2
Main_f.stackedWidget.addWidget(Bookings_f) #3
Main_f.stackedWidget.addWidget(Statistics_f) #4

widget.setCurrentIndex(0)
widget.show()
app.exec()