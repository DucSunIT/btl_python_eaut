from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from PyQt6 import uic

class Main_w(QMainWindow):
    def __init__(self, widget):
        super(Main_w, self).__init__()
        uic.loadUi('../ui/main_window.ui', self)
        self.widget = widget
        self.resize(848, 580)
        # Tìm QStackedWidget trong giao diện
        self.stackedWidget = self.findChild(QStackedWidget, "stackedWidget")

        # Kết nối các nút với các phương thức chuyển đổi view
        self.btn_staff.clicked.connect(self.show_staff)
        self.btn_customers.clicked.connect(self.show_customers)
        self.btn_tours.clicked.connect(self.show_tours)
        self.btn_bookings.clicked.connect(self.show_bookings)
        self.btn_statistics.clicked.connect(self.show_statistics)

    def show_staff(self):
        self.stackedWidget.setCurrentIndex(0)

    def show_customers(self):
        self.stackedWidget.setCurrentIndex(1)

    def show_tours(self):
        self.stackedWidget.setCurrentIndex(2)

    def show_bookings(self):
        self.stackedWidget.setCurrentIndex(3)

    def show_statistics(self):
        self.stackedWidget.setCurrentIndex(4)