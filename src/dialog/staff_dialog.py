from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6 import uic
from database import *

class StaffDialog(QDialog):
    def __init__(self):
        super(StaffDialog, self).__init__()
        uic.loadUi('../ui/dialogs/staff_dialog.ui', self)

        self.btn_save.clicked.connect(self.save_staff)
        self.btn_cancel.clicked.connect(self.close)


    def save_staff(self):
        db = db_connect()
        cursor = db.cursor()
        # Lấy dữ liệu từ các trường nhập liệu
        ma_nv = self.txt_ma_nv.text()
        ho_ten = self.txt_ho_ten.text()
        so_dien_thoai = self.txt_sdt.text()
        email = self.txt_email.text()
        chuc_vu = self.txt_chuc_vu.text()
        dia_chi = self.txt_dia_chi.toPlainText()
        ngay_sinh = self.date_ngay_sinh.date().toString("yyyy-MM-dd")
        gioi_tinh = 'Nam' if self.rad_nam.isChecked() else 'Nữ'
        if self.txt_ma_nv.text() == '' or self.txt_ho_ten.text() == '' or self.txt_sdt.text() == '' or self.txt_email.text() == '' or self.txt_chuc_vu.text() == '' or self.txt_dia_chi.toPlainText() == '':
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return
        # Thêm nhân viên vào cơ sở dữ liệu
        try: 
            cursor.execute("""
                INSERT INTO nhanvien (MaNV, HoTen, DiaChi, NgaySinh, GioiTinh, SDT, Email, ChucVu)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (ma_nv, ho_ten, dia_chi, ngay_sinh, gioi_tinh, so_dien_thoai, email, chuc_vu))
            db.commit()
            QMessageBox.information(self, "Thành công", "Thêm nhân viên thành công")
            self.close()
        except Exception as e:
            QMessageBox.warning(self, "Lỗi", f"Lỗi khi thêm nhân viên: {e}")
        finally:
            db.close()

    def cancel(self):
        self.close()