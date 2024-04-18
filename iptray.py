# py
import sys
import threading
import time
from urllib import request

# qt
from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon, QMainWindow, QLabel
from PySide6.QtGui import QIcon, QGuiApplication

public_ip = 'loading..'

app = QApplication([])

# daemon thread
class Daemon(threading.Thread):
    def __init__(self, tray, refresh_interval):
        super().__init__(target=self.ip_daemon)
        self.tray = tray
        self.refresh_interval = refresh_interval
        self.daemon = True
        self.start()

    def get_public_ip(self):
        try:
            req = request.Request('https://api.ipify.org/')
            response = request.urlopen(req)
            if response.status == 200:
                return response.read().decode('utf-8')
            else:
                return ''
        except Exception as e:
            print(e)
            return 'ERROR'

    def ip_daemon(self):
        global public_ip
        while True:
            public_ip = self.get_public_ip()
            self.tray.setToolTip(public_ip)
            time.sleep(self.refresh_interval)  # Sleep

class App(QMainWindow):
    def __init__(self):
        global app
        super().__init__()

        self.icon = QIcon('icon.ico')

        self.setWindowTitle("Ip Tray")
        self.setWindowIcon(self.icon)

        self.label = QLabel("OCD inducing text")
        self.setCentralWidget(self.label)

        self.init_tray()
        self.clipboard = QGuiApplication.clipboard()
        self.ip_daemon = Daemon(self.tray, 900)
        sys.exit(app.exec())

    def on_tray_click(self, event):
        global public_ip
        if event == QSystemTrayIcon.ActivationReason.Trigger:
            self.clipboard.setText(public_ip)
        elif event == QSystemTrayIcon.ActivationReason.DoubleClick:
            if self.isVisible():
                self.activateWindow()
                self.raise_()
            else:
                self.show()

    def init_tray(self):
        global app

        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(self.icon)
        self.tray.setVisible(True)
        self.tray.setToolTip("fetching ip...")
        self.tray.activated.connect(self.on_tray_click)
        tray_menu = QMenu()
        quit_action = tray_menu.addAction("Quit")

        quit_action.triggered.connect(app.quit)

        self.tray.setContextMenu(tray_menu)

    def closeEvent(self, event):
        self.hide()
        event.ignore()

    def button_clicked(self):
        print("Button clicked!")

App()