import sqlite3

# --------------- Tạo Database -------------------
def create_database(list_tag_names):
    conn = sqlite3.connect('data.db') # Tạo data.db nếu nó chưa tồn tại
    cursor = conn.cursor() # Tạo cursor để thực thi các lệnh SQL
    # Tạo bảng với các cột dựa trên tag name
    create_table_query = f"CREATE TABLE IF NOT EXISTS data ({', '.join([f'{tag} TEXT' for tag in list_tag_names])})"
    cursor.execute(create_table_query)
    conn.commit() # Xác nhận thay đổi
    conn.close() # Đóng kết nối

# ------------------- Đếm số dòng trong database ------------------
def count_rows():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    query = "SELECT COUNT(*) FROM data;"
    cursor.execute(query)
    count = cursor.fetchone()[0]
    conn.close()
    return count


# ---------------- Thêm thông tin vào datase -----------------------------
def insert_value_into_database(value, data_to_insert):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    data_to_insert['ID'] = value
    columns = ', '.join(data_to_insert.keys())
    placeholders = ', '.join(['?' for _ in range(len(data_to_insert))])
    sql_query = f"INSERT INTO data ({columns}) VALUES ({placeholders})"
    values = [data_to_insert[key] for key in data_to_insert]
    cursor.execute(sql_query, values)
    conn.commit()
    conn.close()

# --------------- Cập nhật thông tin vào database -------------------------
def update_value_in_database(value, data_to_update):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    set_clause = ', '.join([f"{key} = ?" for key in data_to_update.keys()])
    sql_query = f"UPDATE data SET {set_clause} WHERE ID = ?"
    values = list(data_to_update.values())
    values.append(value)
    cursor.execute(sql_query, values)
    conn.commit()
    conn.close()

# ------------------- Lấy thông tin tại 1 ô từ database ----------------------------
def get_value(id, key):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    sql_query = f'SELECT {key} FROM data WHERE ID = ?'
    cursor.execute(sql_query, (id,))
    value = cursor.fetchone()[0]
    conn.close()
    return value
    