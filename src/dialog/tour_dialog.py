from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6 import uic
from database import *

class TourDialog(QDialog):
    def __init__(self):
        super(TourDialog, self).__init__()
        uic.loadUi('../ui/dialogs/tour_dialog.ui', self)

        self.btn_save.clicked.connect(self.save_tour)
        self.btn_cancel.clicked.connect(self.close)

    def save_tour(self):
        db = db_connect()
        cursor = db.cursor()
        try:
            # Lấy dữ liệu từ các trường nhập liệu
            ma_tour = self.txt_ma_tour.text()
            ten_tour = self.txt_ten_tour.text()
            dia_diem = self.txt_dia_diem.text()
            ngay_bat_dau = self.date_bat_dau.date().toString("yyyy-MM-dd")
            ngay_ket_thuc = self.date_ket_thuc.date().toString("yyyy-MM-dd")
            so_nguoi = self.spin_so_nguoi.value()
            gia_tour = self.spin_gia_tour.value()
            trang_thai = self.cmb_trang_thai.currentText()
            mo_ta = self.txt_mo_ta.toPlainText()
            if self.txt_ma_tour.text() == '' or self.txt_ten_tour.text() == '' or self.txt_dia_diem.text() == '' or self.txt_mo_ta.toPlainText() == '':
                QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin!") # Thông báo lỗi nếu có trường nào trống
                return
            # Thêm tour vào cơ sở dữ liệu
            cursor.execute("""
                INSERT INTO tour (MaTour, TenTour, DiaDiem, NgayKhoiHanh, NgayKetThuc, SoNguoi, Gia, TrangThai, MoTa)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (ma_tour, ten_tour, dia_diem, ngay_bat_dau, ngay_ket_thuc, so_nguoi, gia_tour, trang_thai, mo_ta))
            db.commit()
            QMessageBox.information(self, "Thành công", "Thêm tour thành công")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi thêm tour: {e}")
        finally:
            db.close()

    def cancel(self):
        self.close()