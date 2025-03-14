from PyQt6.QtWidgets import QDialog, QMessageBox, QLineEdit, QDateEdit, QPlainTextEdit
from PyQt6 import uic
from database import *

class EditCustomerDialog(QDialog):
    def __init__(self, ma_kh):
        super(EditCustomerDialog, self).__init__()
        uic.loadUi('../ui/dialogs/customer_dialog.ui', self)

        # Tìm các widget trong giao diện
        self.txt_ma_kh = self.findChild(QLineEdit, "txt_ma_kh")
        self.txt_ho_ten = self.findChild(QLineEdit, "txt_ho_ten")
        self.txt_sdt = self.findChild(QLineEdit, "txt_sdt")
        self.txt_email = self.findChild(QLineEdit, "txt_email")
        self.date_ngay_sinh = self.findChild(QDateEdit, "date_ngay_sinh")
        self.txt_dia_chi = self.findChild(QPlainTextEdit, "txt_dia_chi")

        self.txt_ma_kh.setReadOnly(True)

        self.btn_save.clicked.connect(self.save_customer)
        self.btn_cancel.clicked.connect(self.close)

        self.load_staff_data(ma_kh)

    def load_staff_data(self, ma_kh):
        db = db_connect()
        cursor = db.cursor()
        try:
            cursor.execute("SELECT * FROM khachhang WHERE MaKH=%s", (ma_kh,))
            data = cursor.fetchone()
            if data:
                self.txt_ma_kh.setText(data[0])
                self.txt_ho_ten.setText(data[1])
                self.txt_sdt.setText(data[2])
                self.txt_email.setText(data[3])
                if data[4] is not None:
                    self.date_ngay_sinh.setDate(data[4])
                self.txt_dia_chi.setPlainText(data[5])
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi tải dữ liệu: {e}")
        finally:
            db.close()

    def save_customer(self):
        db = db_connect()
        cursor = db.cursor()
        try:
            # Lấy dữ liệu từ các trường nhập liệu
            ma_kh = self.txt_ma_kh.text()
            ho_ten = self.txt_ho_ten.text()
            so_dien_thoai = self.txt_sdt.text()
            email = self.txt_email.text()
            dia_chi = self.txt_dia_chi.toPlainText()
            ngay_sinh = self.date_ngay_sinh.date().toString("yyyy-MM-dd")
            # Sửa thông tin nhân viên trong cơ sở dữ liệu
            cursor.execute("UPDATE khachhang SET HoTen=%s, SDT=%s, Email=%s, NgaySinh=%s, DiaChi=%s "
                           "WHERE MaKH=%s", (ho_ten, so_dien_thoai, email, ngay_sinh, dia_chi, ma_kh))
            db.commit()
            if cursor.rowcount > 0:
                QMessageBox.information(self, "Thành công", "Sửa thông tin khách hàng thành công")
            else:
                QMessageBox.warning(self, "Thất bại", "Không có thay đổi nào được thực hiện")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi sửa thông tin khách hàng: {e}")
        finally:
            db.close()

    def cancel(self):
        self.close()