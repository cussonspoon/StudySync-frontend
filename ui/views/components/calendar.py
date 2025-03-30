from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QGridLayout,
    QVBoxLayout, QHBoxLayout
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont, QPalette, QColor
import sys


class CalendarWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calendar UI")
        self.setFixedSize(300, 400)
        self.current_date = QDate.currentDate()
        self.init_ui()

    def init_ui(self):
        # Set white background
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("white"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        main_layout = QVBoxLayout()

        # Month-Year Header
        header_layout = QHBoxLayout()
        self.prev_btn = QPushButton("▲")
        self.next_btn = QPushButton("▼")
        self.prev_btn.setFixedSize(20, 20)
        self.next_btn.setFixedSize(20, 20)
        self.month_label = QLabel()
        self.month_label.setAlignment(Qt.AlignCenter)
        self.month_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.month_label.setStyleSheet("color: black; font-size: 14px;")
        header_layout.addWidget(self.prev_btn)
        header_layout.addWidget(self.month_label, stretch=1)
        header_layout.addWidget(self.next_btn)
        self.prev_btn.setStyleSheet("color: black; font-size: 14px;")
        self.next_btn.setStyleSheet("color: black; font-size: 14px;")

        # Day Grid
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(5)

        # Connect signals
        self.prev_btn.clicked.connect(self.prev_month)
        self.next_btn.clicked.connect(self.next_month)

        main_layout.addLayout(header_layout)
        main_layout.addLayout(self.grid_layout)
        self.setLayout(main_layout)

        self.update_calendar()

    def update_calendar(self):
        # Clear grid
        for i in reversed(range(self.grid_layout.count())):
            self.grid_layout.itemAt(i).widget().setParent(None)

        # Set month-year label
        self.month_label.setText(self.current_date.toString("MMMM yyyy"))

        # Weekday headers
        weekdays = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
        for col, day in enumerate(weekdays):
            label = QLabel(day)
            label.setAlignment(Qt.AlignCenter)
            label.setFont(QFont("Arial", 8))
            label.setStyleSheet("color: black; font-size: 14px;")
            label.setFixedSize(40, 40)
            self.grid_layout.addWidget(label, 0, col)

        # Days
        first_day = QDate(self.current_date.year(), self.current_date.month(), 1)
        start_col = (first_day.dayOfWeek() % 7)
        days_in_month = first_day.daysInMonth()

        row = 1
        col = start_col
        for day in range(1, days_in_month + 1):
            day_label = QLabel(str(day))
            day_label.setAlignment(Qt.AlignCenter)
            day_label.setFont(QFont("Arial", 8))
            day_label.setFixedSize(40, 40) 
            if (day == QDate.currentDate().day()
                    and self.current_date.month() == QDate.currentDate().month()
                    and self.current_date.year() == QDate.currentDate().year()):
                day_label.setStyleSheet(
                    "background-color: teal; color: black; border-radius: 20px; font-size: 14px;"
                )
            else:
                day_label.setStyleSheet("color: black; font-size: 14px;")
            self.grid_layout.addWidget(day_label, row, col)
            col += 1
            if col > 6:
                col = 0
                row += 1

    def prev_month(self):
        self.current_date = self.current_date.addMonths(-1)
        self.update_calendar()

    def next_month(self):
        self.current_date = self.current_date.addMonths(1)
        self.update_calendar()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalendarWidget()
    window.show()
    sys.exit(app.exec())
