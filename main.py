import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QLineEdit, QPushButton, QBoxLayout, QHBoxLayout

conn = sqlite3.connect("cars_db.db")
cursor = conn.cursor()
cursor.execute("""
        CREATE TABLE IF NOT EXISTS cars(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            car_number TEXT,
            brand TEXT,
            model TEXT,
            year INTEGER,
            mileage INTEGER,
            owners INTEGER
        )    
    """)
cars_data = [
    ('A001AA', 'Toyota', 'Land Cruiser', 2020, 50000, 10),
    ('B201CA', 'Toyota', 'Cumry', 2016, 250000, 1),
    ('E071BA', 'Audi', 'A6 Long', 2018, 150000, 5),
    ('E031EE', 'VAZ', '2107', 2008, 345000, 12),
    ('H501MA', 'lada', 'X-ray', 2019, 115000, 3),
    ('B401AA', 'BMW', 'M3', 1999, 2250000, 10),
    ('T602BA', 'Ford', 'F-150', 2020, 470000, 6),
    ('N111AA', 'Lamborghini', 'Gallardo', 2024, 40000, 1),

]

cursor.executemany('INSERT INTO cars (car_number,brand,model,year,mileage,owners) VALUES(?,?,?,?,?,?)', cars_data)
conn.commit()
conn.close()


class CarInfoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.label = QLabel("Enter nuber of car: ", self)
        self.line_edit = QLineEdit(self)
        self.button = QPushButton('Search', self)
        self.info_label = QLabel('',self)
        self.button.clicked.connect(self.on_click)
        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.line_edit)
        layout.addWidget(self.button)
        layout.addWidget(self.info_label)
        self.setLayout(layout)
        self.setWindowTitle("Search engine auto")
        self.show()

    def on_click(self):
        car_number = self.line_edit.text()
        conn = sqlite3.connect('cars_db.db')
        cursor = conn.cursor()
        # Поиск авто в базе
        cursor.execute("SELECT * FROM cars WHERE car_number =? ", (car_number,))
        car_info = cursor.fetchone()

        if car_info:
            info = f"brand:{car_info[2]}, model:{car_info[3]}, year:{car_info[4]}"
        else:
            info = "information about car not found"

        self.info_label.setText(info)
        conn.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = CarInfoApp()
    sys.exit(app.exec_())

