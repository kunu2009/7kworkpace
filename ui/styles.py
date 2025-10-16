"""
Stylesheet definitions for the application
Supports both light and dark themes
"""

def get_stylesheet(dark_mode=False):
    """Get stylesheet based on theme preference"""
    if dark_mode:
        return get_dark_stylesheet()
    return get_light_stylesheet()

def get_light_stylesheet():
    """Light theme stylesheet"""
    return """
    QMainWindow {
        background-color: #f5f7fa;
    }
    
    QLabel {
        color: #333;
    }
    
    QPushButton {
        background-color: #667eea;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 8px 16px;
        font-weight: bold;
        font-size: 12px;
    }
    
    QPushButton:hover {
        background-color: #764ba2;
    }
    
    QPushButton:pressed {
        background-color: #5568d3;
    }
    
    QLineEdit, QTextEdit, QPlainTextEdit {
        background-color: white;
        border: 2px solid #e0e7ff;
        border-radius: 5px;
        padding: 8px;
        color: #333;
        selection-background-color: #667eea;
        font-size: 11px;
    }
    
    QListWidget {
        border: 2px solid #e0e7ff;
        border-radius: 5px;
        background-color: white;
        color: #333;
    }
    
    QListWidget::item {
        padding: 8px;
        color: #333;
    }
    
    QListWidget::item:selected {
        background-color: #e0e7ff;
    }
    
    QCalendarWidget {
        background-color: #2d2d2d;
        color: #e0e0e0;
        border: 2px solid #667eea;
        border-radius: 5px;
    }
    
    QCalendarWidget QAbstractItemView {
        background-color: #1e1e1e;
        color: #e0e0e0;
        selection-background-color: #667eea;
        border: none;
    }
    
    QCalendarWidget QHeaderView::section {
        background-color: #333;
        color: #e0e0e0;
        padding: 5px;
        border: 1px solid #444;
        font-weight: bold;
    }
    
    QCalendarWidget QSpinBox {
        background-color: #333;
        color: #e0e0e0;
        border: 1px solid #667eea;
        border-radius: 3px;
        padding: 3px;
    }
    
    QCalendarWidget QSpinBox::up-button,
    QCalendarWidget QSpinBox::down-button {
        background-color: #667eea;
        color: white;
        border-radius: 3px;
    }
    
    QCalendarWidget QToolButton {
        background-color: #667eea;
        color: white;
        border: none;
        border-radius: 3px;
        padding: 4px 8px;
        font-weight: bold;
    }
    
    QCalendarWidget QToolButton:hover {
        background-color: #764ba2;
    }
    
    QCalendarWidget QToolButton:pressed {
        background-color: #5568d3;
    }
    
    QTabWidget::pane {
        border: none;
        background-color: #f5f7fa;
    }
    
    QTabBar::tab {
        background-color: #e0e7ff;
        color: #333;
        padding: 10px 20px;
        margin-right: 2px;
        border-radius: 4px;
        font-weight: bold;
    }
    
    QTabBar::tab:selected {
        background-color: #667eea;
        color: white;
    }
    
    QScrollBar:vertical {
        background-color: #f5f7fa;
        width: 12px;
        border-radius: 6px;
    }
    
    QScrollBar::handle:vertical {
        background-color: #ccc;
        border-radius: 6px;
        min-height: 20px;
    }
    
    QScrollBar::handle:vertical:hover {
        background-color: #999;
    }
    
    QFrame {
        color: #333;
        background-color: transparent;
    }
    
    QTableWidget {
        background-color: white;
        color: #333;
        border: 2px solid #e0e7ff;
        gridline-color: #e0e7ff;
    }
    
    QTableWidget::item {
        background-color: white;
        color: #333;
        padding: 4px;
    }
    
    QTableWidget::item:selected {
        background-color: #667eea;
        color: white;
    }
    
    QHeaderView::section {
        background-color: #e0e7ff;
        color: #333;
        padding: 5px;
        border: 1px solid #ccc;
        font-weight: bold;
    }
    
    QComboBox {
        background-color: white;
        color: #333;
        border: 2px solid #e0e7ff;
        border-radius: 5px;
        padding: 5px;
    }
    
    QComboBox::drop-down {
        border: none;
        background-color: #667eea;
    }
    
    QComboBox QAbstractItemView {
        background-color: white;
        color: #333;
        selection-background-color: #667eea;
    }
    
    QSpinBox, QDoubleSpinBox {
        background-color: white;
        color: #333;
        border: 2px solid #e0e7ff;
        border-radius: 5px;
        padding: 5px;
    }
    
    QSpinBox::up-button, QSpinBox::down-button,
    QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
        background-color: #667eea;
        color: white;
        border: none;
    }
    
    QCheckBox {
        color: #333;
        background-color: transparent;
    }
    
    QCheckBox::indicator {
        width: 18px;
        height: 18px;
        background-color: white;
        border: 2px solid #e0e7ff;
        border-radius: 3px;
    }
    
    QCheckBox::indicator:checked {
        background-color: #667eea;
        border: 2px solid #667eea;
    }
    
    QProgressBar {
        background-color: #f0f0f0;
        border: 2px solid #e0e7ff;
        border-radius: 5px;
        text-align: center;
        color: #333;
    }
    
    QProgressBar::chunk {
        background-color: #667eea;
        border-radius: 3px;
    }
    
    QTreeWidget {
        background-color: white;
        color: #333;
        border: 2px solid #e0e7ff;
        gridline-color: #e0e7ff;
    }
    
    QTreeWidget::item {
        padding: 4px;
    }
    
    QTreeWidget::item:selected {
        background-color: #667eea;
        color: white;
    }
    
    QDialog {
        background-color: #f5f7fa;
        color: #333;
    }
    
    QMessageBox {
        background-color: #f5f7fa;
    }
    
    QMessageBox QLabel {
        color: #333;
    }
    
    QMenuBar {
        background-color: white;
        color: #333;
        border-bottom: 1px solid #e0e7ff;
    }
    
    QMenuBar::item:selected {
        background-color: #667eea;
        color: white;
    }
    
    QMenu {
        background-color: white;
        color: #333;
        border: 1px solid #e0e7ff;
    }
    
    QMenu::item:selected {
        background-color: #667eea;
        color: white;
    }
    
    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
        border: 2px solid #667eea;
    }
    
    QLabel {
        background-color: transparent;
    }
    
    QWidget {
        background-color: #f5f7fa;
        color: #333;
    }
    
    QScrollBar:horizontal {
        background-color: #f5f7fa;
        height: 12px;
        border-radius: 6px;
    }
    
    QScrollBar::handle:horizontal {
        background-color: #ccc;
        border-radius: 6px;
        min-width: 20px;
    }
    
    QScrollBar::handle:horizontal:hover {
        background-color: #999;
    }
    
    QTabBar::tab:hover:!selected {
        background-color: #d0d7ff;
    }
    """

def get_dark_stylesheet():
    """Dark theme stylesheet"""
    return """
    QMainWindow {
        background-color: #1e1e1e;
    }
    
    QWidget {
        background-color: #1e1e1e;
        color: #e0e0e0;
    }
    
    QLabel {
        color: #e0e0e0;
        background-color: transparent;
    }
    
    QPushButton {
        background-color: #667eea;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 8px 16px;
        font-weight: bold;
        font-size: 12px;
    }
    
    QPushButton:hover {
        background-color: #764ba2;
    }
    
    QPushButton:pressed {
        background-color: #5568d3;
    }
    
    QLineEdit, QTextEdit, QPlainTextEdit {
        background-color: #2d2d2d;
        border: 2px solid #444;
        border-radius: 5px;
        padding: 8px;
        color: #e0e0e0;
        selection-background-color: #667eea;
        font-size: 11px;
    }
    
    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
        border: 2px solid #667eea;
    }
    
    QListWidget {
        border: 2px solid #444;
        border-radius: 5px;
        background-color: #2d2d2d;
        color: #e0e0e0;
    }
    
    QListWidget::item {
        padding: 8px;
        color: #e0e0e0;
        background-color: #333;
    }
    
    QListWidget::item:selected {
        background-color: #667eea;
        color: white;
    }
    
    QTableWidget {
        background-color: #2d2d2d;
        color: #e0e0e0;
        border: 2px solid #444;
        gridline-color: #444;
    }
    
    QTableWidget::item {
        background-color: #2d2d2d;
        color: #e0e0e0;
        padding: 4px;
    }
    
    QTableWidget::item:selected {
        background-color: #667eea;
        color: white;
    }
    
    QHeaderView::section {
        background-color: #333;
        color: #e0e0e0;
        padding: 5px;
        border: 1px solid #444;
        font-weight: bold;
    }
    
    QComboBox {
        background-color: #2d2d2d;
        color: #e0e0e0;
        border: 2px solid #444;
        border-radius: 5px;
        padding: 5px;
    }
    
    QComboBox::drop-down {
        border: none;
        background-color: #667eea;
    }
    
    QComboBox QAbstractItemView {
        background-color: #2d2d2d;
        color: #e0e0e0;
        selection-background-color: #667eea;
    }
    
    QSpinBox, QDoubleSpinBox {
        background-color: #2d2d2d;
        color: #e0e0e0;
        border: 2px solid #444;
        border-radius: 5px;
        padding: 5px;
    }
    
    QSpinBox::up-button, QSpinBox::down-button,
    QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
        background-color: #667eea;
        color: white;
        border: none;
    }
    
    QCheckBox {
        color: #e0e0e0;
        background-color: transparent;
    }
    
    QCheckBox::indicator {
        width: 18px;
        height: 18px;
        background-color: #2d2d2d;
        border: 2px solid #444;
        border-radius: 3px;
    }
    
    QCheckBox::indicator:checked {
        background-color: #667eea;
        border: 2px solid #667eea;
    }
    
    QProgressBar {
        background-color: #2d2d2d;
        border: 2px solid #444;
        border-radius: 5px;
        text-align: center;
        color: #e0e0e0;
    }
    
    QProgressBar::chunk {
        background-color: #667eea;
        border-radius: 3px;
    }
    
    QTreeWidget {
        background-color: #2d2d2d;
        color: #e0e0e0;
        border: 2px solid #444;
        gridline-color: #444;
    }
    
    QTreeWidget::item {
        padding: 4px;
    }
    
    QTreeWidget::item:selected {
        background-color: #667eea;
        color: white;
    }
    
    QCalendarWidget {
        background-color: #2d2d2d;
        color: #e0e0e0;
        border: 2px solid #667eea;
        border-radius: 5px;
    }
    
    QCalendarWidget QAbstractItemView {
        background-color: #1e1e1e;
        color: #e0e0e0;
        selection-background-color: #667eea;
        border: none;
    }
    
    QCalendarWidget QHeaderView::section {
        background-color: #333;
        color: #e0e0e0;
        padding: 5px;
        border: 1px solid #444;
        font-weight: bold;
    }
    
    QCalendarWidget QSpinBox {
        background-color: #333;
        color: #e0e0e0;
        border: 1px solid #667eea;
        border-radius: 3px;
        padding: 3px;
    }
    
    QCalendarWidget QSpinBox::up-button,
    QCalendarWidget QSpinBox::down-button {
        background-color: #667eea;
        color: white;
        border-radius: 3px;
    }
    
    QCalendarWidget QToolButton {
        background-color: #667eea;
        color: white;
        border: none;
        border-radius: 3px;
        padding: 4px 8px;
        font-weight: bold;
    }
    
    QCalendarWidget QToolButton:hover {
        background-color: #764ba2;
    }
    
    QCalendarWidget QToolButton:pressed {
        background-color: #5568d3;
    }
    
    QTabWidget::pane {
        border: none;
        background-color: #1e1e1e;
    }
    
    QTabBar::tab {
        background-color: #333;
        color: #e0e0e0;
        padding: 10px 20px;
        margin-right: 2px;
        border-radius: 4px;
        font-weight: bold;
    }
    
    QTabBar::tab:selected {
        background-color: #667eea;
        color: white;
    }
    
    QTabBar::tab:hover:!selected {
        background-color: #444;
    }
    
    QScrollBar:vertical {
        background-color: #1e1e1e;
        width: 12px;
        border-radius: 6px;
    }
    
    QScrollBar::handle:vertical {
        background-color: #555;
        border-radius: 6px;
        min-height: 20px;
    }
    
    QScrollBar::handle:vertical:hover {
        background-color: #666;
    }
    
    QScrollBar:horizontal {
        background-color: #1e1e1e;
        height: 12px;
        border-radius: 6px;
    }
    
    QScrollBar::handle:horizontal {
        background-color: #555;
        border-radius: 6px;
        min-width: 20px;
    }
    
    QScrollBar::handle:horizontal:hover {
        background-color: #666;
    }
    
    QFrame {
        background-color: #2d2d2d;
        color: #e0e0e0;
    }
    
    QDialog {
        background-color: #1e1e1e;
        color: #e0e0e0;
    }
    
    QMessageBox {
        background-color: #1e1e1e;
    }
    
    QMessageBox QLabel {
        color: #e0e0e0;
    }
    
    QMenuBar {
        background-color: #2d2d2d;
        color: #e0e0e0;
        border-bottom: 1px solid #444;
    }
    
    QMenuBar::item:selected {
        background-color: #667eea;
        color: white;
    }
    
    QMenu {
        background-color: #2d2d2d;
        color: #e0e0e0;
        border: 1px solid #444;
    }
    
    QMenu::item:selected {
        background-color: #667eea;
        color: white;
    }
    """
