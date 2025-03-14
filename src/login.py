from PyQt6.QtWidgets import QDialog, QMessageBox,QApplication
from PyQt6 import uic
from connect import db_connect
import sys
class Login_w(QDialog):
    def __init__(self, widget):
        super(Login_w, self).__init__()
        uic.loadUi('../ui/login_dialog.ui', self)
        self.widget = widget
        self.setGeometry(100, 100, 400, 300)  # Đặt kích thước và vị trí cho cửa sổ đăng nhập
        self.btn_login.clicked.connect(self.login)


    def login(self):
        un = self.txt_username.text()
        pw = self.txt_password.text()
        db = db_connect()

        if self.txt_username.text() == '' or self.txt_password.text() == '':
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return

        res = db.cursor()
        res.execute("SELECT * FROM taikhoan WHERE TenDangNhap = '" + un + "' AND MatKhau = '" + pw + "'")
        data = res.fetchone()
        if data:
            QMessageBox.information(self, 'Đăng Nhập', 'Đăng nhập thành công')
            self.widget.setCurrentIndex(1)
        else:
            QMessageBox.warning(self, 'Đăng Nhập', 'Đăng nhập thất bại')


