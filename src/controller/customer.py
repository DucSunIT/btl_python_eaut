from PyQt6.QtWidgets import QDialog, QTableWidgetItem, QMessageBox
from PyQt6 import uic
from database import *
from dialog import *

class Customer(QDialog):
    def __init__(self, widget):
        super(Customer, self).__init__()
        uic.loadUi('../ui/views/customer_view.ui', self)
        self.widget = widget

        # Kết nối các nút với các phương thức tương ứng
        self.btn_add.clicked.connect(self.show_add_dialog)
        self.btn_edit.clicked.connect(self.edit_customer)
        self.btn_delete.clicked.connect(self.delete_customer)
        self.btn_search.clicked.connect(self.search_customer)
        self.txt_search.textChanged.connect(self.on_search_text_changed)
        self.btn_exit.clicked.connect(self.exit)
        self.load_data()

    def load_data(self):
        db = db_connect()
        print("Kết nối CSDL thành công! -- Customer")
        cursor = db.cursor()
        try:
            cursor.execute("SELECT * FROM khachhang")
            data = cursor.fetchall()
            
            # Đặt tiêu đề cho các cột
            headers = ["Mã KH", "Họ tên", "Số điện thoại", "Email", "Ngày Sinh", "Địa chỉ"]
            self.table_customers.setColumnCount(len(headers))
            self.table_customers.setHorizontalHeaderLabels(headers)
            
            self.table_customers.setRowCount(len(data))

            for row_idx, row_data in enumerate(data):
                for col_idx, col_data in enumerate(row_data):
                    self.table_customers.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi tải dữ liệu: {e}")
        finally:
            db.close()

    def show_add_dialog(self):
        dialog = CustomerDialog()
        dialog.exec()
        self.load_data()

    def edit_customer(self):
        selected_row = self.table_customers.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một nhân viên để sửa!")
            return

        ma_kh = self.table_customers.item(selected_row, 0).text()
        dialog = EditCustomerDialog(ma_kh)
        dialog.exec()
        self.load_data()

    def delete_customer(self):
        selected_row = self.table_customers.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một nhân viên để xóa!")
            return
        res = QMessageBox.question(self, "Xác nhận", f"Bạn muốn xóa khách hàng này")
        if res != QMessageBox.StandardButton.Yes:
            return
        ma_kh = self.table_customers.item(selected_row, 0).text()
        db = db_connect()
        cursor = db.cursor()
        try:
            cursor.execute("DELETE FROM khachhang WHERE MaKH=%s", (ma_kh,))
            db.commit()
            QMessageBox.information(self, "Thành công", "Xóa khách hàng thành công")
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi xóa khách hàng: {e}")
        finally:
            db.close()

    def search_customer(self):
        db = db_connect()
        cursor = db.cursor()
        try:
            # Lấy dữ liệu từ trường nhập liệu
            name = self.txt_search.text()
            ma_kh = self.txt_search.text()
            if name == '':
                self.load_data()
                return
            # Tìm kiếm khách hàng trong cơ sở dữ liệu
            cursor.execute("SELECT * FROM khachhang WHERE HoTen LIKE %s OR MaKH = %s", ('%' + name + '%',  ma_kh ))
            data = cursor.fetchall()

            if not data:
                QMessageBox.information(self, "Thông báo", "Không có dữ liệu phù hợp")
                self.table_customers.setRowCount(0)
                return

            self.table_customers.setRowCount(len(data))
            self.table_customers.setColumnCount(len(data[0]))

            for row_idx, row_data in enumerate(data):
                for col_idx, col_data in enumerate(row_data):
                    self.table_customers.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi tìm kiếm khách hàng: {e}")
        finally:
            db.close()

    def on_search_text_changed(self):
        if self.txt_search.text() == '':
            self.load_data()
    def exit(self):
        self.widget.setCurrentIndex(0)