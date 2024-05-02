class LoginWidget:
    def __init__(self):
        self.username = ""
    
    def get_username(self):
        return self.username
        
    def set_username(self, username):
        self.username = username




class MyWidget:
    def __init__(self):
        self.login_widget = LoginWidget()
    
    def do_something(self):
        # Lấy giá trị username từ LoginWidget
        username = self.login_widget.get_username()
        
        # Gán giá trị username cho LoginWidget
        self.login_widget.set_username("new_username")

    def getdata_noidungsuco(self):
            self.conn = sqlite3.connect('doanpython.db')
            c = self.conn.cursor()
            # tăng id
            c.execute('SELECT MAX(MOTASUCO) FROM SUCO')
            result = c.fetchone()
            self.conn.close()
            if result:
                return result[0]
            else:
                return None
            
    
vanban="""Công ty chúng tôi là một trong những công ty hàng đầu trong lĩnh vực bán các loại sản phẩm điện tử. Chúng tôi cam kết cung cấp cho khách hàng những sản phẩm chất lượng, đa dạng về mẫu mã, chủng loại và giá cả phải chăng.

Chúng tôi luôn tập trung vào việc đáp ứng nhu cầu và mong muốn của khách hàng bằng cách cung cấp những sản phẩm điện tử chất lượng cao, đáp ứng các tiêu chuẩn kỹ thuật hiện đại nhất và được cập nhật liên tục theo xu hướng công nghệ mới nhất.

Ngoài ra, chúng tôi còn có đội ngũ nhân viên tư vấn chuyên nghiệp và nhiệt tình, luôn sẵn sàng giúp đỡ khách hàng trong quá trình lựa chọn sản phẩm, giải đáp thắc mắc, hỗ trợ khách hàng khi có sự cố xảy ra.

Chúng tôi luôn đặt khách hàng làm trung tâm trong mọi hoạt động của công ty, và cam kết mang đến cho khách hàng sự hài lòng tuyệt đối với các sản phẩm và dịch vụ của chúng tôi. Chúng tôi hy vọng sẽ được đồng hành cùng khách hàng trong hành trình khám phá và trải nghiệm công nghệ tuyệt vời của thế giới điện tử."""
import speech_recognition as sr
import pyttsx3
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QRect
from PyQt5.QtCore import QTimer
import time
from gtts import gTTS
import os
import playsound
import sys
import sqlite3


def thongso_sp(text="loa di động"):
    conn = sqlite3.connect('doanpython.db')
    cursor = conn.cursor()
    query = "SELECT PRODUCTID FROM PRODUCTS WHERE PRODUCTNAME like ?"
    cursor.execute(query,('%' + text + '%',))
    result = cursor.fetchone()
    if result is not None:
        product_id = result[0]
        query = "SELECT DESCRIPTION FROM PRODUCTS WHERE PRODUCTID = ?"
        cursor.execute(query, (product_id,))
        product_info = cursor.fetchone()[0]
        conn.close()
        return product_info
    else:
        conn.close()
        return None
def thongs_sp(text='loa di'):
        conn = sqlite3.connect('doanpython.db')
        cursor = conn.cursor()
        query = "SELECT PRODUCTID FROM PRODUCTS WHERE PRODUCTNAME like ?"
        cursor.execute(query, ('%' + text + '%',))
        result1 = cursor.fetchone()
        if result1 is not None:
            result=result1[0]
            conn.close()
            return result
        else:
            conn.close()
            return None
def getid_prd(text='samsung s21'):
        conn = sqlite3.connect('doanpython.db')
        cursor = conn.cursor()
        query = "SELECT PRODUCTID FROM PRODUCTS WHERE PRODUCTNAME like ?"
        cursor.execute(query, ('%' + text + '%',))
        result1 = cursor.fetchone()
        if result1 is not None:
            result = result1[0]
            conn.close()
            return result
        else:
            conn.close()
            return None
def get_id_user():
        username = 'admin'
        conn = sqlite3.connect('doanpython.db')
        c = conn.cursor()
        c.execute("SELECT USERID FROM USERS WHERE USERNAME=?", (username,))
        result = c.fetchone()
        conn.close()
        if result:
            return result[0]
        else:
            return None

    
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


import re

def is_valid_time(time_str="7:00"):
    numbers = re.findall(r'\d+', time_str)
    if len(numbers) > 0:
        hour = int(numbers[0])
        if len(numbers) > 1:
            minute = int(numbers[1])
        else:
            minute = 0
        if hour < 7 or hour > 17 or minute < 0 or minute > 59:
            return False
        else:
            return True
    else:
        return False



def thongso_sp(text):
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
    

def getid_prd(text='điện thoại Xiaomi Mi 11'):
        conn = sqlite3.connect('doanpython.db')
        cursor = conn.cursor()
        query = "SELECT PRODUCTID FROM PRODUCTS WHERE PRODUCTNAME like ?"
        cursor.execute(query, ('%' + text + '%',))
        result1 = cursor.fetchone()
        if result1 is not None:
            result = result1[0]
            conn.close()
            return result
        else:
            conn.close()
            return None
import speech_recognition as sr
import pyttsx3
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QRect
from PyQt5.QtCore import QTimer
import time
from gtts import gTTS
import os
import playsound
import sys
import sqlite3
import sanphamdal
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re
from datetime import datetime, timedelta

def is_valid_date(day_prd='ngày 01 tháng 04 năm 2023'):
        numbers = re.findall(r'\d+', day_prd)
        if len(numbers) == 3:
            day, month, year = map(int, numbers)
            tomorrow = datetime.now().date() + timedelta(days=1)
            
            if month == 2 and day > 29:
                return False
            elif month in [4, 6, 9, 11] and day > 30:
                return False
            elif month in [1, 3, 5, 7, 8, 10, 12] and day > 31:
                return False
            elif day < datetime.now().day :
                return False
            elif month < datetime.now().month or month > datetime.now().month:
                return False
            elif year < datetime.now().year or year > datetime.now().year:
                return False
            else:
                return True
        else:
            return False






def is_valid_score(day_prd=' diem'):
    numbers = re.findall(r'\d+', day_prd)
    if len(numbers) == 1:
        score = int(numbers[0])
        if 0 <= score <= 10:
            return True
        else:
            return False
    else:
        return False
        
print(is_valid_score())