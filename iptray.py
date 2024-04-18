# py
import sys
import threading
import time
from urllib import request

# qt
from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon, QMainWindow
from PySide6.QtGui import QIcon, QGuiApplication

# daemon thread
public_ip = 'Loading...'

def get_public_ip():
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

def fetch_ip_daemon():
    global public_ip
    global tray_icon
    while True:
        public_ip = get_public_ip()
        tray_icon.setToolTip(public_ip)
        time.sleep(900)  # Sleep

daemon_thread = threading.Thread(target=fetch_ip_daemon)
daemon_thread.daemon = True
daemon_thread.start()


# qt app
app = QApplication(sys.argv)
clipboard = QGuiApplication.clipboard()

# tray icon
tray_icon = QSystemTrayIcon()
tray_icon.setIcon(QIcon('icon.ico'))
tray_icon.setVisible(True)
tray_icon.setToolTip("fetching ip...")

class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Auto Minimize to Tray Example")
        self.setWindowIcon(QIcon('icon.ico'))  # Replace 'icon.ico' with your own icon file

        self.button = QPushButton("Click me", self)
        self.button.clicked.connect(self.button_clicked)
        self.setCentralWidget(self.button)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon('icon.ico'))
        self.tray_icon.setVisible(True)
        self.tray_icon.setToolTip("My Tray Icon App")

        self.show()

    def closeEvent(self, event):
        self.hide()  # Hide the main window instead of closing it
        event.ignore()  # Prevent the close event from closing the application

    def button_clicked(self):
        print("Button clicked!")

menu = QMenu()
# show_action = menu.addAction("Show Message")
quit_action = menu.addAction("Quit")

quit_action.triggered.connect(app.quit)

def click_action_handler():
    global public_ip
    clipboard.setText(public_ip)

tray_icon.activated.connect(click_action_handler)

tray_icon.setContextMenu(menu)

sys.exit(app.exec())