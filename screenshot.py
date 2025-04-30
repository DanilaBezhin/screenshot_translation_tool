import sys
import datetime
import threading
import keyboard
from queue import Queue
from PyQt5.QtCore import Qt, QRect, QTimer
from PyQt5.QtGui import QPainter, QColor, QGuiApplication
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel

task_queue = Queue()

class OverlayWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.start_point = None
        self.end_point = None
        self.selected_rect = None
        self.initial_screen_shown = True

    def setup_ui(self) -> None:
        """Настройка пользовательского интерфейса окна."""
        screen_size = QGuiApplication.primaryScreen().size()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowTransparentForInput)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(0, 0, screen_size.width(), screen_size.height())
        self.show_initial_screen()

    def show_initial_screen(self) -> None:
        """Показ начального экрана с инструкцией."""
        self.initial_label = QLabel(">> Выделите область, чтобы сделать скриншот <<", self)
        self.initial_label.setGeometry(self.rect())
        self.initial_label.setAlignment(Qt.AlignCenter)
        self.initial_label.setStyleSheet("background-color: rgba(128, 128, 128, 150); color: white; font-size: 28px; font-weight: 500;")
        self.initial_label.show()

    def hide_initial_screen(self) -> None:
        """Скрытие начального экрана."""
        self.initial_label.hide()

    def mousePressEvent(self, event) -> None:
        """Начало выделения области."""
        if self.initial_screen_shown:
            self.hide_initial_screen()
            self.initial_screen_shown = False
        self.start_point = event.pos()
        self.end_point = self.start_point
        self.update()

    def mouseMoveEvent(self, event) -> None:
        """Обновление выделенной области при движении мыши."""
        if self.start_point:
            self.end_point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event) -> None:
        """Завершение выделения и создание скриншота."""
        if self.start_point and self.end_point:
            self.selected_rect = QRect(self.start_point, self.end_point).normalized()
            self.save_screenshot()
            QApplication.instance().quit()

    def save_screenshot(self) -> None:
        """Создание и сохранение скриншота выделенной области."""
        screen = QGuiApplication.primaryScreen()
        cropped_pixmap = screen.grabWindow(0).copy(self.selected_rect)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_short = f"screenshot_{timestamp}.png"
        filename = f"{sys.path[0]}/{file_short}"
        cropped_pixmap.save(filename)

        task_queue.put(file_short)

    def paintEvent(self, event) -> None:
        """Отрисовка выделенной области."""
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 0))

        if self.start_point and self.end_point:
            rect = QRect(self.start_point, self.end_point).normalized()
            self.draw_overlay(painter, rect)

    def draw_overlay(self, painter, rect) -> None:
        """Отрисовка фона и выделенного прямоугольника."""
        fill_color = QColor(128, 128, 128, 150)
        painter.setPen(Qt.NoPen)
        painter.setBrush(fill_color)

        painter.drawRect(0, 0, self.width(), rect.top())
        painter.drawRect(0, rect.top(), rect.left(), rect.height())
        painter.drawRect(0, rect.bottom() + 1, self.width(), self.height() - rect.bottom() - 1)
        painter.drawRect(rect.right(), rect.top(), self.width() - rect.right(), rect.height())

        painter.setBrush(QColor(255, 255, 255, 0))
        painter.drawRect(rect)


class ScreenshotApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.overlay = OverlayWindow()
        self.overlay.showFullScreen()
        self.showFullScreen()
        self.setMouseTracking(True)

    def setup_ui(self) -> None:
        """Настройка пользовательского интерфейса основного окна."""
        self.setWindowTitle("Screenshot Tool")
        self.setWindowOpacity(0.01)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        screen_size = QGuiApplication.primaryScreen().size()
        self.setGeometry(0, 0, screen_size.width(), screen_size.height())

    def mousePressEvent(self, event) -> None:
        self.overlay.mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:
        self.overlay.mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        self.overlay.mouseReleaseEvent(event)


def launch_screenshot_app() -> None:
    """Запуск PyQt приложения для создания скриншота."""
    app = QApplication(sys.argv)
    window = ScreenshotApp()
    app.exec_()


def main() -> None:
    """Функция для отслеживания сочетания клавиш и запуска приложения."""
    while True:
        keyboard.wait('ctrl+alt+w')
        screenshot_thread = threading.Thread(target=launch_screenshot_app)
        screenshot_thread.start()
