from PyQt6.QtWidgets import QDialog, QMessageBox, QTableWidgetItem,QVBoxLayout
from PyQt6 import uic
from database import db_connect
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
import matplotlib.pyplot as plt

class Statistics(QDialog):
    def __init__(self, widget):
        super(Statistics, self).__init__()
        uic.loadUi('../ui/views/statistics_view.ui', self)
        self.widget = widget
        # Kết nối sự kiện chọn loại biểu đồ
        self.cmb_chart_type.currentIndexChanged.connect(self.on_chart_type_changed)
        self.load_data()
        self.btn_refresh.clicked.connect(self.load_data)
        self.btn_exit.clicked.connect(self.exit)


    def load_data(self):
        db = db_connect()
        cursor = db.cursor()
        try:
            cursor.execute("SELECT COUNT(*) AS TongSoDonDatTour FROM dattour")
            data = cursor.fetchall()
            if data:
                self.lbl_total_bookings.setText(str(data[0][0]))
            else:
                self.lbl_total_bookings.setText("0")

            cursor.execute("SELECT SUM(TongTien) AS TongDoanhThu FROM dattour")
            data = cursor.fetchall()
            if data and data[0][0] is not None:
                total_revenue = data[0][0]
                formatted_revenue = "{:,.0f}".format(total_revenue)
                self.lbl_total_revenue.setText(formatted_revenue)
            else:
                self.lbl_total_revenue.setText("0")

            cursor.execute("SELECT COUNT(DISTINCT MaKH) AS TongSoKhachHang FROM dattour")
            data = cursor.fetchall()
            if data:
                self.lbl_total_customers.setText(str(data[0][0]))
            else:
                self.lbl_total_customers.setText("0")
            self.load_tours()
            self.load_staff()
            self.load_chart_yearly()
            self.load_chart_monthly()

        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi tải dữ liệu: {e}")
        finally:
            cursor.close()
            db.close()

    def exit(self):
        if self.widget:
            self.widget.setCurrentIndex(0)
        else:
            QMessageBox.warning(self, "Cảnh báo", "Không thể thoát vì widget không tồn tại.")

    def load_tours(self):
        db = db_connect()
        cursor = db.cursor()
        try:
            cursor.execute("""
                           SELECT 
                            t.MaTour,
                            t.TenTour,
                            SUM(dt.TongTien) AS TongDoanhThu
                        FROM dattour dt
                        JOIN tour t ON dt.MaTour = t.MaTour
                        GROUP BY t.MaTour, t.TenTour
                        ORDER BY TongDoanhThu DESC
                        LIMIT 5
                """)
            data = cursor.fetchall()
            
            # Đặt tiêu đề cho các cột
            headers = ["Mã NV", "Họ Tên", "Tổng Doanh Thu"]
            self.table_top_tours.setColumnCount(len(headers))
            self.table_top_tours.setHorizontalHeaderLabels(headers)
            
            self.table_top_tours.setRowCount(len(data))

            for row_idx, row_data in enumerate(data):
                for col_idx, col_data in enumerate(row_data):
                    self.table_top_tours.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi tải dữ liệu: {e}")
        finally:
            db.close()

    def load_staff(self):
        db = db_connect()
        cursor = db.cursor()
        try:
            cursor.execute("""
                           SELECT 
                            nv.MaNV,
                            nv.HoTen AS TenNhanVien,
                            SUM(dt.TongTien) AS TongDoanhThu
                        FROM dattour dt
                        JOIN nhanvien nv ON dt.MaNV = nv.MaNV
                        GROUP BY nv.MaNV, nv.HoTen
                        ORDER BY TongDoanhThu DESC
                        LIMIT 5
                """)
            data = cursor.fetchall()
            
            # Đặt tiêu đề cho các cột
            headers = ["Mã NV", "Họ Tên", "Tổng Doanh Thu"]
            self.table_top_staff.setColumnCount(len(headers))
            self.table_top_staff.setHorizontalHeaderLabels(headers)
            
            self.table_top_staff.setRowCount(len(data))

            for row_idx, row_data in enumerate(data):
                for col_idx, col_data in enumerate(row_data):
                    self.table_top_staff.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi tải dữ liệu: {e}")
        finally:
            db.close()


    def on_chart_type_changed(self):

        # Lấy loại biểu đồ được chọn
        chart_type = self.cmb_chart_type.currentText()

        # Gọi hàm vẽ biểu đồ tương ứng
        if chart_type == "Doanh thu theo tháng":
            self.load_chart_monthly()
        elif chart_type == "Doanh thu theo năm":
            self.load_chart_yearly()
        elif chart_type == "Doanh thu theo tour":
            self.load_chart_by_tour()
        elif chart_type == "Doanh thu theo nhân viên":
            self.load_chart_by_staff()

    def load_chart_monthly(self):
        # Kiểm tra nếu chart_container có layout, nếu không thì tạo mới
        layout = self.chart_container.layout()
        if layout is None:
            layout = QVBoxLayout()
            self.chart_container.setLayout(layout)

        # Xóa các widget cũ trong layout
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Kết nối đến MySQL
        try:
            db = db_connect()
            cursor = db.cursor()

            # Truy vấn lấy doanh thu theo tháng
            cursor.execute("""
                SELECT 
                    DATE_FORMAT(NgayDat, '%Y-%m') AS Thang,
                    SUM(TongTien) AS TongDoanhThu
                FROM dattour
                GROUP BY DATE_FORMAT(NgayDat, '%Y-%m')
                ORDER BY Thang;
            """)
            data = cursor.fetchall()

            # Kiểm tra có dữ liệu không
            if not data:
                QMessageBox.warning(self, "Cảnh báo", "Không có dữ liệu để hiển thị biểu đồ!")
                return

            # Tách dữ liệu thành danh sách tháng và doanh thu
            months = [row[0] for row in data]
            revenues = [row[1] for row in data]

            # Tạo biểu đồ
            figure = Figure()
            ax = figure.add_subplot(111)
            # ax.bar(months, revenues, color='blue')
            ax.plot(months, revenues, color='blue', marker='o')
            ax.set_title('Doanh Thu Theo Tháng')
            ax.set_xlabel('Tháng')
            ax.set_ylabel('Doanh Thu')

            canvas = FigureCanvas(figure)
            layout.addWidget(canvas)  # Thêm biểu đồ vào layout

        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi lấy dữ liệu từ MySQL: {e}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'db' in locals():
                db.close()

    def load_chart_yearly(self):
        # Kiểm tra nếu chart_container có layout, nếu không thì tạo mới
        layout = self.chart_container.layout()
        if layout is None:
            layout = QVBoxLayout()
            self.chart_container.setLayout(layout)

        # Xóa các widget cũ trong layout
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Kết nối đến MySQL
        try:
            db = db_connect()
            cursor = db.cursor()

            # Truy vấn lấy doanh thu theo năm
            cursor.execute("""
                SELECT 
                    DATE_FORMAT(NgayDat, '%Y') AS Nam,
                    SUM(TongTien) AS TongDoanhThu
                FROM dattour
                GROUP BY DATE_FORMAT(NgayDat, '%Y')
                ORDER BY Nam;
            """)
            data = cursor.fetchall()

            # Kiểm tra có dữ liệu không
            if not data:
                QMessageBox.warning(self, "Cảnh báo", "Không có dữ liệu để hiển thị biểu đồ!")
                return

            # Tách dữ liệu thành danh sách năm và doanh thu
            years = [row[0] for row in data]
            revenues = [row[1] for row in data]

            # Tạo biểu đồ
            figure = Figure()
            ax = figure.add_subplot(111)
            # ax.bar(years, revenues, color='green')
            ax.plot(years, revenues, color='red', marker='o')
            ax.set_title('Doanh Thu Theo Năm')
            ax.set_xlabel('Năm')
            ax.set_ylabel('Doanh Thu')

            canvas = FigureCanvas(figure)
            layout.addWidget(canvas)  # Thêm biểu đồ vào layout

        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi lấy dữ liệu từ MySQL: {e}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'db' in locals():
                db.close()
