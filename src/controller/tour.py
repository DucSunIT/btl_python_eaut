from PyQt6.QtWidgets import QDialog, QTableWidgetItem, QMessageBox
from PyQt6 import uic
from database import *
from dialog import *

class Tour(QDialog):
    def __init__(self, widget):
        super(Tour, self).__init__()
        uic.loadUi('../ui/views/tour_view.ui', self)
        self.widget = widget

        # Kết nối các nút với các phương thức tương ứng
        self.btn_add.clicked.connect(self.show_add_dialog)
        self.btn_edit.clicked.connect(self.edit_tour)
        self.btn_delete.clicked.connect(self.delete_tour)
        self.btn_search.clicked.connect(self.search_tour)
        self.txt_search.textChanged.connect(self.on_search_text_changed)
        self.btn_exit.clicked.connect(self.exit)
        self.load_data()

    def load_data(self):
        db = db_connect()
        cursor = db.cursor()
        try:
            cursor.execute("SELECT * FROM tour")
            data = cursor.fetchall()
            
            # Đặt tiêu đề cho các cột
            headers = ["Mã Tour", "Tên Tour", "Địa Điểm", "Ngày Khởi Hành", "Ngày Kết Thúc", "Số Người", "Giá", "Trạng Thái", "Mô tả"]
            self.table_tours.setColumnCount(len(headers))
            self.table_tours.setHorizontalHeaderLabels(headers)
            
            self.table_tours.setRowCount(len(data))

            for row_idx, row_data in enumerate(data):
                for col_idx, col_data in enumerate(row_data):
                    self.table_tours.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi tải dữ liệu: {e}")
        finally:
            db.close()

    def show_add_dialog(self):
        dialog = TourDialog()
        dialog.exec()
        self.load_data()

    def edit_tour(self):
        selected_row = self.table_tours.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một tour để sửa!")
            return

        ma_tour = self.table_tours.item(selected_row, 0).text()
        dialog = EditTourDialog(ma_tour)
        dialog.exec()
        self.load_data()

    def delete_tour(self):
        selected_row = self.table_tours.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một tour để xóa!")
            return
        res = QMessageBox.question(self, "Xác nhận", f"Bạn muốn xóa tour này?")
        if res != QMessageBox.StandardButton.Yes:
            return
        ma_tour = self.table_tours.item(selected_row, 0).text()
        db = db_connect()
        cursor = db.cursor()
        try:
            cursor.execute("DELETE FROM tour WHERE MaTour=%s", (ma_tour,))
            db.commit()
            QMessageBox.information(self, "Thành công", "Xóa tour thành công")
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi xóa tour: {e}")
        finally:
            db.close()

    def search_tour(self):
        db = db_connect()
        cursor = db.cursor()
        try:
            # Lấy dữ liệu từ trường nhập liệu
            name = self.txt_search.text()
            ma_tour = self.txt_search.text()
            if name == '':
                self.load_data()
                return
            # Tìm kiếm tour trong cơ sở dữ liệu
            cursor.execute("SELECT * FROM tour WHERE TenTour LIKE %s OR MaTour = %s", ('%' + name + '%',  ma_tour ))
            data = cursor.fetchall()

            if not data:
                QMessageBox.information(self, "Thông báo", "Không có dữ liệu phù hợp")
                self.table_tours.setRowCount(0)
                return

            self.table_tours.setRowCount(len(data))
            self.table_tours.setColumnCount(len(data[0]))

            for row_idx, row_data in enumerate(data):
                for col_idx, col_data in enumerate(row_data):
                    self.table_tours.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi tìm kiếm tour: {e}")
        finally:
            db.close()

    def on_search_text_changed(self):
        if self.txt_search.text() == '':
            self.load_data()
    def exit(self):
        self.widget.setCurrentIndex(0)