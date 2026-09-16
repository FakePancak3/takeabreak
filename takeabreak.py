import sys
import os
import json
import winsound

from PyQt6.QtCore import Qt, QTimer, QPoint, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor, QFont, QAction
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout,
    QSystemTrayIcon, QMenu, QGraphicsDropShadowEffect, QDialog, QSpinBox
)

BREAK_INTERVAL_MINUTES = 10
POPUP_WIDTH = 380
POPUP_HEIGHT = 150
POPUP_MARGIN = 20
FADE_IN_DURATION_MS = 300

BG_COLOR = "#161616"
ACCENT_ORANGE = "#FF6000"
TEXT_GRAY = "#9CA3AF"

SETTINGS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "takeabreak_settings.json")

MENU_STYLE = """
QMenu {
    background-color: #161616;
    color: white;
    border: 1px solid #333333;
    border-radius: 8px;
    padding: 6px;
}
QMenu::item {
    padding: 6px 20px;
    border-radius: 4px;
}
QMenu::item:selected {
    background-color: #FF6000;
    color: black;
}
QMenu::separator {
    height: 1px;
    background: #333333;
    margin: 6px 4px;
}
"""


def load_saved_minutes():
    try:
        with open(SETTINGS_FILE, "r") as f:
            data = json.load(f)
            return int(data.get("interval_minutes", BREAK_INTERVAL_MINUTES))
    except Exception:
        return BREAK_INTERVAL_MINUTES


def save_minutes(minutes):
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump({"interval_minutes": minutes}, f)
    except Exception:
        pass


def create_icon():
    size = 64
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setBrush(QColor(ACCENT_ORANGE))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawEllipse(4, 4, size - 8, size - 8)

    painter.setPen(QColor(BG_COLOR))
    painter.setFont(QFont("Arial", int(size * 0.5), QFont.Weight.Bold))
    painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "!")
    painter.end()

    return QIcon(pixmap)


class BreakPopup(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
            | Qt.WindowType.WindowDoesNotAcceptFocus
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        self.setFixedSize(POPUP_WIDTH, POPUP_HEIGHT)

        box = QWidget(self)
        box.setGeometry(0, 0, POPUP_WIDTH, POPUP_HEIGHT)
        box.setStyleSheet(
            "background-color: " + BG_COLOR + "; border-radius: 14px;"
        )

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 160))
        shadow.setOffset(0, 4)
        box.setGraphicsEffect(shadow)

        layout = QVBoxLayout(box)
        layout.setContentsMargins(18, 14, 14, 16)
        layout.setSpacing(10)

        top_row = QHBoxLayout()
        top_row.setSpacing(8)

        warning_icon = QLabel()
        warning_icon.setPixmap(create_icon().pixmap(20, 20))
        warning_icon.setFixedSize(22, 22)

        title = QLabel("Look around for a bit.")
        title.setStyleSheet("color: white; font-size: 14px; font-weight: bold; background: transparent;")

        close_button = QPushButton("\u2715")
        close_button.setCursor(Qt.CursorShape.PointingHandCursor)
        close_button.setFixedSize(24, 24)
        close_button.setStyleSheet(
            "QPushButton { color: " + ACCENT_ORANGE + "; background: transparent; border: none; font-size: 15px; font-weight: bold; }"
            "QPushButton:hover { color: #FF8A3D; }"
        )
        close_button.clicked.connect(self.close)

        top_row.addWidget(warning_icon)
        top_row.addWidget(title)
        top_row.addStretch()
        top_row.addWidget(close_button)

        message = QLabel("Give your eyes a rest. Focus on an object\nat least 20 feet away.")
        message.setWordWrap(True)
        message.setStyleSheet("color: " + TEXT_GRAY + "; font-size: 12px; background: transparent;")

        bottom_row = QHBoxLayout()
        bottom_row.addStretch()

        got_it_button = QPushButton("Got It")
        got_it_button.setCursor(Qt.CursorShape.PointingHandCursor)
        got_it_button.setFixedSize(90, 32)
        got_it_button.setStyleSheet(
            "QPushButton { background-color: " + ACCENT_ORANGE + "; color: black; font-weight: bold; font-size: 12px; border: none; border-radius: 16px; }"
            "QPushButton:hover { background-color: #FF7A24; }"
            "QPushButton:pressed { background-color: #E05500; }"
        )
        got_it_button.clicked.connect(self.close)
        bottom_row.addWidget(got_it_button)

        layout.addLayout(top_row)
        layout.addWidget(message)
        layout.addStretch()
        layout.addLayout(bottom_row)

    def play_sound(self):
        try:
            winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS | winsound.SND_ASYNC)
        except Exception:
            pass

    def show_in_corner(self):
        screen = QApplication.primaryScreen()
        area = screen.availableGeometry()
        x = area.right() - POPUP_WIDTH - POPUP_MARGIN
        y = area.bottom() - POPUP_HEIGHT - POPUP_MARGIN
        self.move(QPoint(x, y))

        self.setWindowOpacity(0.0)
        self.show()
        self.play_sound()

        self.fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self.fade_animation.setDuration(FADE_IN_DURATION_MS)
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.fade_animation.start()


class SettingsDialog(QDialog):
    def __init__(self, current_minutes):
        super().__init__()

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(320, 160)

        box = QWidget(self)
        box.setGeometry(0, 0, 320, 160)
        box.setStyleSheet(
            "background-color: " + BG_COLOR + "; border-radius: 14px;"
        )

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 160))
        shadow.setOffset(0, 4)
        box.setGraphicsEffect(shadow)

        layout = QVBoxLayout(box)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(12)

        top_row = QHBoxLayout()
        title = QLabel("Break Settings")
        title.setStyleSheet("color: white; font-size: 14px; font-weight: bold; background: transparent;")

        close_button = QPushButton("\u2715")
        close_button.setCursor(Qt.CursorShape.PointingHandCursor)
        close_button.setFixedSize(24, 24)
        close_button.setStyleSheet(
            "QPushButton { color: " + ACCENT_ORANGE + "; background: transparent; border: none; font-size: 15px; font-weight: bold; }"
            "QPushButton:hover { color: #FF8A3D; }"
        )
        close_button.clicked.connect(self.reject)

        top_row.addWidget(title)
        top_row.addStretch()
        top_row.addWidget(close_button)

        label = QLabel("Break interval (minutes):")
        label.setStyleSheet("color: " + TEXT_GRAY + "; font-size: 12px; background: transparent;")

        self.spin_box = QSpinBox()
        self.spin_box.setMinimum(1)
        self.spin_box.setMaximum(1440)
        self.spin_box.setValue(current_minutes)
        self.spin_box.setStyleSheet(
            "QSpinBox { background-color: #232323; color: white; border: 1px solid #333; border-radius: 6px; padding: 6px; }"
        )

        bottom_row = QHBoxLayout()
        bottom_row.addStretch()

        save_button = QPushButton("Save")
        save_button.setCursor(Qt.CursorShape.PointingHandCursor)
        save_button.setFixedSize(90, 32)
        save_button.setStyleSheet(
            "QPushButton { background-color: " + ACCENT_ORANGE + "; color: black; font-weight: bold; font-size: 12px; border: none; border-radius: 16px; }"
            "QPushButton:hover { background-color: #FF7A24; }"
            "QPushButton:pressed { background-color: #E05500; }"
        )
        save_button.clicked.connect(self.accept)
        bottom_row.addWidget(save_button)

        layout.addLayout(top_row)
        layout.addWidget(label)
        layout.addWidget(self.spin_box)
        layout.addStretch()
        layout.addLayout(bottom_row)

    def get_minutes(self):
        return self.spin_box.value()


class TakeABreakApp:
    def __init__(self, app):
        self.app = app
        self.app.setQuitOnLastWindowClosed(False)

        self.interval_minutes = load_saved_minutes()
        self.popup = None
        self.icon = create_icon()

        self.tray_icon = QSystemTrayIcon(self.icon, self.app)
        self.tray_icon.setToolTip("TakeABreak")

        menu = QMenu()
        menu.setStyleSheet(MENU_STYLE)

        trigger_action = QAction("Trigger Break Now", menu)
        trigger_action.triggered.connect(self.show_popup)
        menu.addAction(trigger_action)

        settings_action = QAction("Settings", menu)
        settings_action.triggered.connect(self.open_settings)
        menu.addAction(settings_action)

        menu.addSeparator()

        quit_action = QAction("Quit", menu)
        quit_action.triggered.connect(self.quit_app)
        menu.addAction(quit_action)

        self.tray_icon.setContextMenu(menu)
        self.tray_icon.show()

        self.timer = QTimer()
        self.timer.timeout.connect(self.show_popup)
        self.timer.start(self.interval_minutes * 60 * 1000)

        QTimer.singleShot(500, self.show_startup_message)

    def show_startup_message(self):
        self.tray_icon.showMessage(
            "TakeABreak",
            "TakeABreak is running",
            QSystemTrayIcon.MessageIcon.Information,
            3000,
        )

    def show_popup(self):
        if self.popup is not None and self.popup.isVisible():
            self.popup.close()

        self.popup = BreakPopup()
        self.popup.show_in_corner()

    def open_settings(self):
        dialog = SettingsDialog(self.interval_minutes)
        if dialog.exec():
            self.interval_minutes = dialog.get_minutes()
            save_minutes(self.interval_minutes)
            self.timer.stop()
            self.timer.start(self.interval_minutes * 60 * 1000)

    def quit_app(self):
        self.tray_icon.hide()
        self.app.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    if not QSystemTrayIcon.isSystemTrayAvailable():
        sys.exit(1)

    take_a_break = TakeABreakApp(app)
    sys.exit(app.exec())
