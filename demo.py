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


class SUCO:
    def __init__(self, USERID=None, PRODUCTID=None, NGAYPHATHIEN=None, MOCASUCO=None):
        self.USERID = USERID
        self.PRODUCTID = PRODUCTID
        self.NGAYPHATHIEN = NGAYPHATHIEN
        self.MOTASUCO = MOCASUCO


class DATLICH:
    def __init__(self, IDKHACHHANG=None, NGAYHEN=None, THOIGIAN=None, NOIDUNG=None):
        self.IDKHACHHANG = IDKHACHHANG
        self.NGAYHEN = NGAYHEN
        self.THOIGIAN = THOIGIAN
        self.NOIDUNG = NOIDUNG


class REVIEWS:
    def __init__(self, USERID=None, PRODUCTID=None,  RATING=None, COMMENT=None):
        self.USERID = USERID
        self.PRODUCTID = PRODUCTID
        self.RATING = RATING
        self.COMMMENT = COMMENT


class MyWidget(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        from demologin import LoginWindow
        self.login_window = LoginWindow()
        self.stop_flag = False
        self.timers = []
        self.recognizer = sr.Recognizer()
        self.setWindowTitle('Chăm Sóc Khách Hàng')
        self.setGeometry(200, 200, 800, 600)
        # Tạo QTextEdit để hiển thị nội dung chat
        self.chat_display = QTextEdit(self)
        self.chat_display.setReadOnly(True)
        self.chat_display.ensureCursorVisible()
        self.chat_display.append('<div style="display: flex; justify-content: center; align-items: center;"><div style="text-align: center; margin-top: 100px;"><b><span style="font-size:20px">ĐÂY LÀ ỨNG DỤNG CHĂM SÓC KHÁCH HÀNG BẰNG GIỌNG NÓI CỦA BÊN CÔNG TY MÌNH</span></b></div><div style="margin: auto;"><img src="anh1.webp" alt="Your Image" /></div><div style="text-align: center;"><b> Nhấn "START"để bắt đầu<b></div></div>')

        # Tạo QPushButton để kích hoạt sự kiện gửi nội dung chat- end
        self.start_button = QPushButton('START', self)
        self.start_button.clicked.connect(self.send_message)
        self.end_button = QPushButton('END', self)
        self.end_button.clicked.connect(self.stop)
        self.logout_button = QPushButton('LOG OUT', self)
        self.logout_button.clicked.connect(self.logout)
        # Tạo QHBoxLayout để quản lý chat_input và send_button
        self.chat_input_layout = QHBoxLayout()
        self.chat_input_layout.addWidget(self.start_button)
        self.chat_input_layout.addWidget(self.end_button)
        self.chat_input_layout.addWidget(self.logout_button)
        self.logout_button.setFixedSize(100, 30)

        self.end_button.setEnabled(False)

        # Tạo QVBoxLayout để quản lý các widget
        vbox = QVBoxLayout()
        vbox.addWidget(self.chat_display)
        vbox.addLayout(self.chat_input_layout)
        # Thiết lập layout cho QWidget
        self.setLayout(vbox)
    spdal = sanphamdal.sp_dal()
###########################################################################

    def get_full_name(self):
        username = self.username
        self.conn = sqlite3.connect('doanpython.db')
        c = self.conn.cursor()
        c.execute("SELECT FULLNAME FROM USERS WHERE USERNAME=?", (username,))
        result = c.fetchone()
        self.conn.close()
        if result:
            return result[0]
        else:
            return None

    def get_email(self):
        username = self.username
        self.conn = sqlite3.connect('doanpython.db')
        c = self.conn.cursor()
        c.execute("SELECT EMAIL FROM USERS WHERE USERNAME=?", (username,))
        result = c.fetchone()
        self.conn.close()
        if result:
            print(result[0])
            return result[0]
        else:
            return None

    def get_email_ngayhen(self):
        id_user = self.get_id_user()
        self.conn = sqlite3.connect('doanpython.db')
        c = self.conn.cursor()
        c.execute(f"SELECT NGAYHEN FROM DATLICH WHERE IDKHACHHANG=? AND IDDATLICH = (SELECT MAX(IDDATLICH) FROM DATLICH WHERE IDKHACHHANG=?)", (id_user, id_user))
        result = c.fetchone()
        self.conn.close()
        if result:
            print(result[0])
            return result[0]
        else:
            return None

    def get_email_thoigian(self):
        id_user = self.get_id_user()
        self.conn = sqlite3.connect('doanpython.db')
        c = self.conn.cursor()
        c.execute(f"SELECT THOIGIAN FROM DATLICH WHERE IDKHACHHANG=? AND IDDATLICH = (SELECT MAX(IDDATLICH) FROM DATLICH WHERE IDKHACHHANG=?)", (id_user, id_user))
        result = c.fetchone()
        self.conn.close()
        if result:
            print(result[0])
            return result[0]
        else:
            return None

    def get_email_noidung(self):
        id_user = self.get_id_user()
        self.conn = sqlite3.connect('doanpython.db')
        c = self.conn.cursor()
        c.execute(f"SELECT NOIDUNG FROM DATLICH WHERE IDKHACHHANG=? AND IDDATLICH = (SELECT MAX(IDDATLICH) FROM DATLICH WHERE IDKHACHHANG=?)", (id_user, id_user))
        result = c.fetchone()
        self.conn.close()
        if result:
            print(result[0])
            return result[0]
        else:
            return None

    def get_email_ngaygapsuco(self):
        id_user = self.get_id_user()
        self.conn = sqlite3.connect('doanpython.db')
        c = self.conn.cursor()
        c.execute(f"SELECT NGAYPHATHIEN FROM SUCO WHERE USERID=? AND IDSUCO = (SELECT MAX(IDSUCO) FROM SUCO WHERE USERID=?)", (id_user, id_user))
        result = c.fetchone()
        self.conn.close()
        if result:
            print(result[0])
            return result[0]
        else:
            return None

    def get_email_noidungsuco(self):
        id_user = self.get_id_user()
        self.conn = sqlite3.connect('doanpython.db')
        c = self.conn.cursor()
        c.execute(f"SELECT MOTASUCO FROM SUCO WHERE USERID=? AND IDSUCO = (SELECT MAX(IDSUCO) FROM SUCO WHERE USERID=?)", (id_user, id_user))
        result = c.fetchone()
        self.conn.close()
        if result:
            print(result[0])
            return result[0]
        else:
            return None

    def get_id_user(self):
        username = self.username
        self.conn = sqlite3.connect('doanpython.db')
        c = self.conn.cursor()
        c.execute("SELECT USERID FROM USERS WHERE USERNAME=? ", (username,))
        result = c.fetchone()
        self.conn.close()
        if result:
            return result[0]
        else:
            return None

    def get_name_product(self):
        id_user = self.get_id_user()
        self.conn = sqlite3.connect('doanpython.db')
        c = self.conn.cursor()
        c.execute("SELECT p.PRODUCTNAME FROM SUCO s INNER JOIN PRODUCTS p ON s.PRODUCTID = p.PRODUCTID WHERE s.USERID = ? AND s.IDSUCO = (SELECT MAX(IDSUCO) FROM SUCO WHERE USERID = ?)", (id_user, id_user))
        result = c.fetchone()
        self.conn.close()
        if result:
            return result[0]
        else:
            return None

    def checkproduct(self, id):
        id_user = self.get_id_user()
        self.conn = sqlite3.connect('doanpython.db')
        c = self.conn.cursor()
        c.execute(
            "SELECT * FROM BANHANG WHERE PRODUCTID=? AND USERID=?", (id, id_user))
        result = c.fetchone()
        self.conn.close()
        if result:
            return True
        else:
            return False
#######################################################################

    def bot_speak(self, text):
        if not self.stop_flag:
            self.chat_display.setAcceptRichText(True)
            self.chat_display.append(f'<b>Bot:</b>{text}')
            self.chat_display.append('')
            # text_clear = text.replace('<br>', '')
            text_clear = text.replace('<br>', '').replace('<div>', '').replace(
                '</div>', '').replace('<p>', '').replace('</p>', '')
            self.process_message(text_clear)

    def get_voice(self):
        if not self.stop_flag:
            with sr.Microphone() as source:
                self.chat_display.append('<b>Bot:</b> (Đang lắng nghe...)')
                self.chat_display.append('')
                audio = self.recognizer.listen(source, phrase_time_limit=5)
                try:
                    text = self.recognizer.recognize_google(
                        audio, language="vi-VN")
                    self.chat_display.append(f'<b>Bạn:</b> {text}')
                    self.chat_display.append('')
                    return text.lower()
                except sr.UnknownValueError:
                    self.chat_display.append(
                        '<b>Bạn:</b> (Không thể nhận dữ liệu giọng nói)')
                    self.chat_display.append('')
                    return None
                except sr.RequestError as e:
                    self.chat_display.append(
                        '<b>Bạn:</b> (Không thể kết nối tới Google Speech Recognition service)')
                    self.chat_display.append('')
                    return ''

    def process_message(self, message):
        if not self.stop_flag:
            # truyen vao text de doc len
            tts = gTTS(text=message, lang='vi', slow=False)
            tts.save("sound.mp3")
            playsound.playsound("sound.mp3", False)
            os.remove("sound.mp3")
            return message

    def stop(self):
        self.bot_speak('Hẹn gặp lại bạn nhé')
        self.stop_flag = True
        self.add_single_shot_timer(5000,lambda:self.start_button.setEnabled(True))
        self.add_single_shot_timer(5000,lambda:self.logout_button.setEnabled(True))
        self.end_button.setEnabled(False)

    def logout(self):
        self.login_window.show()
        self.close()

    def export_table(self, result):
        html = "<table style='border-collapse: collapse; border: 1px solid black;'>\n"
        html += "<tr style='border: 1px solid black;'><th style='border: 1px solid black;'>Product name</th><th style='border: 1px solid black;'>Description</th><th style='border: 1px solid black;'>Price</th><th style='border: 1px solid black;'>Category</th><th style='border: 1px solid black;'>Bao hanh</th></tr>\n"
        for row in result:
            html += "<tr style='border: 1px solid black;'>"
            for col in row:
                html += f"<td style='border: 1px solid black; text-align: center;'>{col}</td>"
            html += "</tr>\n"
        html += "</table>"
        return html
###############################################################################

    def hotro_cactuvan(self):
        self.add_single_shot_timer(0, lambda: self.bot_speak(
            'Mời bạn lựa chọn hỗ trợ để mình giúp đỡ '))
        self.add_single_shot_timer(5000, self.hotro_cactuvan1)

    def hotro_cactuvan1(self):
        texthotro_cactuvan = self.get_voice()
        if texthotro_cactuvan is None:
            self.add_single_shot_timer(0, lambda: self.bot_speak(
                'Xin mời bạn nói lại mình không nghe rõ'))
            self.add_single_shot_timer(5000, self.hotro_cactuvan1)
        elif 'sản phẩm' in texthotro_cactuvan:
            self.add_single_shot_timer(0, lambda: self.bot_speak(
                'Đây là danh sách sản phẩm bên mình'))
            data = self.spdal.get_dssp()  # Lấy dữ liệu từ CSDL
            html = self.export_table(data)  # Tạo bảng HTML
            # Thêm bảng HTML vào chat_display
            self.add_single_shot_timer(
                10000, lambda: self.chat_display.append(html))

            self.add_single_shot_timer(30000, lambda: self.bot_speak(
                'Bạn có muốn xem theo từng loại không'))

            self.add_single_shot_timer(35000, self.hotro_cactuvan1_1_sp)

        elif 'giới thiệu' in texthotro_cactuvan or 'thông tin' in texthotro_cactuvan:
            self.add_single_shot_timer(0, self.hotro_thongtin)

        elif 'sự cố' in texthotro_cactuvan or 'khắc phục' in texthotro_cactuvan:
            self.add_single_shot_timer(0, self.hotro_suco)

        elif 'phản hồi' in texthotro_cactuvan:
            self.add_single_shot_timer(0, self.hotro_phanhoi)
        else:
            self.add_single_shot_timer(0, lambda: self.bot_speak(
                'Xin bạn nhắc lại ạ'))

    def hotro_cactuvan1_1_sp(self):
        text = self.get_voice()
        if text is None:
            self.add_single_shot_timer(0, lambda: self.bot_speak(
                'có hay không ạ'))
            self.add_single_shot_timer(5000, self.hotro_cactuvan1_1_sp)
        elif 'có' in text:
            self.add_single_shot_timer(0, self.hotro_cactuvan2_sp)
        elif 'không' in text:
            self.add_single_shot_timer(0, self.hotro_cactuvan5_sp)
        else:
            self.add_single_shot_timer(0, lambda: self.bot_speak(
                'Xin bạn nhắc lại là có hay không ạ'))

    def hotro_cactuvan2_sp(self):
        self.add_single_shot_timer(0, lambda: self.bot_speak(
            'Bạn muốn xem loại sản phẩm cụ thể là loại nào ạ'))
        self.add_single_shot_timer(5000, self.hotro_cactuvan3_sp)

    def hotro_cactuvan3_sp(self):
        text_dssp_category1 = self.get_voice()
        if text_dssp_category1 is None:
            self.add_single_shot_timer(0, lambda: self.bot_speak(
                'Xin lỗi, tôi không nghe rõ. Bạn có thể nói lại được không?'))
            # Cho chương trình nghe lại sau 5 giây
            self.add_single_shot_timer(5000, self.hotro_cactuvan3_sp)
        if text_dssp_category1 is not None:
            self.add_single_shot_timer(
                0, lambda: self.hotro_cactuvan4_sp(text_dssp_category1))

    def hotro_cactuvan4_sp(self, text_dssp_category1):
        if 'điện thoại' in text_dssp_category1 or 'thông minh' in text_dssp_category1:
            text_dssp_category2 = 'Điện thoại thông minh'
            data = self.spdal.get_dssp_catogory(
                text_dssp_category2)  # Lấy dữ liệu từ CSDL
            html = self.export_table(data)  # Tạo bảng HTML
            # Thêm bảng HTML vào chat_display
            self.add_single_shot_timer(3000, lambda: self.bot_speak(
                f'Đây là sản phẩm loại {text_dssp_category2}'))
            self.add_single_shot_timer(
                5000, lambda: self.chat_display.append(html))
            self.add_single_shot_timer(15000, self.hotro_cactuvan5_sp)
        elif 'laptop' in text_dssp_category1 or 'loptop' in text_dssp_category1:
            text_dssp_category2 = 'Laptop'
            data = self.spdal.get_dssp_catogory(
                text_dssp_category2)  # Lấy dữ liệu từ CSDL
            html = self.export_table(data)  # Tạo bảng HTML
            # Thêm bảng HTML vào chat_display
            self.add_single_shot_timer(3000, lambda: self.bot_speak(
                f'Đây là sản phẩm loại {text_dssp_category2}'))
            self.add_single_shot_timer(
                5000, lambda: self.chat_display.append(html))
            self.add_single_shot_timer(15000, self.hotro_cactuvan5_sp)
        elif 'máy ảnh' in text_dssp_category1 or 'chuyên nghiệp' in text_dssp_category1:
            text_dssp_category2 = 'Máy ảnh chuyên nghiệp'
            data = self.spdal.get_dssp_catogory(
                text_dssp_category2)  # Lấy dữ liệu từ CSDL
            html = self.export_table(data)  # Tạo bảng HTML
            # Thêm bảng HTML vào chat_display
            self.add_single_shot_timer(3000, lambda: self.bot_speak(
                f'Đây là sản phẩm loại {text_dssp_category2}'))
            self.add_single_shot_timer(
                5000, lambda: self.chat_display.append(html))
            self.add_single_shot_timer(15000, self.hotro_cactuvan5_sp)
        elif 'tivi' in text_dssp_category1 or 'tidi' in text_dssp_category1:
            text_dssp_category2 = 'Tivi'
            data = self.spdal.get_dssp_catogory(
                text_dssp_category2)  # Lấy dữ liệu từ CSDL
            html = self.export_table(data)  # Tạo bảng HTML
            # Thêm bảng HTML vào chat_display
            self.add_single_shot_timer(3000, lambda: self.bot_speak(
                f'Đây là sản phẩm loại {text_dssp_category2}'))
            self.add_single_shot_timer(
                5000, lambda: self.chat_display.append(html))
            self.add_single_shot_timer(15000, self.hotro_cactuvan5_sp)
        elif 'loa không dây' in text_dssp_category1:
            text_dssp_category2 = 'Loa không dây'
            data = self.spdal.get_dssp_catogory(
                text_dssp_category2)  # Lấy dữ liệu từ CSDL
            html = self.export_table(data)  # Tạo bảng HTML
            # Thêm bảng HTML vào chat_display
            self.add_single_shot_timer(3000, lambda: self.bot_speak(
                f'Đây là sản phẩm loại {text_dssp_category2}'))
            self.add_single_shot_timer(
                5000, lambda: self.chat_display.append(html))
            self.add_single_shot_timer(15000, self.hotro_cactuvan5_sp)
        elif 'máy tính' in text_dssp_category1 or 'máy tính bảng' in text_dssp_category1:
            text_dssp_category2 = 'Máy tính bảng'
            data = self.spdal.get_dssp_catogory(
                text_dssp_category2)  # Lấy dữ liệu từ CSDL
            html = self.export_table(data)  # Tạo bảng HTML
            # Thêm bảng HTML vào chat_display
            self.add_single_shot_timer(3000, lambda: self.bot_speak(
                f'Đây là sản phẩm loại {text_dssp_category2}'))
            self.add_single_shot_timer(
                5000, lambda: self.chat_display.append(html))
            self.add_single_shot_timer(15000, self.hotro_cactuvan5_sp)
        elif 'tai nghe true' in text_dssp_category1 or 'true wireless' in text_dssp_category1:
            text_dssp_category2 = 'Tai nghe true wireless'
            data = self.spdal.get_dssp_catogory(
                text_dssp_category2)  # Lấy dữ liệu từ CSDL
            html = self.export_table(data)  # Tạo bảng HTML
            # Thêm bảng HTML vào chat_display
            self.add_single_shot_timer(3000, lambda: self.bot_speak(
                f'Đây là sản phẩm loại {text_dssp_category2}'))
            self.add_single_shot_timer(
                5000, lambda: self.chat_display.append(html))
            self.add_single_shot_timer(15000, self.hotro_cactuvan5_sp)
        elif 'tai nghe không dây' in text_dssp_category1:
            text_dssp_category2 = 'Tai nghe không dây'
            data = self.spdal.get_dssp_catogory(
                text_dssp_category2)  # Lấy dữ liệu từ CSDL
            html = self.export_table(data)  # Tạo bảng HTML
            # Thêm bảng HTML vào chat_display
            self.add_single_shot_timer(3000, lambda: self.bot_speak(
                f'Đây là sản phẩm loại {text_dssp_category2}'))
            self.add_single_shot_timer(
                5000, lambda: self.chat_display.append(html))
            self.add_single_shot_timer(15000, self.hotro_cactuvan5_sp)
        elif 'loa di động' in text_dssp_category1:
            text_dssp_category2 = 'Loa di động'
            data = self.spdal.get_dssp_catogory(
                text_dssp_category2)  # Lấy dữ liệu từ CSDL
            html = self.export_table(data)  # Tạo bảng HTML
            # Thêm bảng HTML vào chat_display
            self.add_single_shot_timer(3000, lambda: self.bot_speak(
                f'Đây là sản phẩm loại {text_dssp_category2}'))
            self.add_single_shot_timer(
                5000, lambda: self.chat_display.append(html))
            self.add_single_shot_timer(15000, self.hotro_cactuvan5_sp)
        else:
            self.add_single_shot_timer(0, lambda: self.bot_speak(
                'Không có sản phẩm nào như vậy'))
            self.add_single_shot_timer(5000, lambda: self.bot_speak(
                'Bạn hãy nhắc lại giúp mình'))
            self.add_single_shot_timer(10000, self.hotro_cactuvan3_sp)

    def hotro_cactuvan5_sp(self):
        self.add_single_shot_timer(0, lambda: self.bot_speak(
            'Bạn muốn biết thông tin về sản phẩm nào bên mình ạ, ngoài những thông tin trên?'))
        self.add_single_shot_timer(7000, self.hotro_cactuvan6_sp)

    def hotro_cactuvan6_sp(self):
        text = self.get_voice()
        if text is not None:
            thongso = self.spdal.thongso_sp(text)
            if thongso is None:
                self.add_single_shot_timer(0, lambda: self.bot_speak(
                    'xin hãy nhắc lại đúng tên sản phẩm'))
                self.add_single_shot_timer(5000, self.hotro_cactuvan6_sp)
            elif thongso is not None:
                self.add_single_shot_timer(0, lambda: self.bot_speak(
                    f'Dưới đây là chi tiết thông số sản phẩm {text}'))
                self.add_single_shot_timer(
                    5000, lambda: self.chat_display.append(f'{thongso}'))
                self.add_single_shot_timer(15000, lambda: self.bot_speak(
                    '''Bạn muốn tiếp tục hỏi về sản phẩm khác?<br>
                Hoặc là hãy nói 'trở về' để quay lại giao diện hỗ trợ chính  '''))
                self.add_single_shot_timer(25000, self.hotro_cactuvan7_sp)
        elif text is None:
            self.add_single_shot_timer(0, lambda: self.bot_speak(
                'Không nghe rõ, xin hãy nhắc lại tên sản phẩm'))
            self.add_single_shot_timer(5000, self.hotro_cactuvan6_sp)

    def hotro_cactuvan7_sp(self):
        text = self.get_voice()
        if text is None:
            self.add_single_shot_timer(0, lambda: self.bot_speak(
                'Không nghe rõ, xin hãy nhắc lại ý của bạn'))
            self.add_single_shot_timer(5000, self.hotro_cactuvan7_sp)
        elif 'tiếp tục' in text or 'có' in text:
            self.add_single_shot_timer(0, self.hotro_cactuvan5_sp)
        elif 'không' in text or 'trở về' in text:
            self.add_single_shot_timer(0, lambda: self.bot_speak("""Dưới đây là những việc mình có thể hỗ trợ bạn hiện giờ<br>
            - Hỏi về sản phẩm<br>
            - Thông tin về Công Ty ABC<br>
            - Sản phẩm gặp sự cố <br>
            - Phản hồi về sản phẩm của bên mình
            """))
            self.add_single_shot_timer(20000, self.hotro_cactuvan)
        else:
            self.add_single_shot_timer(0, lambda: self.bot_speak(
                'Xin bạn nhắc lại là có hay không ạ'))


# _thong tin cong ty

    def hotro_thongtin(self):
        self.add_single_shot_timer(5000, lambda: self.bot_speak(
            '''Bạn cần hỗ trợ gì về thông tin công ty<br>
            -Giới thiệu<br>
            -Thông tin liên hệ'''))
        self.add_single_shot_timer(20000, self.hotro_thongtin0_5)
# _thong tin cong ty

    def hotro_thongtin0_5(self):
        text = self.get_voice()
        if text is None:
            self.add_single_shot_timer(
                0, lambda: self.bot_speak('Xin hãy nhắc lại'))
            self.add_single_shot_timer(10000, self.hotro_thongtin0_5)
        elif 'giới thiệu' in text:
            self.add_single_shot_timer(0, lambda: self.bot_speak(
                """<div>
  <p>GIỚI THIỆU</p>
  <p>Công ty chúng tôi là một trong những công ty hàng đầu trong lĩnh vực bán các loại sản phẩm điện tử.</p>
  <p>Chúng tôi cam kết cung cấp cho khách hàng những sản phẩm chất lượng, đa dạng về mẫu mã, chủng loại và giá cả phải chăng.</p>
  <p>Chúng tôi luôn tập trung vào việc đáp ứng nhu cầu và mong muốn của khách hàng bằng cách cung cấp những sản phẩm điện tử chất lượng cao, đáp ứng các tiêu chuẩn kỹ thuật hiện đại nhất và được cập nhật liên tục theo xu hướng công nghệ mới nhất.</p>
  <p>Ngoài ra, chúng tôi còn có đội ngũ nhân viên tư vấn chuyên nghiệp và nhiệt tình, luôn sẵn sàng giúp đỡ khách hàng trong quá trình lựa chọn sản phẩm, giải đáp thắc mắc, hỗ trợ khách hàng khi có sự cố xảy ra.</p>
  <p>Chúng tôi hy vọng sẽ được đồng hành cùng khách hàng trong hành trình khám phá và trải nghiệm công nghệ tuyệt vời của thế giới điện tử.</p>
</div>"""))
            self.add_single_shot_timer(70000, lambda: self.bot_speak(
                'Bạn có muốn xem thông tin khác không'))
            self.add_single_shot_timer(75000, self.hotro_thongtin1)

        elif 'thông tin' in text or 'liên lạc' in text:
            self.add_single_shot_timer(0, lambda: self.bot_speak(
                ''' LIÊN HỆ<br>
                Phòng D003, Dãy nhà D, Trường Đại học Sài Gòn<br>
                273 An Dương Vương, P.3, Q.5, TP.Hồ Chí Minh<br>
                SĐT : (028) 38-303-108<br>
                Email : sdh@sgu.edu.vn'''))
            self.add_single_shot_timer(45000, lambda: self.bot_speak(
                'Bạn có muốn xem thông tin khác không'))
            self.add_single_shot_timer(50000, self.hotro_thongtin1)
        else:
            self.add_single_shot_timer(0, lambda: self.bot_speak(
                'Xin bạn nhắc lại ạ'))

    def hotro_thongtin1(self):
        text = self.get_voice()
        if text is None:
            self.add_single_shot_timer(0, lambda: self.bot_speak(
                'có hay không ạ'))
            self.add_single_shot_timer(5000, self.hotro_thongtin1)
        elif 'có' in text:
            self.add_single_shot_timer(0, self.hotro_thongtin)
        elif 'không' in text:
            self.add_single_shot_timer(0, lambda: self.bot_speak("""Dưới đây là những việc mình có thể hỗ trợ bạn hiện giờ<br>
            - Hỏi về sản phẩm<br>
            - Thông tin về Công Ty ABC<br>
            - Sản phẩm gặp sự cố <br>
            - Phản hồi về sản phẩm của bên mình
            """))
            self.add_single_shot_timer(20000, self.hotro_cactuvan)
        else:
            self.add_single_shot_timer(0, lambda: self.bot_speak(
                'Xin bạn nhắc lại là có hay không ạ'))

# Sản phẩm gặp sự cố
    def hotro_suco(self):
        self.add_single_shot_timer(0, lambda: self.bot_speak(
            'Chúng tôi rất lấy làm tiếc vì sự bất tiện này '))
        self.add_single_shot_timer(5000, lambda: self.bot_speak(
            'Cảm phiền bạn cho chúng tôi biết một số thông tin sau'))
        self.add_single_shot_timer(11000, self.getdata_suco)

    def getid_prd(self, suco):
        text = self.get_voice()
        if text is None:
            self.add_single_shot_timer(0, lambda: self.bot_speak(
                'có vẻ như tôi không nghe thấy,Bạn hãy nhắc lại tên sản phẩm ạ?'))
            self.add_single_shot_timer(5000, lambda: self.getid_prd(suco))
        elif text is not None:
            id_prd = self.spdal.getid_prd(text)
            print(id_prd)
            print(self.checkproduct(id_prd))
            if self.checkproduct(id_prd) == True:
                if id_prd is None:
                    self.add_single_shot_timer(0, lambda: self.bot_speak(
                        'có vẻ như tôi không tìm thấy,Bạn hãy nhắc lại tên sản phẩm ạ?'))
                    self.add_single_shot_timer(
                        5000, lambda: self.getid_prd(suco))
                elif id_prd is not None:
                    suco.PRODUCTID = id_prd
                    self.add_single_shot_timer(
                        3000, lambda: self.getday_prd(suco))
                    return id_prd
            elif self.checkproduct(id_prd) == False:
                self.add_single_shot_timer(0, lambda: self.bot_speak(
                    'Có vẻ như bạn chưa mua sản phẩm này hãy kiểm tra lại'))
                self.add_single_shot_timer(5000, lambda: self.getid_prd(suco))

    def getday_prd(self, suco):
        day_prd = datetime.now().strftime('%d-%m-%Y')
        suco.NGAYPHATHIEN = day_prd
        self.add_single_shot_timer(3000, lambda: self.bot_speak(
            'Bạn gặp sự cố như thế nào hãy nói ngắn gọn ?'))
        self.add_single_shot_timer(8000, lambda: self.getsuco_prd(suco))
        return day_prd

    def getsuco_prd(self, suco):
        suco_prd = self.get_voice()
        if suco_prd is None:
            self.add_single_shot_timer(0, lambda: self.bot_speak(
                'có vẻ như tôi không nghe rõ sự cố, hãy nhắc lại'))
            self.add_single_shot_timer(5000, lambda: self.getsuco_prd(suco))
        elif suco_prd is not None:
            suco.MOTASUCO = suco_prd
            self.add_single_shot_timer(0, lambda: self.spdal.insert_suco(suco))

            self.add_single_shot_timer(5000, lambda: self.bot_speak(
                'Chúng tôi đã ghi nhận lại thông tin lỗi'))

            self.add_single_shot_timer(10000, lambda: self.bot_speak(
                'Bạn có nhu cầu đặt lịch để tới trực tiếp sửa chữa không ạ'))

            self.add_single_shot_timer(15000, self.getdata_suco1)
            return suco_prd

    def getdata_suco(self):
        id_user = self.get_id_user()
        suco = SUCO(id_user)
        self.add_single_shot_timer(0, lambda: self.bot_speak(
            'Bạn gặp sự cố về sản phẩm nào của bên mình ạ'))
        self.add_single_shot_timer(5000, lambda: self.getid_prd(suco))

    def getdata_suco0_5(self):
        text05 = self.get_voice()
        if text05 is None:
            self.add_single_shot_timer(0, lambda: self.bot_speak(
                'có hay không ạ'))
            self.add_single_shot_timer(5000, self.getdata_suco0_5)
        elif 'có' in text05:
            self.add_single_shot_timer(0, self.getdata_suco)
        elif 'không' in text05:
            self.add_single_shot_timer(0, lambda: self.bot_speak("""Dưới đây là những việc mình có thể hỗ trợ bạn hiện giờ<br>
            - Hỏi về sản phẩm<br>
            - Thông tin về Công Ty ABC<br>
            - Sản phẩm gặp sự cố <br>
            - Phản hồi về sản phẩm của bên mình
            """))
            self.add_single_shot_timer(15000, self.hotro_cactuvan)

    def getdata_suco1(self):
        text = self.get_voice()
        if text is None:
            self.add_single_shot_timer(0, lambda: self.bot_speak(
                'có hay không ạ'))
            self.add_single_shot_timer(5000, self.getdata_suco1)
        elif 'có' in text:
            self.add_single_shot_timer(0, self.getdata_datlich)
        elif 'không' in text:
            self.add_single_shot_timer(0, lambda: self.bot_speak(
                'Bạn có muốn tiếp tục báo cáo sự cố khác không ạ'))
            self.add_single_shot_timer(5000, self.getdata_suco0_5)
        else:
            self.add_single_shot_timer(0, lambda: self.bot_speak(
                'Xin bạn nhắc lại là có hay không ạ'))
##############################################################################

    '''def is_valid_date(self, day_prd):
        numbers = re.findall(r'\d+', day_prd)
        if len(numbers) == 3:
            day, month, year = map(int, numbers)
            tomorrow = datetime.now().date() + timedelta(days=1)
            if datetime(year, month, day).date() < tomorrow:
                return False
            elif month == 2 and day > 29:
                return False
            elif month in [4, 6, 9, 11] and day > 30:
                return False
            elif month in [1, 3, 5, 7, 8, 10, 12] and day > 31:
                return False
            elif year < datetime.now().year or year > datetime.now().year:
                return False
            else:
                return True
        else:
            return False'''
    
    def is_valid_date(self, day_prd):
        numbers = re.findall(r'\d+', day_prd)
        if len(numbers) == 3:
            day, month, year = map(int, numbers)        
            if month == 2 and day > 29:
                return False
            elif month in [4, 6, 9, 11] and day > 30:
                return False
            elif month in [1, 3, 5, 7, 8, 10, 12] and day > 31:
                return False
            elif day <= datetime.now().day :
                return False
            elif month < datetime.now().month or month > datetime.now().month:
                return False
            elif year < datetime.now().year or year > datetime.now().year:
                return False
            else:
                return True
        else:
            return False

    def getdata_datlich(self):
        self.add_single_shot_timer(0, lambda: self.bot_speak(
            'Bạn hãy cho mình biết một số thông tin để tiến hành đặt lịch'))
        self.add_single_shot_timer(5000, self.getdata_datlich1)

    def getdata_ngayhen(self, datlich):
        get_ngayhen = self.get_voice()
        if self.is_valid_date(get_ngayhen)==True:
            datlich.NGAYHEN = get_ngayhen
            self.add_single_shot_timer(0, lambda: self.bot_speak(
                'Bạn hãy cho mình biết thời gian'))
            self.add_single_shot_timer(
                5000, lambda: self.getdata_thoigian(datlich))
            return get_ngayhen
        elif get_ngayhen is None or self.is_valid_date(get_ngayhen) == False:
            self.add_single_shot_timer(0, lambda: self.bot_speak(
                'Ngày tháng năm không hợp lệ, vui lòng nhập lại'))
            self.add_single_shot_timer(
                5000, lambda: self.getdata_ngayhen(datlich))

    def getdata_thoigian(self, datlich):
        get_thoigian = self.get_voice()
        if self.is_valid_time(get_thoigian):
            datlich.THOIGIAN = get_thoigian
            self.add_single_shot_timer(0, lambda: self.bot_speak(
                'Bạn hãy cho mình biết nội dung'))
            self.add_single_shot_timer(
                5000, lambda: self.getdata_noidung(datlich))
            return get_thoigian
        elif get_thoigian is None or self.is_valid_time(get_thoigian) == False:
            self.add_single_shot_timer(0, lambda: self.bot_speak(
                'giờ không hợp lệ, vui lòng nhập lại'))
            self.add_single_shot_timer(
                5000, lambda: self.getdata_thoigian(datlich))

    def is_valid_time(self, time_str):
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

    def getdata_noidung(self, datlich):
        get_noidung = self.get_voice()
        if get_noidung is None:
            self.add_single_shot_timer(0, lambda: self.bot_speak(
                'có vẻ như tôi không nghe rõ nội dung, hãy nhắc lại'))
            self.add_single_shot_timer(
                5000, lambda: self.getdata_noidung(datlich))
        elif get_noidung is not None:
            datlich.NOIDUNG = get_noidung
            self.add_single_shot_timer(
                5000, lambda: self.spdal.insert_datlich(datlich))

            self.add_single_shot_timer(10000, lambda: self.bot_speak(
                'Chúng tôi đã ghi nhận lại thông tin đặt lịch'))

            self.add_single_shot_timer(13000, self.send_email)

            self.add_single_shot_timer(17000, lambda: self.bot_speak(
                'Bên mình đã gửi mail cho bạn'))

            self.add_single_shot_timer(23000, lambda: self.bot_speak(
                'Bạn có muốn bên mình tư vấn gì tiếp không'))

            self.add_single_shot_timer(28000, self.getdata_datlich2)
            return get_noidung

    def getdata_datlich1(self):
        id_user = self.get_id_user()
        datlich = DATLICH(id_user)

        self.add_single_shot_timer(0, lambda: self.bot_speak(
            'Bạn hãy cho mình biết ngày tháng năm bạn muốn đặt lịch'))
        self.add_single_shot_timer(5000, lambda: self.getdata_ngayhen(datlich))

    def getdata_datlich2(self):
        text = self.get_voice()
        if text is None:
            self.add_single_shot_timer(0, lambda: self.bot_speak(
                'có hay không ạ'))
            self.add_single_shot_timer(5000, self.getdata_datlich2)
        elif 'có' in text:
            self.add_single_shot_timer(5000, lambda: self.bot_speak("""Dưới đây là những việc mình có thể hỗ trợ bạn hiện giờ<br>
            - Hỏi về sản phẩm<br>
            - Thông tin về Công Ty ABC<br>
            - Sản phẩm gặp sự cố <br>
            - Phản hồi về sản phẩm của bên mình
            """))
            self.add_single_shot_timer(20000, self.hotro_cactuvan)
        elif 'không' in text:
            self.add_single_shot_timer(5000, lambda: self.bot_speak(
                'Cảm ơn bạn đã sử dụng dịch vụ chăm sóc khách hàng'))
            self.add_single_shot_timer(10000, self.stop)
        else:
            self.add_single_shot_timer(0, lambda: self.bot_speak(
                'Xin bạn nhắc lại ạ'))

    def send_email(self):
        # Thông tin người gửi và người nhận
        email = self.get_email()
        from_email = "brokayyy@gmail.com"
        to_email = f"{email}"
        # Tạo message
        message = MIMEMultipart()
        message['From'] = from_email
        message['To'] = to_email
        message['Subject'] = f"THÔNG BÁO ĐẶT LỊCH CÔNG TY ABC"
        body = f"""
XIN CHÀO {self.username}, ĐÂY LÀ THÔNG BÁO VỀ LỊCH HẸN CỦA BẠN
Ngày hẹn: {self.get_email_ngayhen()}
Thời gian: {self.get_email_thoigian()} 
Nội dung đặt lịch: {self.get_email_noidung()}
Sản phẩm gặp sự cố: {self.get_name_product()}
Ngày gặp sự cố: {self.get_email_ngaygapsuco()}
Nội dung sự cố: {self.get_email_noidungsuco()}
Đ/c: Phòng D003, Dãy nhà D, Trường Đại học Sài Gòn 273 An Dương Vương, P.3, Q.5, TP.Hồ Chí Minh
*Note: Khi đến trung tâm bạn nhớ đưa mail này cho nhân viên bên mình để xác nhận đặt lịch ạ"""
        message.attach(MIMEText(body, 'plain'))
        # Kết nối đến SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        # Đăng nhập vào tài khoản email của người gửi
        password = "pwzaouydletjjkzk"
        server.login(from_email, password)
        # Gửi email
        text = message.as_string()
        server.sendmail(from_email, to_email, text)
        # Đóng kết nối
        server.quit()
####################################################

    def hotro_phanhoi(self):
        self.add_single_shot_timer(0, lambda: self.bot_speak(
            'Để phản hồi bên mình bạn vui lòng cho mình biết một số thông tin nhé'))
        self.add_single_shot_timer(7000, self.getdata_phanhoi)

    def getdata_phanhoi(self):
        id_user = self.get_id_user()
        reviews = REVIEWS(id_user)
        self.add_single_shot_timer(0, lambda: self.bot_speak(
            'Bạn muốn phản hồi hay góp ý về sản phẩm nào ạ?'))
        self.add_single_shot_timer(
            5000, lambda: self.getid_prdphanhoi(reviews))

    def getid_prdphanhoi(self, reviews):
        text = self.get_voice()
        if text is None:
            self.add_single_shot_timer(0, lambda: self.bot_speak(
                'có vẻ như tôi không nghe thấy,Bạn hãy nhắc lại tên sản phẩm ạ?'))
            self.add_single_shot_timer(
                5000, lambda: self.getid_prdphanhoi(reviews))
        elif text is not None:
            id_prd = self.spdal.getid_prd(text)
            if self.checkproduct(id_prd) == True:
                if id_prd is None:
                    self.add_single_shot_timer(0, lambda: self.bot_speak(
                        'có vẻ như tôi không tìm thấy,Bạn hãy nhắc lại tên sản phẩm ạ?'))
                    self.add_single_shot_timer(
                        5000, lambda: self.getid_prdphanhoi(reviews))
                elif id_prd is not None:
                    reviews.PRODUCTID = id_prd
                    self.add_single_shot_timer(0, lambda: self.bot_speak(
                        'Bạn hãy cho mình biết đánh giá trên thang điểm 10 về dịch vụ bên mình?'))
                    self.add_single_shot_timer(
                        7000, lambda: self.get_rating(reviews))
                    return id_prd
            elif self.checkproduct(id_prd) == False:
                self.add_single_shot_timer(0, lambda: self.bot_speak(
                    'Có vẻ như bạn chưa mua sản phẩm này hãy kiểm tra lại'))
                self.add_single_shot_timer(
                    5000, lambda: self.getid_prdphanhoi(reviews))

    def is_valid_score(self, scores):
        numbers = re.findall(r'\d+', scores)
        if len(numbers) == 1:
            score = int(numbers[0])
            if 0 <= score <= 10:
                return True
            else:
                return False
        else:
            return False
        
    def get_rating(self, reviews):
        rating_prd = self.get_voice()
        if rating_prd is None or self.is_valid_score(rating_prd) == False:
            self.add_single_shot_timer(0, lambda: self.bot_speak(
                'có vẻ như tôi không nghe rõ hoặc rating của bạn không hợp lệ, hãy nhắc lại'))
            self.add_single_shot_timer(7000, lambda: self.get_rating(reviews))
        elif rating_prd is not None:
            if self.is_valid_score(rating_prd)==True:
                reviews.RATING = rating_prd
                self.add_single_shot_timer(0, lambda: self.bot_speak(
                    'Bạn hãy cho dịch vụ bên mình lời nhận xét'))
                self.add_single_shot_timer(5000, lambda: self.get_cmt(reviews))
                return rating_prd

    def get_cmt(self, reviews):
        get_noidung = self.get_voice()
        if get_noidung is None:
            self.add_single_shot_timer(0, lambda: self.bot_speak(
                'có vẻ như tôi không nghe rõ nội dung, hãy nhắc lại'))
            self.add_single_shot_timer(5000, lambda: self.get_cmt(reviews))
        elif get_noidung is not None:
            reviews.COMMENT = get_noidung
            self.add_single_shot_timer(
                5000, lambda: self.spdal.insert_phanhoi(reviews))

            self.add_single_shot_timer(10000, lambda: self.bot_speak(
                'Cảm ơn bạn đã phản hồi bên mình sẽ ghi nhận góp ý của bạn'))

            self.add_single_shot_timer(17000, lambda: self.bot_speak(
                'Bạn có muốn bên mình tư vấn gì tiếp không'))

            self.add_single_shot_timer(20000, self.getdata_phanhoi2)
            return get_noidung

    def getdata_phanhoi2(self):
        text = self.get_voice()
        if text is None:
            self.add_single_shot_timer(0, lambda: self.bot_speak(
                'có hay không ạ'))
            self.add_single_shot_timer(5000, self.getdata_phanhoi2)
        elif 'có' in text:
            self.add_single_shot_timer(5000, lambda: self.bot_speak("""Dưới đây là những việc mình có thể hỗ trợ bạn hiện giờ<br>
            - Hỏi về sản phẩm<br>
            - Thông tin về Công Ty ABC<br>
            - Sản phẩm gặp sự cố <br>
            - Phản hồi về sản phẩm của bên mình
            """))
            self.add_single_shot_timer(20000, self.hotro_cactuvan)
        elif 'không' in text:
            self.add_single_shot_timer(5000, self.stop)
        else:
            self.add_single_shot_timer(0, lambda: self.bot_speak(
                'Xin bạn nhắc lại là có hay không ạ'))

    #################################################################################################

    def add_timer(self, timer):
        self.timers.append(timer)

    def reset_timers(self):
        for timer in self.timers:
            if timer and timer.isActive():
                timer.stop()
                timer.deleteLater()
        self.timers = []

    def add_single_shot_timer(self, interval, slot):
        timer = QTimer()
        timer.setSingleShot(True)
        timer.timeout.connect(slot)
        self.add_timer(timer)
        timer.start(interval)

    def send_message(self):
        self.start_button.setEnabled(False)
        self.end_button.setEnabled(True)
        self.logout_button.setEnabled(False)
        self.stop_flag = False
        self.chat_display.clear()

        # Đặt lại giá trị cho tất cả các QTimer
        self.reset_timers()

        name = self.get_full_name()
        QTimer.singleShot(0, lambda: self.bot_speak(f"""Đây là ứng dụng chăm sóc khách hàng của Công Ty ABC<br>
         Xin chào {name}, mình rất vui được gặp cậu"""))
        QTimer.singleShot(10000, lambda: self.bot_speak("""Dưới đây là những việc mình có thể hỗ trợ bạn hiện giờ<br>
         - Hỏi về sản phẩm<br>
         - Thông tin về Công Ty ABC<br>
         - Sản phẩm gặp sự cố <br>
        - Phản hồi về sản phẩm của bên mình
        """))
        self.add_single_shot_timer(25000, self.hotro_cactuvan)
