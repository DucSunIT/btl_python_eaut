from PyQt6.QtWidgets import QDialog, QMessageBox, QLineEdit, QDateEdit, QRadioButton, QPlainTextEdit
from PyQt6 import uic
from database import *

class EditStaffDialog(QDialog):
    def __init__(self, ma_nv):
        super(EditStaffDialog, self).__init__()
        uic.loadUi('../ui/dialogs/staff_dialog.ui', self)

        # Tìm các widget trong giao diện
        self.txt_ma_nv = self.findChild(QLineEdit, "txt_ma_nv")
        self.txt_ho_ten = self.findChild(QLineEdit, "txt_ho_ten")
        self.txt_sdt = self.findChild(QLineEdit, "txt_sdt")
        self.txt_email = self.findChild(QLineEdit, "txt_email")
        self.txt_chuc_vu = self.findChild(QLineEdit, "txt_chuc_vu")
        self.txt_dia_chi = self.findChild(QPlainTextEdit, "txt_dia_chi")
        self.date_ngay_sinh = self.findChild(QDateEdit, "date_ngay_sinh")
        self.rad_nam = self.findChild(QRadioButton, "rad_nam")
        self.rad_nu = self.findChild(QRadioButton, "rad_nu")
        self.txt_ma_nv.setReadOnly(True)

        self.btn_save.clicked.connect(self.save_staff)
        self.btn_cancel.clicked.connect(self.close)

        self.load_staff_data(ma_nv)

    def load_staff_data(self, ma_nv):
        db = db_connect()
        cursor = db.cursor()
        try: 
            cursor.execute("SELECT * FROM nhanvien WHERE MaNV=%s", (ma_nv,))
            data = cursor.fetchone()
            if data:
                self.txt_ma_nv.setText(data[0])
                self.txt_ho_ten.setText(data[1])
                self.txt_dia_chi.setPlainText(data[2])
                self.date_ngay_sinh.setDate(data[3])
                if data[4] == 'Nam':
                    self.rad_nam.setChecked(True)
                else:
                    self.rad_nu.setChecked(True)
                self.txt_sdt.setText(data[5])
                self.txt_email.setText(data[6])
                self.txt_chuc_vu.setText(data[7])
        except Exception as e:
            QMessageBox.warning(self, "Lỗi", f"Lỗi khi tải dữ liệu nhân viên: {e}")
        finally:
            db.close()

    def save_staff(self):
        db = db_connect()
        cursor = db.cursor()
        try:
            # Lấy dữ liệu từ các trường nhập liệu
            ma_nv = self.txt_ma_nv.text()
            ho_ten = self.txt_ho_ten.text()
            so_dien_thoai = self.txt_sdt.text()
            email = self.txt_email.text()
            chuc_vu = self.txt_chuc_vu.text()
            dia_chi = self.txt_dia_chi.toPlainText()
            ngay_sinh = self.date_ngay_sinh.date().toString("yyyy-MM-dd")
            gioi_tinh = 'Nam' if self.rad_nam.isChecked() else 'Nữ'
            # Sửa thông tin nhân viên trong cơ sở dữ liệu
            cursor.execute("UPDATE nhanvien SET HoTen=%s, DiaChi=%s, NgaySinh=%s, GioiTinh=%s, SDT=%s, Email=%s, ChucVu=%s "
                        "WHERE MaNV=%s", (ho_ten, dia_chi, ngay_sinh, gioi_tinh, so_dien_thoai, email, chuc_vu, ma_nv))
            db.commit()
            if cursor.rowcount > 0:
                QMessageBox.information(self, "Thành công", "Sửa thông tin nhân viên thành công")
            else:
                QMessageBox.warning(self, "Thất bại", "Không có thay đổi nào được thực hiện")
            self.close()
        except Exception as e:
            QMessageBox.warning(self, "Lỗi", f"Lỗi khi sửa thông tin nhân viên: {e}")
        finally:    
            db.close()

    def cancel(self):
        self.close()