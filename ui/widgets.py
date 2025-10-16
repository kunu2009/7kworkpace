"""
UI Widgets and Components
"""

from PyQt6.QtWidgets import QPushButton, QFrame, QLabel, QCalendarWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor


class RoundedButton(QPushButton):
    """Custom rounded button"""
    def __init__(self, text=""):
        super().__init__(text)
        self.setMinimumHeight(40)
        self.setCursor(Qt.CursorShape.PointingHandCursor)


class StatsCard(QFrame):
    """Statistics card widget"""
    def __init__(self, title, value, icon=""):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                border: 2px solid #e0e7ff;
            }
        """)
        self.setMinimumHeight(120)
        
        from PyQt6.QtWidgets import QVBoxLayout
        layout = QVBoxLayout(self)
        
        title_label = QLabel(f"{icon} {title}")
        title_label.setStyleSheet("color: #666; font-size: 12px; font-weight: bold;")
        layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setStyleSheet("color: #667eea; font-size: 24px; font-weight: bold;")
        layout.addWidget(value_label)


class FileCard(QFrame):
    """File card widget"""
    def __init__(self, filename, path):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 5px;
                border: 1px solid #e0e7ff;
            }
        """)
        self.setMinimumHeight(80)
        
        from PyQt6.QtWidgets import QVBoxLayout
        layout = QVBoxLayout(self)
        
        name_label = QLabel(filename)
        name_label.setStyleSheet("color: #333; font-weight: bold;")
        layout.addWidget(name_label)
        
        path_label = QLabel(path)
        path_label.setStyleSheet("color: #999; font-size: 10px;")
        layout.addWidget(path_label)


class NoteCard(QFrame):
    """Note card widget"""
    def __init__(self, text, timestamp=""):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background-color: #fffacd;
                border-radius: 5px;
                border: 1px solid #f0e68c;
            }
        """)
        self.setMinimumHeight(100)
        
        from PyQt6.QtWidgets import QVBoxLayout
        layout = QVBoxLayout(self)
        
        note_label = QLabel(text)
        note_label.setStyleSheet("color: #333; font-size: 12px;")
        note_label.setWordWrap(True)
        layout.addWidget(note_label)
        
        if timestamp:
            time_label = QLabel(timestamp)
            time_label.setStyleSheet("color: #999; font-size: 10px;")
            layout.addWidget(time_label)


class CustomCalendar(QCalendarWidget):
    """Custom styled calendar"""
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QCalendarWidget {
                background-color: white;
                border: 2px solid #e0e7ff;
                border-radius: 5px;
            }
        """)


class GradientFrame(QFrame):
    """Frame with gradient background"""
    def __init__(self, color1="#667eea", color2="#764ba2"):
        super().__init__()
        self.color1 = color1
        self.color2 = color2
        self.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {color1}, stop:1 {color2});
                border-radius: 10px;
            }}
        """)
        self.setMinimumHeight(100)
