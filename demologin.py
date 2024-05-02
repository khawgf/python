import speech_recognition as sr
import pyttsx3
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QRect
import time
from gtts import gTTS
import os
import playsound
import sys
import sqlite3
from demo import MyWidget


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Tạo các thành phần UI

        # Tạo các thành phần UI

        # Tạo các thành phần UI
        self.username_label = QLabel('Tên đăng nhập', self)
        self.username_input = QLineEdit(self)
        self.password_label = QLabel('Mật khẩu', self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(
            QLineEdit.Password)  # Ẩn chữ khi nhập mật khẩu
        self.login_button = QPushButton('Đăng nhập', self)

        # Tạo layout cho UI
        username_layout = QHBoxLayout()
        username_layout.addWidget(self.username_label)
        username_layout.addWidget(self.username_input)

        password_layout = QHBoxLayout()
        password_layout.addWidget(self.password_label)
        password_layout.addWidget(self.password_input)

        login_layout = QHBoxLayout()
        login_layout.addStretch()
        login_layout.addWidget(self.login_button)
        login_layout.addStretch()

        vbox = QVBoxLayout(self)
        vbox.addStretch()
        vbox.addLayout(username_layout)
        vbox.addLayout(password_layout)
        vbox.addStretch()
        vbox.addLayout(login_layout)
        vbox.addStretch()

        self.setLayout(vbox)
        self.setWindowTitle('LOGIN')
        # Kết nối sự kiện đăng nhập
        self.login_button.clicked.connect(self.login)

        # Thiết lập kích thước cửa sổ
        self.setFixedSize(400, 250)

        # Thiết lập kích thước các thành phần UI
        self.username_label.setFixedSize(120, 30)
        self.username_input.setFixedSize(200, 30)
        self.password_label.setFixedSize(120, 30)
        self.password_input.setFixedSize(200, 30)
        self.login_button.setFixedSize(100, 30)

    def login(self):
        # Kiểm tra thông tin đăng nhậpadmin
        username = self.username_input.text()
        password = self.password_input.text()
        self.conn = sqlite3.connect('doanpython.db')
        # Kiểm tra thông tin đăng nhập trong database
        c = self.conn.cursor()
        c.execute(
            'SELECT *FROM USERS WHERE USERNAME = ? AND PASSWORD = ?', (username, password))
        user = c.fetchone()

        if user is not None:
            # Nếu thông tin đăng nhập chính xác, chuyển sang giao diện ứng dụng chính
            self.hide()  # Ẩn giao diện đăng nhập
            # Tạo một đối tượng MyWidget mới
            self.my_widget = MyWidget(username)
            self.my_widget.show()  # Hiển thị giao diện MyWidget
        else:
            # Nếu thông tin đăng nhập sai, hiển thị thông báo lỗi
            error_message = 'Sai tên đăng nhập hoặc mật khẩu'
            QMessageBox.warning(
                self, 'Đăng nhập không thành công', error_message, QMessageBox.Ok)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
