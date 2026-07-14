from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTextEdit,
    QPushButton,
    QComboBox,
    QMessageBox,
    QListWidget,
    QListWidgetItem,
    QCheckBox,
    QFileDialog
)

from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import Qt

from sms.manager import SMSManager
from database import get_all_customers


class SMSPage(QWidget):

    def __init__(self):
        super().__init__()

        self.sms = SMSManager()

        layout = QVBoxLayout(self)

        title = QLabel("ارسال پیامک")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size:26px;
            font-weight:bold;
        """)

        self.method = QComboBox()

        self.method.addItem("ارسال با گوشی", "phone")
        self.method.addItem("ارسال با پنل پیامکی", "panel")

        current = self.sms.get_method()

        index = self.method.findData(current)

        if index >= 0:
            self.method.setCurrentIndex(index)

        self.method.currentIndexChanged.connect(
            self.change_method
        )

        self.all_customers = QCheckBox(
            "ارسال به همه مشتریان"
        )

        self.list = QListWidget()

        self.load_customers()

        self.message = QTextEdit()

        self.message.setPlaceholderText(
            "متن پیام را وارد کنید..."
        )

        self.send = QPushButton("📨 ارسال پیامک")
        self.copy = QPushButton("📋 کپی شماره‌ها")
        self.export = QPushButton("💾 خروجی TXT")

        self.send.clicked.connect(self.send_sms)
        self.copy.clicked.connect(self.copy_numbers)
        self.export.clicked.connect(self.export_numbers)

        layout.addWidget(title)
        layout.addWidget(self.method)
        layout.addWidget(self.all_customers)

        layout.addWidget(
            QLabel("مشتریان")
        )

        layout.addWidget(self.list)
        layout.addWidget(self.message)

        layout.addWidget(self.send)
        layout.addWidget(self.copy)
        layout.addWidget(self.export)

    def change_method(self):

        method = self.method.currentData()

        self.sms.save_method(method)

    def load_customers(self):

        self.list.clear()

        customers = get_all_customers()

        for customer in customers:

            item = QListWidgetItem(
                f"{customer[1]}   ({customer[2]})"
            )

            item.setData(
                Qt.UserRole,
                customer[2]
            )

            item.setCheckState(
                Qt.Unchecked
            )

            self.list.addItem(item)

    def get_numbers(self):

        numbers = []

        if self.all_customers.isChecked():

            for i in range(self.list.count()):

                number = self.list.item(i).data(Qt.UserRole)

                if number:

                    number = number.strip()

                    if number.startswith("0"):
                        number = number[1:]

                    if len(number) == 10 and number.isdigit():

                        if number not in numbers:
                            numbers.append(number)

        else:

            for i in range(self.list.count()):

                item = self.list.item(i)

                if item.checkState() == Qt.Checked:

                    number = item.data(Qt.UserRole)

                    if number:

                        number = number.strip()

                        if number.startswith("0"):
                            number = number[1:]

                        if len(number) == 10 and number.isdigit():

                            if number not in numbers:
                                numbers.append(number)

        return numbers

    def send_sms(self):

        message = self.message.toPlainText().strip()

        if message == "":

            QMessageBox.warning(
                self,
                "خطا",
                "متن پیام را وارد کنید."
            )

            return

        numbers = self.get_numbers()

        if len(numbers) == 0:

            QMessageBox.warning(
                self,
                "خطا",
                "حداقل یک مشتری انتخاب کنید."
            )

            return

        result = self.sms.send_sms(
            numbers,
            message
        )

        QMessageBox.information(
            self,
            "نتیجه ارسال",
            str(result)
        )

    def copy_numbers(self):

        numbers = self.get_numbers()

        if len(numbers) == 0:

            QMessageBox.warning(
                self,
                "خطا",
                "شماره‌ای وجود ندارد."
            )

            return

        text = "\n".join(numbers)

        QGuiApplication.clipboard().setText(text)

        QMessageBox.information(
            self,
            "انجام شد",
            f"{len(numbers)} شماره در کلیپ‌بورد کپی شد."
        )

    def export_numbers(self):

        numbers = self.get_numbers()

        if len(numbers) == 0:

            QMessageBox.warning(
                self,
                "خطا",
                "شماره‌ای وجود ندارد."
            )

            return

        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "ذخیره فایل",
            "customers.txt",
            "Text Files (*.txt)"
        )

        if not file_name:
            return

        with open(file_name, "w", encoding="utf-8") as f:

            f.write("\n".join(numbers))

        QMessageBox.information(
            self,
            "ذخیره شد",
            f"{len(numbers)} شماره ذخیره شد."
        )