from PyQt6.QtWidgets import QDialog, QMessageBox, QComboBox, QLineEdit, QDateEdit, QSpinBox, QPushButton
from PyQt6 import uic
from database import *

class BookingDialog(QDialog):
    def __init__(self):
        super(BookingDialog, self).__init__()
        uic.loadUi('../ui/dialogs/booking_dialog.ui', self)

        # Tìm các combobox trong giao diện
        self.cmb_tour = self.findChild(QComboBox, "cmb_tour")
        self.cmb_khach_hang = self.findChild(QComboBox, "cmb_khach_hang")
        self.cmb_nhan_vien = self.findChild(QComboBox, "cmb_nhan_vien")
        self.cmb_trang_thai = self.findChild(QComboBox, "cmb_trang_thai")
        self.txt_ma_dat = self.findChild(QLineEdit, "txt_ma_dat")
        self.date_ngay_dat = self.findChild(QDateEdit, "date_ngay_dat")
        self.spin_so_luong = self.findChild(QSpinBox, "spin_so_luong")
        self.txt_tong_tien = self.findChild(QLineEdit, "txt_tong_tien")
        self.txt_tien_tt = self.findChild(QLineEdit, "txt_tien_tt")
        self.btn_save = self.findChild(QPushButton, "btn_save")
        self.btn_cancel = self.findChild(QPushButton, "btn_cancel")

        # Kiểm tra combobox
        if not self.cmb_tour or not self.cmb_khach_hang or not self.cmb_nhan_vien:
            QMessageBox.critical(self, "Lỗi", "Không tìm thấy các combobox trong giao diện")
            return

        # Kết nối sự kiện
        self.btn_save.clicked.connect(self.save_booking)
        self.btn_cancel.clicked.connect(self.close)
        
        # Load dữ liệu vào combobox
        self.load_combobox_data()

    def load_combobox_data(self):
        db = db_connect()
        if not db:
            QMessageBox.critical(self, "Lỗi", "Không thể kết nối đến CSDL!")
            return

        cursor = db.cursor()
        try:
            # Load dữ liệu vào combobox tour
            cursor.execute("SELECT MaTour, TenTour FROM tour")
            tours = cursor.fetchall()
            self.cmb_tour.clear()
            for tour in tours:
                self.cmb_tour.addItem(f"{tour[1]} ({tour[0]})", tour[0])

            # Load dữ liệu vào combobox khách hàng
            cursor.execute("SELECT MaKH, HoTen FROM khachhang")
            khach_hangs = cursor.fetchall()
            self.cmb_khach_hang.clear()
            for kh in khach_hangs:
                self.cmb_khach_hang.addItem(f"{kh[1]} ({kh[0]})", kh[0])

            # Load dữ liệu vào combobox nhân viên
            cursor.execute("SELECT MaNV, HoTen FROM nhanvien")
            nhan_viens = cursor.fetchall()
            self.cmb_nhan_vien.clear()
            for nv in nhan_viens:
                self.cmb_nhan_vien.addItem(f"{nv[1]} ({nv[0]})", nv[0])

        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi tải dữ liệu: {e}")
        finally:
            db.close()

    def save_booking(self):
        db = db_connect()
        cursor = db.cursor()
        # Lấy dữ liệu từ các trường nhập liệu
        ma_dat_tour = self.txt_ma_dat.text()
        ma_tour = self.cmb_tour.currentData()
        ma_khach_hang = self.cmb_khach_hang.currentData()
        ma_nhan_vien = self.cmb_nhan_vien.currentData()
        ngay_dat = self.date_ngay_dat.date().toString("yyyy-MM-dd")
        so_luong_nguoi = self.spin_so_luong.value()
        tong_tien = self.txt_tong_tien.text()
        so_tien_da_thanh_toan = self.txt_tien_tt.text()
        trang_thai = self.cmb_trang_thai.currentText()

        if not ma_dat_tour or not ma_tour or not ma_khach_hang or not ma_nhan_vien:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return

        # Thêm thông tin đặt tour vào cơ sở dữ liệu
        cursor.execute("""
            INSERT INTO dattour (MaDatTour, MaTour, MaKH, MaNV, NgayDat, SoLuongNguoi, TongTien, SoTienDaThanhToan, TrangThai)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (ma_dat_tour, ma_tour, ma_khach_hang, ma_nhan_vien, ngay_dat, so_luong_nguoi, tong_tien, so_tien_da_thanh_toan, trang_thai))
        db.commit()
        QMessageBox.information(self, "Thành công", "Thêm tour thành công")
        self.close()

    def cancel(self):
        self.close()