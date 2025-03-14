from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6 import uic
from database import *

class CustomerDialog(QDialog):
    def __init__(self):
        super(CustomerDialog, self).__init__()
        uic.loadUi('../ui/dialogs/customer_dialog.ui', self)

        self.btn_save.clicked.connect(self.save_customer)
        self.btn_cancel.clicked.connect(self.close)

    def save_customer(self):
        db = db_connect()
        cursor = db.cursor()
        try:
            # Lấy dữ liệu từ các trường nhập liệu
            ma_kh = self.txt_ma_kh.text()
            ho_ten = self.txt_ho_ten.text()
            so_dien_thoai = self.txt_sdt.text()
            email = self.txt_email.text()
            ngay_sinh = self.date_ngay_sinh.date().toString("yyyy-MM-dd")
            dia_chi = self.txt_dia_chi.toPlainText()

            if self.txt_ma_kh.text() == '' or self.txt_ho_ten.text() == '' or self.txt_sdt.text() == '' or self.txt_email.text() == '' or self.txt_dia_chi.toPlainText() == '':
                QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin!")
                return

            # Thêm khách hàng vào cơ sở dữ liệu
            cursor.execute("""
                INSERT INTO khachhang (MaKH, HoTen, SDT, Email, NgaySinh, DiaChi)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (ma_kh, ho_ten, so_dien_thoai, email, ngay_sinh, dia_chi))
            db.commit()
            QMessageBox.information(self, "Thành công", "Thêm khách hàng thành công")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi thêm khách hàng: {e}")
        finally:
            db.close()

    def cancel(self):
        self.close()