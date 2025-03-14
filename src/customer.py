from PyQt6.QtWidgets import QDialog, QTableWidgetItem, QMessageBox
from PyQt6 import uic
from connect import db_connect
from edit_dialog import EditDialog
from staff_dialog import StaffDialog

class Customer(QDialog):
    def __init__(self, widget):
        super(Customer, self).__init__()
        uic.loadUi('../ui/customer_view.ui', self)
        self.widget = widget

    #     # Kết nối các nút với các phương thức tương ứng
    #     self.btn_add.clicked.connect(self.show_add_dialog)
    #     self.btn_edit.clicked.connect(self.edit_staff)
    #     self.btn_delete.clicked.connect(self.delete_staff)
    #     self.btn_search.clicked.connect(self.search_staff)
    #     self.txt_search.textChanged.connect(self.on_search_text_changed)

    #     self.load_data()

    # def load_data(self):
    #     db = db_connect()
    #     cursor = db.cursor()
    #     cursor.execute("SELECT * FROM nhanvien")
    #     data = cursor.fetchall()
        
    #     # Đặt tiêu đề cho các cột
    #     headers = ["Mã NV", "Họ tên", "Địa chỉ", "Ngày sinh", "Giới tính", "SĐT", "Email", "Chức vụ"]
    #     self.table_staff.setColumnCount(len(headers))
    #     self.table_staff.setHorizontalHeaderLabels(headers)
        
    #     self.table_staff.setRowCount(len(data))

    #     for row_idx, row_data in enumerate(data):
    #         for col_idx, col_data in enumerate(row_data):
    #             self.table_staff.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

    # def show_add_dialog(self):
    #     dialog = StaffDialog()
    #     dialog.exec()
    #     self.load_data()

    # def edit_staff(self):
    #     selected_row = self.table_staff.currentRow()
    #     if selected_row < 0:
    #         QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một nhân viên để sửa!")
    #         return

    #     ma_nv = self.table_staff.item(selected_row, 0).text()
    #     dialog = EditDialog(ma_nv)
    #     dialog.exec()
    #     self.load_data()

    # def delete_staff(self):
    #     selected_row = self.table_staff.currentRow()
    #     if selected_row < 0:
    #         QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một nhân viên để xóa!")
    #         return
    #     res = QMessageBox.question(self, "Xác nhận", f"Bạn muốn xóa nhân viên này")
    #     if res != QMessageBox.StandardButton.Yes:
    #         return
    #     ma_nv = self.table_staff.item(selected_row, 0).text()
    #     db = db_connect()
    #     cursor = db.cursor()
    #     cursor.execute("DELETE FROM nhanvien WHERE MaNV=%s", (ma_nv,))
    #     db.commit()
    #     QMessageBox.information(self, "Thành công", "Xóa nhân viên thành công")
    #     self.load_data()

    # def search_staff(self):
    #     db = db_connect()
    #     cursor = db.cursor()
    #     # Lấy dữ liệu từ trường nhập liệu
    #     name = self.txt_search.text()
    #     ma_nv = self.txt_search.text()
    #     if name == '':
    #         self.load_data()
    #     # Tìm kiếm nhân viên trong cơ sở dữ liệu
    #     cursor.execute("SELECT * FROM nhanvien WHERE HoTen LIKE %s OR MaNV = %s", ('%' + name + '%',  ma_nv ))
    #     data = cursor.fetchall()

    #     if not data:
    #         QMessageBox.information(self, "Thông báo", "Không có dữ liệu phù hợp")
    #         self.table_staff.setRowCount(0)
    #         return

    #     self.table_staff.setRowCount(len(data))
    #     self.table_staff.setColumnCount(len(data[0]))

    #     for row_idx, row_data in enumerate(data):
    #         for col_idx, col_data in enumerate(row_data):
    #             self.table_staff.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

    # def on_search_text_changed(self):
    #     if self.txt_search.text() == '':
    #         self.load_data()