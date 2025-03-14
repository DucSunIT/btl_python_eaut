from PyQt6.QtWidgets import QDialog, QMessageBox, QApplication
from PyQt6 import uic
from database import *

class Login_w(QDialog):
    def __init__(self, widget):
        super(Login_w, self).__init__()
        uic.loadUi('../ui/dialogs/login_dialog.ui', self)
        self.widget = widget
        self.setGeometry(100, 100, 400, 300)  # Đặt kích thước và vị trí cho cửa sổ đăng nhập
        self.btn_login.clicked.connect(self.login)

    def login(self):
        un = self.txt_username.text()
        pw = self.txt_password.text()
        db = db_connect()
        print("Kết nối CSDL thành công -- Login!")

        if self.txt_username.text() == '' or self.txt_password.text() == '':
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return

        cursor = db.cursor()
        try:
            cursor.execute("SELECT * FROM taikhoan WHERE TenDangNhap = %s AND MatKhau = %s", (un, pw))
            data = cursor.fetchone()
            if data:
                QMessageBox.information(self, 'Đăng Nhập', 'Đăng nhập thành công')
                self.widget.setCurrentIndex(1)
            else:
                QMessageBox.warning(self, 'Đăng Nhập', 'Đăng nhập thất bại')
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi đăng nhập: {e}")
        finally:
            db.close()
