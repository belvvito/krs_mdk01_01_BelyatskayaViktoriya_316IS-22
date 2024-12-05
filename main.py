import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget, QLabel, QFormLayout


def create_database():
    conn = sqlite3.connect("store.db")
    cursor = conn.cursor()

    # Создание таблицы "Категория".
    cursor.execute('''CREATE TABLE IF NOT EXISTS Category (
                        Category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        Name_category VARCHAR(50) NOT NULL,
                        Description VARCHAR(150))''')

    # Создание таблицы "Товары".
    cursor.execute('''CREATE TABLE IF NOT EXISTS Products (
                        Product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        Name VARCHAR(100) NOT NULL,
                        Category_id INTEGER,
                        Description VARCHAR(150),
                        Price VARCHAR(50),
                        Article VARCHAR(50),
                        FOREIGN KEY (Category_id) REFERENCES Category (Category_id))''')

    # Создание таблицы "Пользователи" с паролем.
    cursor.execute('''CREATE TABLE IF NOT EXISTS Customers (
                        Customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        Fio VARCHAR(100) NOT NULL,
                        Phone VARCHAR(20),
                        Email VARCHAR(100),
                        Password VARCHAR(20))''')
    # Создание таблицы "Продавец".
    cursor.execute('''CREATE TABLE IF NOT EXISTS Saleman (
                        Saleman_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        Fio VARCHAR(100) NOT NULL,
                        Phone VARCHAR(20))''')

    # Создание таблицы "Кассир".
    cursor.execute('''CREATE TABLE IF NOT EXISTS Cashier (
                        Cashier_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        Fio VARCHAR(100) NOT NULL,
                        Phone VARCHAR(20))''')

    # Создание таблицы "Склад".
    cursor.execute('''CREATE TABLE IF NOT EXISTS Warehouse (
                        Warehouse_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        Product_id INTEGER,
                        Amount VARCHAR(50) NOT NULL,
                        FOREIGN KEY (Product_id) REFERENCES Products (Product_id))''')

    # Создание таблицы "Заказ".
    cursor.execute('''CREATE TABLE IF NOT EXISTS Orders (
                        Order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        Product_id INTEGER,
                        Customer_id INTEGER,
                        Salesman_id INTEGER,
                        FOREIGN KEY (Product_id) REFERENCES Products (Product_id),
                        FOREIGN KEY (Customer_id) REFERENCES Customers (Customer_id),
                        FOREIGN KEY (Salesman_id) REFERENCES Saleman (Saleman_id))''')

    # Создание таблицы "Оплата".
    cursor.execute('''CREATE TABLE IF NOT EXISTS Payment (
                        Payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        Order_id INTEGER,
                        Salesman_id INTEGER,
                        Cashier_id INTEGER,
                        FOREIGN KEY (Order_id) REFERENCES Orders (Order_id),
                        FOREIGN KEY (Salesman_id) REFERENCES Saleman (Saleman_id),
                        FOREIGN KEY (Cashier_id) REFERENCES Cashier (Cashier_id))''')

    # Сохранение изменений и закрытие подключения.
    conn.commit()
    conn.close()


# Окно авторизации
class AuthWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Авторизация')
        self.setGeometry(100, 100, 300, 200)

        # Основной виджет и макет
        self.main_widget = QWidget()
        self.layout = QVBoxLayout()

        # Поля для ввода данных
        self.email_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_button = QPushButton('Войти')
        self.register_button = QPushButton('Зарегистрироваться')

        # Добавление элементов на окно
        self.layout.addWidget(QLabel('Email'))
        self.layout.addWidget(self.email_input)
        self.layout.addWidget(QLabel('Пароль'))
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.login_button)
        self.layout.addWidget(self.register_button)

        # Обработчики кнопок
        self.login_button.clicked.connect(self.login)
        self.register_button.clicked.connect(self.register)

        # Устанавливаем виджет в окно
        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)

    def login(self):
        email = self.email_input.text()
        password = self.password_input.text()

        print(f"Попытка авторизации: Email={email}, Пароль={password}")  # Отладка

        # Логика авторизации
        try:
            conn = sqlite3.connect("store.db")
            cursor = conn.cursor()

            # Поиск пользователя по email и паролю
            cursor.execute("SELECT * FROM Customers WHERE Email = ? AND Password = ?", (email, password))
            user = cursor.fetchone()

            if email == 'admin' and password == 'admin':
                print("Авторизация администратора успешна!")  # Отладка
                self.admin_window = AdminWindow(user)
                self.admin_window.show()
                self.close()
            elif user:
                print("Авторизация успешна!")  # Отладка
                self.main_window = MainWindow(user)
                self.main_window.show()
                self.close()
            else:
                print("Неверный email или пароль.")  # Отладка
            conn.close()

        except sqlite3.Error as e:
            print(f"Ошибка при подключении к базе данных: {e}")  # Отладка

    def register(self):
        self.register_window = RegisterWindow()
        self.register_window.show()
        self.close()


# Окно регистрации
class RegisterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Регистрация')
        self.setGeometry(100, 100, 300, 250)

        self.main_widget = QWidget()
        self.layout = QFormLayout()

        self.name_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.register_button = QPushButton('Зарегистрироваться')

        self.layout.addRow("ФИО:", self.name_input)
        self.layout.addRow("Телефон:", self.phone_input)
        self.layout.addRow("Email:", self.email_input)
        self.layout.addRow("Пароль:", self.password_input)
        self.layout.addWidget(self.register_button)

        self.register_button.clicked.connect(self.register_user)

        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)

    def register_user(self):
        name = self.name_input.text()
        phone = self.phone_input.text()
        email = self.email_input.text()
        password = self.password_input.text()

        # Регистрация нового пользователя в базе данных
        try:
            conn = sqlite3.connect("store.db")
            cursor = conn.cursor()

            # Проверка на наличие пользователя с таким email
            cursor.execute("SELECT * FROM Customers WHERE Email = ?", (email,))
            existing_user = cursor.fetchone()

            if existing_user:
                print("Пользователь с таким email уже существует.")  # Отладка
            else:
                cursor.execute("INSERT INTO Customers (Fio, Phone, Email, Password) VALUES (?, ?, ?, ?)",
                               (name, phone, email, password))
                conn.commit()
                print(f"Пользователь {name} зарегистрирован.")  # Отладка
            conn.close()

        except sqlite3.Error as e:
            print(f"Ошибка при подключении к базе данных: {e}")  # Отладка


# Главное окно (после входа)
class MainWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.setWindowTitle('Главное окно')
        self.setGeometry(100, 100, 400, 300)
        self.user = user

        self.main_widget = QWidget()
        self.layout = QVBoxLayout()

        # Кнопки для оформление заказа и оплаты
        self.add_to_order_button = QPushButton('Оформить заказ')
        self.pay_button = QPushButton('Оформить оплату')

        self.layout.addWidget(self.add_to_order_button)
        self.layout.addWidget(self.pay_button)

        self.add_to_order_button.clicked.connect(self.add_to_order)
        self.pay_button.clicked.connect(self.pay)

        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)
    def add_to_order(self):
        self.add_order_window = AddOrderWindow()
        self.add_order_window.show()
        self.close()

    def pay(self):
        self.add_payment_window = AddOrderWindow()
        self.add_payment_window.show()
        self.close()

class AddOrderWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Оформление заказа')
        self.setGeometry(100, 100, 300, 250)

        self.main_widget = QWidget()
        self.layout = QFormLayout()

        self.product_id_input = QLineEdit()
        self.customer_id_input = QLineEdit()
        self.salesman_id_input = QLineEdit()
        self.add_button = QPushButton('Оформить заказ')

        self.layout.addRow("Номер продукта:", self.product_id_input)
        self.layout.addRow("Номер пользователя:", self.customer_id_input)
        self.layout.addRow("Номер продавца:", self.salesman_id_input)
        self.layout.addWidget(self.add_button)

        self.add_button.clicked.connect(self.add_order)

        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)

    def add_order(self):
        product_id = self.product_id_input.text()
        customer_id = self.customer_id_input.text()
        salesman_id = self.salesman_id_input.text()


        # Добавление нового заказа в базе данных
        try:
            conn = sqlite3.connect("store.db")
            cursor = conn.cursor()

            cursor.execute("INSERT INTO Orders (Product_id, Customer_id, Salesman_id) VALUES (?, ?, ?)",
                               (product_id, customer_id, salesman_id))
            conn.commit()
            print(f"Заказ оформлен.")  # Отладка
            conn.close()

        except sqlite3.Error as e:
            print(f"Ошибка при подключении к базе данных: {e}")  # Отладка

class AddPaymentWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Оформление оплаты')
        self.setGeometry(100, 100, 300, 250)

        self.main_widget = QWidget()
        self.layout = QFormLayout()

        self.order_id_input = QLineEdit()
        self.customer_id_input = QLineEdit()
        self.salesman_id_input = QLineEdit()
        self.add_button = QPushButton('Оформить оплату')

        self.layout.addRow("Номер заказа:", self.order_id_input)
        self.layout.addRow("Номер пользователя:", self.customer_id_input)
        self.layout.addRow("Номер продавца:", self.salesman_id_input)
        self.layout.addWidget(self.add_button)

        self.add_button.clicked.connect(self.add_payment)

        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)

    def add_payment(self):
        order_id = self.order_id_input.text()
        customer_id = self.customer_id_input.text()
        salesman_id = self.salesman_id_input.text()


        # Добавление новой оплаты в базе данных
        try:
            conn = sqlite3.connect("store.db")
            cursor = conn.cursor()

            cursor.execute("INSERT INTO Payment (Order_id, Customer_id, Salesman_id) VALUES (?, ?, ?)",
                               (order_id, customer_id, salesman_id))
            conn.commit()
            print(f"Оплата оформлена.")  # Отладка
            conn.close()

        except sqlite3.Error as e:
            print(f"Ошибка при подключении к базе данных: {e}")  # Отладка

class AdminWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.setWindowTitle('Главное окно')
        self.setGeometry(100, 100, 400, 300)
        self.user = user

        self.main_widget = QWidget()
        self.layout = QVBoxLayout()

        # Кнопки для добавления товара и категории
        self.add_to_products_button = QPushButton('Добавить товары и категории')
        self.layout.addWidget(self.add_to_products_button)

        self.add_to_products_button.clicked.connect(self.add_to_products)

        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)

        self.add_to_cashier_button = QPushButton('Добавить кассиров и продавцов')
        self.layout.addWidget(self.add_to_cashier_button)

        self.add_to_cashier_button.clicked.connect(self.add_to_cashier)

        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)

    def add_to_products(self):
        self.add_products_window = AddProductsWindow()
        self.add_products_window.show()
        self.close()

    def add_to_cashier(self):
        self.add_cashier_window = AddCashierWindow()
        self.add_cashier_window.show()
        self.close()

class AddProductsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Добавление новых товаров и категорий')
        self.setGeometry(100, 100, 300, 250)

        self.main_widget = QWidget()
        self.layout = QFormLayout()

        self.name_category_input = QLineEdit()
        self.description_category_input = QLineEdit()
        self.add_button = QPushButton('Добавить категорию')

        self.layout.addRow("Название категории:", self.name_category_input)
        self.layout.addRow("Описание категории:", self.description_category_input)
        self.layout.addWidget(self.add_button)

        self.add_button.clicked.connect(self.add_category)

        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)

        self.name_input = QLineEdit()
        self.category_id_input = QLineEdit()
        self.price_input = QLineEdit()
        self.description_input = QLineEdit()
        self.article_input = QLineEdit()
        self.add_button = QPushButton('Добавить товар')

        self.layout.addRow("Название товара:", self.name_input)
        self.layout.addRow("Номер категории:", self.category_id_input)
        self.layout.addRow("Описание товара:", self.description_input)
        self.layout.addRow("Цена товара:", self.price_input)
        self.layout.addRow("Артикул:", self.article_input)
        self.layout.addWidget(self.add_button)

        self.add_button.clicked.connect(self.add_products)

        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)

        self.product_id_for_warehouse_input = QLineEdit()
        self.amount_input = QLineEdit()
        self.add_button = QPushButton('Добавить товар на склад')

        self.layout.addRow("Номер товара:", self.product_id_for_warehouse_input)
        self.layout.addRow("Количество товаров:", self.amount_input)
        self.layout.addWidget(self.add_button)

        self.add_button.clicked.connect(self.add_products_to_warehouse)

        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)

    def add_products(self):
        name = self.name_input.text()
        category_id = self.category_id_input.text()
        description = self.description_input.text()
        price = self.price_input.text()
        article = self.article_input.text()


        # Добавление нового продукта в базе данных
        try:
            conn = sqlite3.connect("store.db")
            cursor = conn.cursor()

            cursor.execute("INSERT INTO Products (Name, Category_id, Description, Price, Article) VALUES (?, ?, ?, ?, ?)",
                               (name, category_id, description, price, article))
            conn.commit()
            print(f"Товар {name} добавлен.")  # Отладка
            conn.close()

        except sqlite3.Error as e:
            print(f"Ошибка при подключении к базе данных: {e}")  # Отладка

    def add_category(self):
        name_category = self.name_category_input.text()
        description = self.description_category_input.text()


        # Добавление новой категории в базе данных
        try:
            conn = sqlite3.connect("store.db")
            cursor = conn.cursor()

            cursor.execute("INSERT INTO Category (Name_category, Description) VALUES (?, ?)",
                               (name_category, description))
            conn.commit()
            print(f"Категория {name_category} добавлена.")  # Отладка
            conn.close()

        except sqlite3.Error as e:
            print(f"Ошибка при подключении к базе данных: {e}")  # Отладка

    def add_products_to_warehouse(self):
        product_id_for_warehouse = self.product_id_for_warehouse_input.text()
        amount = self.amount_input.text()


        # Добавление нового товара на склад в базе данных
        try:
            conn = sqlite3.connect("store.db")
            cursor = conn.cursor()

            cursor.execute("INSERT INTO Warehouse (Product_id, Amount) VALUES (?, ?)",
                               (product_id_for_warehouse, amount))
            conn.commit()
            print(f"Товар {product_id_for_warehouse} добавлен на склад.")  # Отладка
            conn.close()

        except sqlite3.Error as e:
            print(f"Ошибка при подключении к базе данных: {e}")  # Отладка

class AddCashierWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Добавление новых кассиров и продавцов')
        self.setGeometry(100, 100, 300, 250)

        self.main_widget = QWidget()
        self.layout = QFormLayout()

        self.fio_cashier_input = QLineEdit()
        self.phone_cashier_input = QLineEdit()
        self.add_button = QPushButton('Добавить кассиров')

        self.layout.addRow("ФИО кассира:", self.fio_cashier_input)
        self.layout.addRow("Номер телефона кассира:", self.phone_cashier_input)
        self.layout.addWidget(self.add_button)

        self.add_button.clicked.connect(self.add_cashier)

        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)

        self.fio_saleman_input = QLineEdit()
        self.phone_saleman_input = QLineEdit()
        self.add_button = QPushButton('Добавить продавцов')

        self.layout.addRow("ФИО продавца:", self.fio_saleman_input)
        self.layout.addRow("Номер телефона продавца:", self.phone_saleman_input)
        self.layout.addWidget(self.add_button)

        self.add_button.clicked.connect(self.add_saleman)

        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)

    def add_cashier(self):
        fio_cashier = self.fio_cashier_input.text()
        phone_cashier = self.phone_cashier_input.text()


        # Добавление нового кассира в базе данных
        try:
            conn = sqlite3.connect("store.db")
            cursor = conn.cursor()

            cursor.execute("INSERT INTO Cashier (Fio, Phone) VALUES (?, ?)",
                               (fio_cashier, phone_cashier))
            conn.commit()
            print(f"Кассир {fio_cashier} добавлен.")  # Отладка
            conn.close()

        except sqlite3.Error as e:
            print(f"Ошибка при подключении к базе данных: {e}")  # Отладка

    def add_saleman(self):
        fio_saleman = self.fio_saleman_input.text()
        phone_saleman = self.phone_saleman_input.text()


        # Добавление нового продавца в базе данных
        try:
            conn = sqlite3.connect("store.db")
            cursor = conn.cursor()

            cursor.execute("INSERT INTO Saleman (Fio, Phone) VALUES (?, ?)",
                               (fio_saleman, phone_saleman))
            conn.commit()
            print(f"Продавец {fio_saleman} добавлен.")  # Отладка
            conn.close()

        except sqlite3.Error as e:
            print(f"Ошибка при подключении к базе данных: {e}")  # Отладка



# Запуск приложения
if __name__ == "__main__":
    create_database()  # Создаем базу данных при запуске
    app = QApplication(sys.argv)
    auth_window = AuthWindow()
    auth_window.show()
    sys.exit(app.exec())
