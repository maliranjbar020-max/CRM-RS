from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QStackedWidget
)
from PySide6.QtCore import Qt

from ui.customers import CustomersPage
from ui.products import ProductsPage
from ui.sms import SMSPage


class Dashboard(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("CRM RS")
        self.resize(1400, 800)

        central = QWidget()
        self.setCentralWidget(central)

        layout = QHBoxLayout(central)

        # ---------- منوی سمت چپ ----------

        menu = QVBoxLayout()

        title = QLabel("CRM RS")
        title.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
        """)

        btn_home = QPushButton("🏠 خانه")
        btn_customers = QPushButton("👤 مشتریان")
        btn_products = QPushButton("📦 انبار")
        btn_invoice = QPushButton("💰 فاکتورها")
        btn_cut = QPushButton("✂️ برش")
        btn_send = QPushButton("🚚 ارسال")
        btn_sms = QPushButton("📨 ارسال پیامک")

        menu.addWidget(title)
        menu.addSpacing(20)

        menu.addWidget(btn_home)
        menu.addWidget(btn_customers)
        menu.addWidget(btn_products)
        menu.addWidget(btn_invoice)
        menu.addWidget(btn_cut)
        menu.addWidget(btn_send)
        menu.addWidget(btn_sms)

        menu.addStretch()

        layout.addLayout(menu, 1)

        # ---------- صفحات ----------

        self.stack = QStackedWidget()

        home = QLabel("به CRM RS خوش آمدید")
        home.setAlignment(Qt.AlignCenter)
        home.setStyleSheet("""
            font-size:30px;
            font-weight:bold;
        """)

        self.customers = CustomersPage()
        self.products = ProductsPage()
        self.sms = SMSPage()

        self.stack.addWidget(home)
        self.stack.addWidget(self.customers)
        self.stack.addWidget(self.products)
        self.stack.addWidget(self.sms)

        layout.addWidget(self.stack, 4)

        # ---------- اتصال دکمه‌ها ----------

        btn_home.clicked.connect(
            lambda: self.stack.setCurrentIndex(0)
        )

        btn_customers.clicked.connect(
            lambda: self.stack.setCurrentIndex(1)
        )

        btn_products.clicked.connect(
            lambda: self.stack.setCurrentIndex(2)
        )

        btn_sms.clicked.connect(
            lambda: self.stack.setCurrentIndex(3)
        )