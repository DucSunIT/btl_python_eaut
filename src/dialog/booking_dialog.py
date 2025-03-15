from PyQt6.QtWidgets import QDialog, QMessageBox
from PyQt6 import uic
from database import *
class BookingDialog(QDialog):
    def __init__(self):
        super(BookingDialog, self).__init__()
        uic.loadUi('../ui/dialogs/booking_dialog.ui', self)

        self.btn_save.clicked.connect(self.save_booking)
        self.btn_cancel.clicked.connect(self.close)

        self.load_data()
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
            self.cmb_trang_thai.addItems(["Chưa thanh toán", "Đã thanh toán", "Đã hủy"])

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
            tour = self.cmb_tour.currentData()
            khach_hang = self.cmb_khach_hang.currentData()
            nhan_vien = self.cmb_nhan_vien.currentData()
            ngay_dat = self.date_ngay_dat.date().toString("yyyy-MM-dd")
            so_luong_khach = self.spin_so_luong.value()
            tong_tien = self.txt_tong_tien.text()
            so_tien_da_thanh_toan = self.txt_tien_tt.text()
            trang_thai = self.cmb_trang_thai.currentText()

            if not ma_dat_tour or not tour or not khach_hang or not nhan_vien or not ngay_dat or not so_luong_khach or not tong_tien or not so_tien_da_thanh_toan or not trang_thai:
                QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin")
                return
            
            # Debugging information
            print(f"TrangThai: {trang_thai}")

            # Thêm khách hàng vào cơ sở dữ liệu
            cursor.execute("""
                INSERT INTO dattour (MaDatTour, MaKH, MaTour, NgayDat, SoLuongNguoi, TongTien, SoTienDaThanhToan, MaNV, TrangThai)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (ma_dat_tour, khach_hang, tour, ngay_dat, so_luong_khach, tong_tien, so_tien_da_thanh_toan, nhan_vien, trang_thai))
            db.commit()
            QMessageBox.information(self, "Thành công", "Thêm tour thành công")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi thêm tour: {e}")
        finally:
            db.close()

    def cancel(self):
        self.close()