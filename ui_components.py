import psutil
from datetime import datetime
from collections import deque
 
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QColor, QPainter, QPen
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QFrame,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
)

from config import THEME_TEXT, FONT_FAMILY

class MetricCard(QFrame):
    def __init__(self, title: str, translations: dict, lang: str):
        super().__init__()
        self.setObjectName("metricCard")

        self.translations = translations
        self.lang = lang

        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(6)

        self.title_label = QLabel(title)
        self.title_label.setFont(QFont(FONT_FAMILY, 11, QFont.Bold))

        self.value_label = QLabel("--")
        self.value_label.setFont(QFont(FONT_FAMILY, 18, QFont.Bold))

        self.pred_label = QLabel("")
        self.pred_label.setFont(QFont(FONT_FAMILY, 9))

        self.state_label = QLabel("Status: –")
        self.state_label.setFont(QFont(FONT_FAMILY, 9))

        self.details_label = QLabel("")
        self.details_label.setFont(QFont(FONT_FAMILY, 8))
        self.details_label.setWordWrap(True)

        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)
        layout.addWidget(self.pred_label)
        layout.addWidget(self.state_label)
        layout.addWidget(self.details_label)

        self.setLayout(layout)
        self._apply_state_style("LEARN")

    def _apply_state_style(self, status: str):
        if status in ("OK", "STABLE"):
            bg = "#1e3a2f"
            border = "#10b981"
        elif status == "WARN":
            bg = "#3b2f1e"
            border = "#fbbf24"
        elif status == "ALERT":
            bg = "#3f1e1e"
            border = "#ef4444"
        else:
            bg = "#111827"
            border = "#6b7280"

        self.setStyleSheet(f"""
        QFrame#metricCard {{
            background-color: {bg};
            border: 1px solid {border};
            border-radius: 8px;
        }}
        QLabel {{
            color: {THEME_TEXT};
        }}
        """)

    def update_language(self, lang: str):
        self.lang = lang
        self.state_label.setText(f"{self.translations[self.lang]['status_label']}: –")

    def update_metric(self, status, details_text: str, prediction_text: str):
        self.value_label.setText(f"{status.value:.2f} {status.unit}")
        self.state_label.setText(f"{self.translations[self.lang]['status_label']}: {status.state}")
        self.details_label.setText(details_text)
        self.pred_label.setText(prediction_text)
        self._apply_state_style(status.state)

class ProcessMonitorWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setSpacing(6)

        header = QHBoxLayout()
        title = QLabel("Top 10 Prozesse")
        title.setFont(QFont(FONT_FAMILY, 10, QFont.Bold))

        self.refresh_button = QPushButton("Aktualisieren")
        self.refresh_button.clicked.connect(self.update_processes)

        self.kill_button = QPushButton("Prozess beenden")
        self.kill_button.clicked.connect(self.kill_selected_process)

        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.refresh_button)
        header.addWidget(self.kill_button)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["PID", "Name", "CPU %", "RAM %", "Threads"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)

        layout.addLayout(header)
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_processes)
        self.timer.start(3000)

    def update_processes(self):
        processes = []
        for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'num_threads']):
            try:
                info = p.info
                processes.append(info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
        processes = processes[:10]

        self.table.setRowCount(len(processes))

        for row, info in enumerate(processes):
            self.table.setItem(row, 0, QTableWidgetItem(str(info['pid'])))
            self.table.setItem(row, 1, QTableWidgetItem(str(info['name'])))
            self.table.setItem(row, 2, QTableWidgetItem(f"{info['cpu_percent']:.1f}"))
            self.table.setItem(row, 3, QTableWidgetItem(f"{info['memory_percent']:.1f}"))
            self.table.setItem(row, 4, QTableWidgetItem(str(info['num_threads'])))

    def kill_selected_process(self):
        from PySide6.QtWidgets import QMessageBox

        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Prozess beenden", "Bitte einen Prozess auswählen.")
            return

        pid_item = self.table.item(row, 0)
        if pid_item is None:
            return

        pid = int(pid_item.text())
        name_item = self.table.item(row, 1)
        name = name_item.text() if name_item else str(pid)

        confirm = QMessageBox.question(
            self,
            "Prozess beenden",
            f"Soll der Prozess '{name}' (PID {pid}) wirklich beendet werden?",
        )
        if confirm != QMessageBox.Yes:
            return

        try:
            p = psutil.Process(pid)
            p.terminate()
        except Exception as e:
            QMessageBox.warning(self, "Fehler", f"Prozess konnte nicht beendet werden:\n{e}")

class LiveGraphWidget(QWidget):
    def __init__(self, color: QColor = QColor("#10b981")):
        super().__init__()
        self.values = deque(maxlen=60)
        self.color = color
        self.setMinimumHeight(80)

    def add_value(self, v: float):
        self.values.append(v)
        self.update()

    def paintEvent(self, event):
        if not self.values:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(self.color, 2)
        painter.setPen(pen)

        w = self.width()
        h = self.height()

        max_i = max(len(self.values) - 1, 1)
        points = []
        for i, val in enumerate(self.values):
            x = int((i / max_i) * w)
            y = int(h - (val / 100.0) * h)
            points.append((x, y))

        for i in range(len(points) - 1):
            painter.drawLine(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1])

class HeatmapWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(160)
        self.data = [[0 for _ in range(24)] for _ in range(7)]

    def add_event(self, state: str):
        now = datetime.now()
        day = now.weekday()
        hour = now.hour

        if state == "WARN":
            self.data[day][hour] += 1
        elif state == "ALERT":
            self.data[day][hour] += 2

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        w = self.width() / 24
        h = self.height() / 7

        for d in range(7):
            for h_i in range(24):
                val = self.data[d][h_i]

                if val == 0:
                    color = QColor("#111827")
                elif val == 1:
                    color = QColor("#fbbf24")
                else:
                    color = QColor("#ef4444")

                painter.fillRect(h_i * w, d * h, w - 1, h - 1, color)

class EventLogWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Zeit", "Metrik", "Status", "Wert"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addWidget(self.table)
        self.setLayout(layout)

    def add_event(self, metric_name: str, state: str, value: float):
        row = self.table.rowCount()
        self.table.insertRow(row)

        self.table.setItem(row, 0, QTableWidgetItem(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        self.table.setItem(row, 1, QTableWidgetItem(metric_name))
        self.table.setItem(row, 2, QTableWidgetItem(state))
        self.table.setItem(row, 3, QTableWidgetItem(f"{value:.2f}"))

    def get_events(self):
        events = []
        rows = self.table.rowCount()

        for r in range(rows):
            events.append({
                "timestamp": self.table.item(r, 0).text(),
                "metric": self.table.item(r, 1).text(),
                "status": self.table.item(r, 2).text(),
                "value": float(self.table.item(r, 3).text().replace(",", ".")),
            })

        return events