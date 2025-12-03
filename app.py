import sys
from PySide6.QtWidgets import QApplication
from ui_main import SystemMonitorUI
 
def main():
    app = QApplication(sys.argv)
    app.setApplicationName("SystemMonitor Pro AI")
    window = SystemMonitorUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()