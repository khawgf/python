
import sqlite3


class sp_dal:
    def get_dssp(self):
        conn = sqlite3.connect('doanpython.db')
        cursor = conn.cursor()
        query = "SELECT PRODUCTNAME,DESCRIPTION,PRICE,CATEGORY,BAOHANH FROM PRODUCTS"
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()
        return result

    def get_dssp_catogory(self, category):
        conn = sqlite3.connect('doanpython.db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT PRODUCTNAME, DESCRIPTION, PRICE, CATEGORY, BAOHANH FROM PRODUCTS WHERE CATEGORY=?", (category,))
        result = cursor.fetchall()
        conn.close()
        return result

    def thongso_sp(self, text):
        conn = sqlite3.connect('doanpython.db')
        cursor = conn.cursor()
        new_text=text[0].upper() + text[1:].lower()
        query = "SELECT PRODUCTID FROM PRODUCTS WHERE LOWER(PRODUCTNAME) LIKE ?"
        cursor.execute(query, ('%' +new_text+ '%',))
        print(new_text)
        result = cursor.fetchone()
        if result is not None:
            product_id = result[0]
            query = "SELECT THONGSO FROM PRODUCTS WHERE PRODUCTID = ?"
            cursor.execute(query, (product_id,))
            product_info = cursor.fetchone()[0]
            conn.close()
            return product_info
        else:
            conn.close()
            return None

    def getid_prd(self,text):
        conn = sqlite3.connect('doanpython.db')
        cursor = conn.cursor()
        new_text=text[0].upper() + text[1:].lower()
        query = "SELECT PRODUCTID FROM PRODUCTS WHERE LOWER(PRODUCTNAME) LIKE ?"
        cursor.execute(query, ('%' +new_text+ '%',))
        result1 = cursor.fetchone()
        if result1 is not None:
            result = result1[0]
            conn.close()
            return result
        else:
            conn.close()
            return None
    
    def insert_suco(self, suco):
            conn = sqlite3.connect('doanpython.db')
            c = conn.cursor()
            # tăng id
            c.execute('SELECT MAX(IDSUCO) FROM SUCO')
            last_id = c.fetchone()[0] or 0
            # tăng giá trị ID và thêm bản ghi mới vào bảng Customer
            new_id = last_id + 1
            data = (new_id, suco.USERID, suco.PRODUCTID, suco.NGAYPHATHIEN, suco.MOTASUCO)
            placeholders = ', '.join(['?'] * len(data))
            query = f"INSERT INTO SUCO VALUES ({placeholders})"
            c.execute(query, data)
            conn.commit()
            conn.close()

    def insert_phanhoi(self, reviews):
            conn = sqlite3.connect('doanpython.db')
            c = conn.cursor()
            # tăng id
            c.execute('SELECT MAX(REVIEWID) FROM REVIEWS')
            last_id = c.fetchone()[0] or 0
            # tăng giá trị ID và thêm bản ghi mới vào bảng Customer
            new_id = last_id + 1
            data = (new_id, reviews.USERID, reviews.PRODUCTID, reviews.RATING, reviews.COMMENT)
            placeholders = ', '.join(['?'] * len(data))
            query = f"INSERT INTO REVIEWS VALUES ({placeholders})"
            c.execute(query, data)
            conn.commit()
            conn.close()

    def insert_datlich(self, datlich):
            conn = sqlite3.connect('doanpython.db')
            c = conn.cursor()
            # tăng id
            c.execute('SELECT MAX(IDDATLICH) FROM DATLICH')
            last_id = c.fetchone()[0] or 0
            # tăng giá trị ID và thêm bản ghi mới vào bảng Customer
            new_id = last_id + 1
            data = (new_id, datlich.IDKHACHHANG, datlich.NGAYHEN, datlich.THOIGIAN, datlich.NOIDUNG)
            placeholders = ', '.join(['?'] * len(data))
            query = f"INSERT INTO DATLICH VALUES ({placeholders})"
            c.execute(query, data)
            conn.commit()
            conn.close()

    