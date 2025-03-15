from PyQt6.QtWidgets import QDialog, QMessageBox, QLineEdit, QDateEdit, QComboBox, QSpinBox, QPushButton
from PyQt6 import uic
from PyQt6.QtCore import QDate
from database import *

class EditBookingDialog(QDialog):
    def __init__(self, ma_dat_tour):
        super(EditBookingDialog, self).__init__()
        uic.loadUi('../ui/dialogs/booking_dialog.ui', self)

        # Tìm các widget trong giao diện
        self.txt_ma_dat = self.findChild(QLineEdit, "txt_ma_dat")
        self.cmb_tour = self.findChild(QComboBox, "cmb_tour")
        self.cmb_khach_hang = self.findChild(QComboBox, "cmb_khach_hang")
        self.cmb_nhan_vien = self.findChild(QComboBox, "cmb_nhan_vien")
        self.date_ngay_dat = self.findChild(QDateEdit, "date_ngay_dat")
        self.spin_so_luong = self.findChild(QSpinBox, "spin_so_luong")
        self.txt_tong_tien = self.findChild(QLineEdit, "txt_tong_tien")
        self.txt_tien_tt = self.findChild(QLineEdit, "txt_tien_tt")
        self.cmb_trang_thai = self.findChild(QComboBox, "cmb_trang_thai")

        self.txt_ma_dat.setReadOnly(True)

        self.btn_save = self.findChild(QPushButton, "btn_save")
        self.btn_cancel = self.findChild(QPushButton, "btn_cancel")

        self.btn_save.clicked.connect(self.save_booking)
        self.btn_cancel.clicked.connect(self.close)
        self.load_data()
        self.load_tour_data(ma_dat_tour)
    def load_data(self):
        db = db_connect()
        cursor = db.cursor()
        try:
            # Load data for cmb_tour
            cursor.execute("SELECT MaTour, TenTour FROM tour")
            tours = cursor.fetchall()
            self.cmb_tour.clear()
            for tour in tours:
                self.cmb_tour.addItem(tour[1], tour[0])

            # Load data for cmb_khach_hang
            cursor.execute("SELECT MaKH, HoTen FROM khachhang")
            khach_hangs = cursor.fetchall()
            self.cmb_khach_hang.clear()
            for khach_hang in khach_hangs:
                self.cmb_khach_hang.addItem(khach_hang[1], khach_hang[0])

            # Load data for cmb_nhan_vien
            cursor.execute("SELECT MaNV, HoTen FROM nhanvien")
            nhan_viens = cursor.fetchall()
            self.cmb_nhan_vien.clear()
            for nhan_vien in nhan_viens:
                self.cmb_nhan_vien.addItem(nhan_vien[1], nhan_vien[0])

            # Load data for cmb_trang_thai
            self.cmb_trang_thai.clear()
            self.cmb_trang_thai.addItems(["Chưa thanh toán", "Đã thanh toán", "Đã xác nhân","Đã hủy"])

        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi tải dữ liệu: {e}")
        finally:
            db.close()
    def load_tour_data(self, ma_dat_tour):
        db = db_connect()
        cursor = db.cursor()
        try:
            cursor.execute("SELECT * FROM dattour WHERE MaDatTour=%s", (ma_dat_tour,))
            data = cursor.fetchone()
            if data:
                self.txt_ma_dat.setText(str(data[0]))
                self.cmb_tour.setCurrentText(str(data[1]))
                self.cmb_khach_hang.setCurrentText(str(data[2]))
                self.date_ngay_dat.setDate(QDate.fromString(str(data[3]), "dd-MM-yyyy"))
                self.spin_so_luong.setValue(int(data[4]))
                self.txt_tong_tien.setText(str(data[5]))
                self.txt_tien_tt.setText(str(data[6]))
                self.cmb_nhan_vien.setCurrentText(str(data[7]))
                self.cmb_trang_thai.setCurrentText(str(data[8]))
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi tải dữ liệu: {e}")
        finally:
            db.close()

    def save_booking(self):
        db = db_connect()
        cursor = db.cursor()
        try:
            # Lấy dữ liệu từ các trường nhập liệu
            ma_dat_tour = self.txt_ma_dat.text()
            ma_khach_hang = self.cmb_khach_hang.currentData()
            ma_tour = self.cmb_tour.currentData()
            ngay_dat = self.date_ngay_dat.date().toString("yyyy-MM-dd")
            so_luong_nguoi = self.spin_so_luong.value()
            tong_tien = self.txt_tong_tien.text()
            so_tien_da_thanh_toan = self.txt_tien_tt.text()
            ma_nhan_vien = self.cmb_nhan_vien.currentData()
            trang_thai = self.cmb_trang_thai.currentText()

            # Sửa thông tin tour trong cơ sở dữ liệu
            cursor.execute("""
                UPDATE dattour SET MaKH=%s, MaTour=%s, NgayDat=%s, SoLuongNguoi=%s, TongTien=%s, SoTienDaThanhToan=%s, MaNV=%s, TrangThai=%s
                WHERE MaDatTour=%s
            """, (ma_khach_hang, ma_tour, ngay_dat, so_luong_nguoi, tong_tien, so_tien_da_thanh_toan, ma_nhan_vien, trang_thai, ma_dat_tour))
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