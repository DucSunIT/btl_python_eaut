from PyQt6.QtWidgets import QDialog, QMessageBox, QLineEdit, QDateEdit, QPlainTextEdit, QSpinBox, QComboBox, QPushButton, QDoubleSpinBox
from PyQt6 import uic
from PyQt6.QtCore import QDate
from database import *
import datetime

class EditTourDialog(QDialog):
    def __init__(self, ma_tour):
        super(EditTourDialog, self).__init__()
        uic.loadUi('../ui/dialogs/tour_dialog.ui', self)

        # Tìm các widget trong giao diện
        self.txt_ma_tour = self.findChild(QLineEdit, "txt_ma_tour")
        self.txt_ten_tour = self.findChild(QLineEdit, "txt_ten_tour")
        self.txt_dia_diem = self.findChild(QLineEdit, "txt_dia_diem")
        self.date_bat_dau = self.findChild(QDateEdit, "date_bat_dau")
        self.date_ket_thuc = self.findChild(QDateEdit, "date_ket_thuc")
        self.spin_so_nguoi = self.findChild(QSpinBox, "spin_so_nguoi")
        self.spin_gia_tour = self.findChild(QDoubleSpinBox, "spin_gia_tour")
        self.cmb_trang_thai = self.findChild(QComboBox, "cmb_trang_thai")
        self.txt_mo_ta = self.findChild(QPlainTextEdit, "txt_mo_ta")

        self.txt_ma_tour.setReadOnly(True)

        self.btn_save = self.findChild(QPushButton, "btn_save")
        self.btn_cancel = self.findChild(QPushButton, "btn_cancel")

        self.btn_save.clicked.connect(self.save_tour)
        self.btn_cancel.clicked.connect(self.close)

        self.load_tour_data(ma_tour)

    def load_tour_data(self, ma_tour):
        db = db_connect()
        cursor = db.cursor()
        try:
            cursor.execute("SELECT * FROM tour WHERE MaTour=%s", (ma_tour,))
            data = cursor.fetchone()
            if data:
                self.txt_ma_tour.setText(data[0])
                self.txt_ten_tour.setText(data[1])
                self.txt_dia_diem.setText(data[2])
                self.spin_so_nguoi.setValue(data[5])
                self.spin_gia_tour.setValue(data[6])
                self.cmb_trang_thai.setCurrentText(data[7])
                self.txt_mo_ta.setPlainText(data[8])
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi tải dữ liệu: {e}")
        finally:
            db.close()

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

            # Sửa thông tin tour trong cơ sở dữ liệu
            cursor.execute("UPDATE tour SET TenTour=%s, DiaDiem=%s, NgayKhoiHanh=%s, NgayKetThuc=%s, SoNguoi=%s, Gia=%s, TrangThai=%s, MoTa=%s "
                           "WHERE MaTour=%s", (ten_tour, dia_diem, ngay_bat_dau, ngay_ket_thuc, so_nguoi, gia_tour, trang_thai, mo_ta, ma_tour))
            db.commit()
            if cursor.rowcount > 0:
                QMessageBox.information(self, "Thành công", "Sửa thông tin tour thành công")
            else:
                QMessageBox.warning(self, "Thất bại", "Không có thay đổi nào được thực hiện")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi sửa thông tin tour: {e}")
        finally:
            db.close()

    def cancel(self):
        self.close()