from PyQt6.QtWidgets import QDialog, QTableWidgetItem, QMessageBox
from PyQt6 import uic
from database import *
from dialog import *

class Booking(QDialog):
    def __init__(self, widget):
        super(Booking, self).__init__()
        uic.loadUi('../ui/views/booking_view.ui', self)
        self.widget = widget

        # Kết nối các nút với các phương thức tương ứng
        self.btn_add.clicked.connect(self.show_add_dialog)
        self.btn_edit.clicked.connect(self.edit_booking)
        self.btn_delete.clicked.connect(self.delete_booking)
        self.btn_search.clicked.connect(self.search_booking)
        self.txt_search.textChanged.connect(self.on_search_text_changed)

        self.load_data()

    def load_data(self):
        db = db_connect()
        print("Kết nối CSDL thành công! -- Booking")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM dattour")
        data = cursor.fetchall()
        
        # Đặt tiêu đề cho các cột
        headers = ["Mã Đặt Tour", "Mã KH" ,"Mã Tour", "Ngày Đặt", "Số lượng người", "Tổng tiền", "Số tiền đã TT", "Mã nhân viên", "Trạng thái"]
        self.table_bookings.setColumnCount(len(headers))
        self.table_bookings.setHorizontalHeaderLabels(headers)
        
        self.table_bookings.setRowCount(len(data))

        for row_idx, row_data in enumerate(data):
            for col_idx, col_data in enumerate(row_data):
                self.table_bookings.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

    def show_add_dialog(self):
        dialog = BookingDialog()
        dialog.exec()
        self.load_data()

    def edit_booking(self):
        selected_row = self.table_bookings.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một tour để sửa!")
            return

        ma_dat_tour = self.table_bookings.item(selected_row, 0).text()
        dialog = EditBookingDialog(ma_dat_tour)
        dialog.exec()
        self.load_data()

    def delete_booking(self):
        selected_row = self.table_bookings.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một tour để xóa!")
            return
        res = QMessageBox.question(self, "Xác nhận", f"Bạn muốn xóa tour hàng này")
        if res != QMessageBox.StandardButton.Yes:
            return
        ma_dat_tour = self.table_bookings.item(selected_row, 0).text()
        db = db_connect()
        cursor = db.cursor()
        cursor.execute("DELETE FROM dattour WHERE MaDatTour=%s", (ma_dat_tour,))
        db.commit()
        QMessageBox.information(self, "Thành công", "Xóa tour thành công")
        self.load_data()

    def search_booking(self):
        db = db_connect()
        cursor = db.cursor()
        # Lấy dữ liệu từ trường nhập liệu
        name = self.txt_search.text()
        ma_dat_tour = self.txt_search.text()
        if name == '':
            self.load_data()
        # Tìm kiếm tour trong cơ sở dữ liệu
        cursor.execute("SELECT * FROM dattour WHERE HoTen LIKE %s OR MaKH = %s", ('%' + name + '%',  ma_dat_tour ))
        data = cursor.fetchall()

        if not data:
            QMessageBox.information(self, "Thông báo", "Không có dữ liệu phù hợp")
            self.table_bookings.setRowCount(0)
            return

        self.table_bookings.setRowCount(len(data))
        self.table_bookings.setColumnCount(len(data[0]))

        for row_idx, row_data in enumerate(data):
            for col_idx, col_data in enumerate(row_data):
                self.table_bookings.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

    def on_search_text_changed(self):
        if self.txt_search.text() == '':
            self.load_data()