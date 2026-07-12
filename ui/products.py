from PySide6.QtWidgets import (
    QWidget,QVBoxLayout,QHBoxLayout,QFormLayout,QLabel,QLineEdit,
    QPushButton,QTableWidget,QTableWidgetItem,QHeaderView
)

class ProductsPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        title = QLabel("مدیریت کالاها و انبار")
        title.setStyleSheet("font-size:24px;font-weight:bold;")

        self.search = QLineEdit()
        self.search.setPlaceholderText("جستجوی کالا...")

        form = QFormLayout()

        self.name = QLineEdit()
        self.category = QLineEdit()
        self.thickness = QLineEdit()
        self.width = QLineEdit()
        self.length = QLineEdit()
        self.brand = QLineEdit()
        self.unit = QLineEdit()
        self.stock = QLineEdit()
        self.min_stock = QLineEdit()
        self.buy_price = QLineEdit()
        self.sell_price = QLineEdit()
        self.warehouse = QLineEdit()

        fields = [
            ("نام کالا",self.name),
            ("دسته",self.category),
            ("ضخامت",self.thickness),
            ("عرض",self.width),
            ("طول",self.length),
            ("برند",self.brand),
            ("واحد",self.unit),
            ("موجودی",self.stock),
            ("حداقل موجودی",self.min_stock),
            ("قیمت خرید",self.buy_price),
            ("قیمت فروش",self.sell_price),
            ("انبار",self.warehouse),
        ]
        for t,w in fields:
            form.addRow(t,w)

        btns = QHBoxLayout()
        self.save_btn=QPushButton("💾 ثبت")
        self.edit_btn=QPushButton("✏ ویرایش")
        self.delete_btn=QPushButton("🗑 حذف")
        self.edit_btn.setEnabled(False)
        self.delete_btn.setEnabled(False)
        btns.addWidget(self.save_btn)
        btns.addWidget(self.edit_btn)
        btns.addWidget(self.delete_btn)

        self.table=QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "نام","دسته","ضخامت","ابعاد","برند","موجودی","فروش","وضعیت"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addWidget(title)
        layout.addWidget(self.search)
        layout.addLayout(form)
        layout.addLayout(btns)
        layout.addWidget(self.table)
