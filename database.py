import sqlite3

# Kết nối tới cơ sở dữ liệu SQLite
conn = sqlite3.connect('thong_tin_ca_nhan.db')
cursor = conn.cursor()

# Tạo bảng
cursor.execute('''CREATE TABLE thong_tin_ca_nhan (
                    id INTEGER PRIMARY KEY,
                    ho_ten TEXT,
                    ngay_thang_nam_sinh DATE,
                    gioi_tinh TEXT,
                    so_cccd TEXT,
                    dan_toc TEXT,
                    ton_giao TEXT,
                    quoc_tich TEXT,
                    tinh_trang_hon_nhan TEXT,
                    nhom_mau TEXT,
                    noi_dang_ki_khai_sinh TEXT,
                    que_quan TEXT,
                    noi_thuong_tru TEXT,
                    noi_o_hien_tai TEXT,
                    nghe_nghiep TEXT,
                    trinh_do_hoc_van TEXT,
                    so_dien_thoai TEXT
                )''')

# Lưu thay đổi và đóng kết nối
conn.commit()
conn.close()
