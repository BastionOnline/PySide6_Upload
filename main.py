from PySide6.QtCore import QObject, Slot, QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebChannel import QWebChannel
import tempfile, pathlib
import os
import sys
from PySide6.QtWidgets import QApplication # QApplication → runs the GUI event loop


# Assume 'view' is your QWebEngineView instance
class Backend(QObject):

    def __init__(self, view):
        super().__init__()
        self.view = view
        # Connect downloadRequested here once
        self.view.page().profile().downloadRequested.connect(self.handle_download)

    @Slot()
    def downloadThankYouFile(self):
        thank_you_text = "Thank you for uploading your file!"
        temp_file = pathlib.Path(tempfile.gettempdir()) / "thank_you.txt"
        temp_file.write_text(thank_you_text, encoding="utf-8")

        # Trigger download by creating a QUrl and passing to the page's profile
        
        self.view.page().profile().download(QUrl.fromLocalFile(str(temp_file)), str(temp_file))

    def handle_download(self, download):
        # Automatically save the file
        download.setPath(download.downloadFileName())  # can customize path
        download.accept()


# Utility to locate HTML
def resource_path(relative_path):
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

app = QApplication(sys.argv)

view = QWebEngineView()

# Set up the channel
channel = QWebChannel()
backend = Backend(view)
channel.registerObject("backend", backend)
view.page().setWebChannel(channel)

# Load HTML
html_file = resource_path('index.html')
view.load(QUrl.fromLocalFile(html_file))
view.show()

sys.exit(app.exec())