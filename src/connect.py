import MySQLdb as mdb

def db_connect():
    try:
        conn = mdb.connect('localhost', 'root', '', 'quan_ly_tour_2')
        return conn
    except:
        print("Lỗi kết nối đến database")