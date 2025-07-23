from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QVBoxLayout, QWidget, QPushButton, QMenu, QSystemTrayIcon
from PyQt6.QtCore import QTime, QTimer, Qt, QDate, QSettings
from PyQt6.QtGui import QFont, QCursor, QFontDatabase, QIcon, QAction
import sys, os



class Clocks(QMainWindow):
    def __init__(self):
        super().__init__()
        self.time_label = QLabel()
        self.fonts = [
            ("fonts/LOV.otf", 36),
            ("fonts/awd.otf", 60),
            ("fonts/BTTF.ttf", 46)
        ]
        
        self.font_index = 0
        self.load_fonts(self.font_index)

        self.settings = QSettings("Sckrich", "GothicClocks")
        saved_pos = self.settings.value("window_position")
        if saved_pos:  
            self.move(saved_pos)
        else:
            self.setGeometry(100, 100, 400, 80)

        self.setWindowTitle("My timer")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("icon1.ico")) 
        
        tray_menu = QMenu()
        open_action = tray_menu.addAction("Открыть")
        open_action.triggered.connect(self.show)
        exit_action = tray_menu.addAction("Выход")
        exit_action.triggered.connect(self.close_app)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
    
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        self.hide()

        
        self.time_label.setStyleSheet(
            """
            color: white
            """
        )
        self.setCursor(QCursor(Qt.CursorShape.OpenHandCursor))
        self.time_label.setFont(self.font)
        
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, False)
        self.setWindowFlag(Qt.WindowType.WindowDoesNotAcceptFocus, False)
        self.setWindowFlag(Qt.WindowType.X11BypassWindowManagerHint, False)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, True)
        self.setWindowFlag(Qt.WindowType.Tool, True)
        app.setQuitOnLastWindowClosed(False)
        
        layout = QVBoxLayout()
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.time_label)
        self.setLayout(layout)
        self.setCentralWidget(self.time_label)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        
        self.update_time()
        
        self.chosen_font = 0
        self.color = "white"
    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            if self.isVisible():
                self.hide()
            else:
                self.show()

    def load_fonts(self, font_index):
        if getattr(sys, 'frozen', False):  
            base_dir = sys._MEIPASS
        else:  
            base_dir = os.path.dirname(__file__)
        
        font_path, size = self.fonts[font_index]
        full_path = os.path.join(base_dir, font_path)  
        
        font_id = QFontDatabase.addApplicationFont(full_path)
        if font_id == -1:
            print(f"Error font loading: {full_path}")
        else:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            self.font = QFont(font_family, size)
            self.time_label.setFont(self.font)

    def update_time(self):
        current_time1 = QTime.currentTime().toString("hh:mm:ss\n")
        current_date = QDate.currentDate()
        current_time = current_time1 + current_date.toString()
        self.time_label.setText(current_time)

    def close_app(self):
        self.settings.setValue("window_position", self.pos())
        self.tray_icon.hide()
        QApplication.quit()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            self.setCursor(QCursor(Qt.CursorShape.ClosedHandCursor)) 
        elif event.button() == Qt.MouseButton.RightButton:
            self.drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            if self.color == "white":
                self.time_label.setStyleSheet(
                    """
                    color: black
                    """)
                self.color = "black"
            else:
                self.time_label.setStyleSheet(
                    """
                    color: white
                    """
                )
                self.color = "white"
            self.setCursor(QCursor(Qt.CursorShape.ClosedHandCursor)) 
        elif event.button() == Qt.MouseButton.MiddleButton:
            self.font_index = (self.font_index + 1) % len(self.fonts)
            self.load_fonts(self.font_index)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self.drag_pos:
            self.move(event.globalPosition().toPoint() - self.drag_pos)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.drag_pos = None
        self.setCursor(QCursor(Qt.CursorShape.OpenHandCursor))  
        self.settings.setValue("window_position", self.pos())
        super().mouseReleaseEvent(event)

app = QApplication(sys.argv)
clock = Clocks()
clock.show()
sys.exit(app.exec())
