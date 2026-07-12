from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView
)

from database import (
    add_customer,
    get_customers,
    search_customers,
    delete_customer,
    update_customer
)


class CustomersPage(QWidget):

    def __init__(self):
        super().__init__()

        self.selected_id = None

        layout = QVBoxLayout()

        title = QLabel("مدیریت مشتریان")
        title.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
        """)

        self.search = QLineEdit()
        self.search.setPlaceholderText("جستجوی مشتری...")
        self.search.textChanged.connect(self.search_data)

        form = QFormLayout()

        self.name = QLineEdit()
        self.phone = QLineEdit()
        self.company = QLineEdit()
        self.address = QLineEdit()

        form.addRow("نام", self.name)
        form.addRow("موبایل", self.phone)
        form.addRow("شرکت", self.company)
        form.addRow("آدرس", self.address)

        buttons = QHBoxLayout()

        self.save_btn = QPushButton("💾 ثبت")
        self.update_btn = QPushButton("✏ ویرایش")
        self.delete_btn = QPushButton("🗑 حذف")

        self.update_btn.setEnabled(False)
        self.delete_btn.setEnabled(False)

        buttons.addWidget(self.save_btn)
        buttons.addWidget(self.update_btn)
        buttons.addWidget(self.delete_btn)

        self.table = QTableWidget()

        self.table.setColumnCount(5)

        self.table.setHorizontalHeaderLabels([
            "کد",
            "نام",
            "موبایل",
            "شرکت",
            "آدرس"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.table.cellClicked.connect(
            self.select_customer
        )

        self.save_btn.clicked.connect(
            self.save_customer
        )

        self.update_btn.clicked.connect(
            self.update_selected
        )

        self.delete_btn.clicked.connect(
            self.delete_selected
        )

        layout.addWidget(title)
        layout.addWidget(self.search)
        layout.addLayout(form)
        layout.addLayout(buttons)
        layout.addWidget(self.table)

        self.setLayout(layout)

        self.load_customers()


    def fill_table(self, data):

        self.table.setRowCount(len(data))

        for row, customer in enumerate(data):

            for col, value in enumerate(customer):

                self.table.setItem(
                    row,
                    col,
                    QTableWidgetItem(str(value))
                )


    def load_customers(self):

        self.fill_table(
            get_customers()
        )


    def search_data(self):

        text = self.search.text()

        if text == "":
            self.load_customers()

        else:
            self.fill_table(
                search_customers(text)
            )


    def save_customer(self):

        ok = add_customer(
            self.name.text(),
            self.phone.text(),
            self.company.text(),
            self.address.text()
        )

        if not ok:

            QMessageBox.warning(
                self,
                "خطا",
                "این شماره موبایل قبلاً ثبت شده است."
            )

            return

        QMessageBox.information(
            self,
            "ثبت شد",
            "مشتری ذخیره شد."
        )

        self.clear_form()
        self.load_customers()


    def select_customer(self, row, column):

        self.selected_id = int(
            self.table.item(row, 0).text()
        )

        self.name.setText(
            self.table.item(row, 1).text()
        )

        self.phone.setText(
            self.table.item(row, 2).text()
        )

        self.company.setText(
            self.table.item(row, 3).text()
        )

        self.address.setText(
            self.table.item(row, 4).text()
        )

        self.update_btn.setEnabled(True)
        self.delete_btn.setEnabled(True)


    def update_selected(self):

        if self.selected_id is None:
            return

        update_customer(
            self.selected_id,
            self.name.text(),
            self.phone.text(),
            self.company.text(),
            self.address.text()
        )

        QMessageBox.information(
            self,
            "ویرایش شد",
            "اطلاعات مشتری بروزرسانی شد."
        )

        self.clear_form()
        self.load_customers()


    def delete_selected(self):

        if self.selected_id is None:
            return

        result = QMessageBox.question(
            self,
            "حذف مشتری",
            "از حذف این مشتری مطمئن هستید؟",
            QMessageBox.Yes | QMessageBox.No
        )

        if result == QMessageBox.Yes:

            delete_customer(
                self.selected_id
            )

            QMessageBox.information(
                self,
                "حذف شد",
                "مشتری حذف شد."
            )

            self.clear_form()
            self.load_customers()


    def clear_form(self):

        self.selected_id = None

        self.name.clear()
        self.phone.clear()
        self.company.clear()
        self.address.clear()

        self.update_btn.setEnabled(False)
        self.delete_btn.setEnabled(False)