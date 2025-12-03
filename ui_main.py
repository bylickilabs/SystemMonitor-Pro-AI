import os
import sys
import json
import webbrowser
import platform
from collections import defaultdict, deque
from datetime import datetime
 
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTabWidget,
    QComboBox,
    QMessageBox,
    QCheckBox,
    QFileDialog,
)

from config import (
    APP_NAME,
    APP_TITLE,
    APP_COMPANY,
    APP_VERSION,
    APP_AUTHOR,
    GITHUB_URL,
    UPDATE_INTERVAL_MS,
    THEME_BACKGROUND,
    THEME_TEXT,
    FONT_FAMILY,
    NEON_BACKGROUND,
    NEON_TEXT,
    NEON_ACCENT,
    NEON_SECONDARY,
    AUTOSTART_REG_NAME,
)
from monitoring import SystemMonitorBackend, AnomalyDetector, MetricStatus
from ui_components import (
    MetricCard,
    ProcessMonitorWidget,
    LiveGraphWidget,
    HeatmapWidget,
    EventLogWidget,
)

def is_autostart_enabled() -> bool:
    if platform.system() != "Windows":
        return False
    try:
        import winreg
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_READ,
        )
        try:
            value, _ = winreg.QueryValueEx(key, AUTOSTART_REG_NAME)
            return bool(value)
        except FileNotFoundError:
            return False
        finally:
            key.Close()
    except Exception:
        return False


def set_autostart_enabled(enabled: bool):
    if platform.system() != "Windows":
        return

    import winreg

    script_path = os.path.abspath(sys.argv[0])
    command = f'"{sys.executable}" "{script_path}"'

    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Run",
        0,
        winreg.KEY_SET_VALUE,
    )
    try:
        if enabled:
            winreg.SetValueEx(key, AUTOSTART_REG_NAME, 0, winreg.REG_SZ, command)
        else:
            try:
                winreg.DeleteValue(key, AUTOSTART_REG_NAME)
            except FileNotFoundError:
                pass
    finally:
        key.Close()

TRANSLATIONS = {
    "de": {
        "title_bar": f"{APP_TITLE} – {APP_COMPANY}",
        "tagline": "KI-gestütztes Echtzeit-Monitoring mit Prognosen, adaptiven Schwellen und Anomalie-Heatmap.",
        "lang_label": "Sprache:",
        "tab_dashboard": "Dashboard",
        "tab_processes": "Prozesse",
        "tab_analytics": "Analytics",
        "tab_settings": "Einstellungen",
        "metric_cpu": "CPU-Auslastung",
        "metric_ram": "RAM-Nutzung",
        "metric_disk": "Festplatten-Auslastung",
        "metric_net_up": "Netzwerk Upload",
        "metric_net_down": "Netzwerk Download",
        "status_label": "Status",
        "prediction_high_load": "Hohe Last erwartet in ca. {minutes:.1f} Minuten.",
        "prediction_normal": "Keine erhöhte Last im Prognosefenster (bis 30 Minuten) erwartet.",
        "prediction_insufficient": "Zu wenige Daten für eine verlässliche Prognose.",
        "footer": f"Entwickelt von {APP_AUTHOR} · {APP_COMPANY} · Version {APP_VERSION}",
        "btn_github": "GitHub",
        "btn_github_tooltip": "Projekt-Repository auf GitHub öffnen",
        "btn_info": "Info",
        "btn_info_tooltip": "Informationen zu dieser Anwendung",
        "btn_profile": "Profiling 60s",
        "btn_profile_tooltip": "60 Sekunden Diagnose-Profiling starten",
        "btn_export": "Export (JSON)",
        "btn_export_tooltip": "Event-Log als JSON exportieren",
        "info_title": "Über diese Anwendung",
        "info_text": (
            f"{APP_TITLE}\n\n"
            "SystemMonitor Pro AI ist ein lokal ausgeführtes, KI-gestütztes Monitoring-Tool "
            "für Windows- und Desktop-Umgebungen.\n\n"
            "Kernfunktionen:\n"
            "• Live-Überwachung von CPU, RAM, Festplatte und Netzwerk\n"
            "• Adaptive Schwellenwerte auf Basis statistischer Normalprofile\n"
            "• Prognosen zur Systemauslastung (Trend-Analyse)\n"
            "• Anomalie-Heatmap und AI-Event-Log\n"
            "• Vollständig zweisprachige Oberfläche (Deutsch/Englisch)\n\n"
            f"Entwickelt von {APP_AUTHOR} · {APP_COMPANY}"
        ),
        "state_LEARN": "KI lernt den Normalbereich – Basislinie wird aufgebaut (Messwerte: {samples}).",
        "state_STABLE": "Sehr stabile Werte, kaum Schwankungen (Ø={mean:.2f}, σ={stdev:.2f}).",
        "state_OK": "Wert im erwarteten Bereich (z≈{z:.2f}, Ø={mean:.2f}, σ={stdev:.2f}).",
        "state_WARN": "Erhöhte Abweichung vom Normalbereich (z≈{z:.2f}, Ø={mean:.2f}, σ={stdev:.2f}).",
        "state_ALERT": "Starke Abweichung vom Normalbereich – mögliche Anomalie (z≈{z:.2f}, Ø={mean:.2f}, σ={stdev:.2f}).",
        "state_UNKNOWN": "Status nicht verfügbar.",
        "heatmap_title": "AI-Anomalie-Heatmap (Wochentag × Stunde)",
        "eventlog_title": "AI-Event-Log (WARN/ALERT)",
        "settings_autostart": "Beim Systemstart automatisch starten (Windows)",
        "settings_neon": "Dark-Neon BYLICKILABS Mode aktivieren",
        "msg_profile_done_title": "Profiling abgeschlossen",
        "msg_profile_done_text": "60 Sekunden Profiling abgeschlossen. Ergebnis wurde als JSON gespeichert.",
        "msg_export_success": "Export erfolgreich",
        "msg_export_error": "Fehler beim Export",
    },
    "en": {
        "title_bar": f"{APP_TITLE} – {APP_COMPANY}",
        "tagline": "AI-powered real-time monitoring with forecasting, adaptive thresholds and anomaly heatmap.",
        "lang_label": "Language:",
        "tab_dashboard": "Dashboard",
        "tab_processes": "Processes",
        "tab_analytics": "Analytics",
        "tab_settings": "Settings",
        "metric_cpu": "CPU Utilization",
        "metric_ram": "RAM Usage",
        "metric_disk": "Disk Usage",
        "metric_net_up": "Network Upload",
        "metric_net_down": "Network Download",
        "status_label": "Status",
        "prediction_high_load": "High load expected in approx. {minutes:.1f} minutes.",
        "prediction_normal": "No increased load expected within the forecast window (up to 30 minutes).",
        "prediction_insufficient": "Not enough data yet for a reliable forecast.",
        "footer": f"Developed by {APP_AUTHOR} · {APP_COMPANY} · Version {APP_VERSION}",
        "btn_github": "GitHub",
        "btn_github_tooltip": "Open project repository on GitHub",
        "btn_info": "Info",
        "btn_info_tooltip": "Information about this application",
        "btn_profile": "Profiling 60s",
        "btn_profile_tooltip": "Start 60 seconds diagnostic profiling",
        "btn_export": "Export (JSON)",
        "btn_export_tooltip": "Export event log as JSON",
        "info_title": "About this application",
        "info_text": (
            f"{APP_TITLE}\n\n"
            "SystemMonitor Pro AI is a locally running, AI-powered monitoring tool "
            "for Windows and desktop environments.\n\n"
            "Core features:\n"
            "• Live monitoring of CPU, RAM, disk and network\n"
            "• Adaptive thresholds based on statistical baseline profiles\n"
            "• Forecasting of system load trends\n"
            "• Anomaly heatmap and AI event log\n"
            "• Fully bilingual interface (German/English)\n\n"
            f"Developed by {APP_AUTHOR} · {APP_COMPANY}"
        ),
        "state_LEARN": "AI is learning the baseline – building initial profile (samples: {samples}).",
        "state_STABLE": "Values are very stable with minimal variance (µ={mean:.2f}, σ={stdev:.2f}).",
        "state_OK": "Value within expected range (z≈{z:.2f}, µ={mean:.2f}, σ={stdev:.2f}).",
        "state_WARN": "Increased deviation from normal range (z≈{z:.2f}, µ={mean:.2f}, σ={stdev:.2f}).",
        "state_ALERT": "Strong deviation from normal range – potential anomaly (z≈{z:.2f}, µ={mean:.2f}, σ={stdev:.2f}).",
        "state_UNKNOWN": "Status not available.",
        "heatmap_title": "AI anomaly heatmap (weekday × hour)",
        "eventlog_title": "AI event log (WARN/ALERT)",
        "settings_autostart": "Start automatically with system boot (Windows)",
        "settings_neon": "Enable dark neon BYLICKILABS mode",
        "msg_profile_done_title": "Profiling completed",
        "msg_profile_done_text": "60 seconds profiling completed. Result has been saved as JSON.",
        "msg_export_success": "Export successful",
        "msg_export_error": "Error during export",
    },
}


class SystemMonitorUI(QWidget):
    def __init__(self):
        super().__init__()

        self.backend = SystemMonitorBackend()
        self.detector = AnomalyDetector()

        self.current_lang = "de"
        self.t = TRANSLATIONS

        self.history_for_forecast = defaultdict(lambda: deque(maxlen=60))

        self.profiling_active = False
        self.profiling_data = []

        self.neon_enabled = False

        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.setMinimumSize(1024, 640)

        self._build_ui()
        self._apply_stylesheet()
        self._start_timer()

    def _build_ui(self):
        root = QVBoxLayout()
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(10)

        top_bar = QHBoxLayout()
        top_bar.setSpacing(8)

        self.header_label = QLabel(self.t[self.current_lang]["title_bar"])
        self.header_label.setFont(QFont(FONT_FAMILY, 13, QFont.Bold))

        top_bar.addWidget(self.header_label)
        top_bar.addStretch()

        self.lang_label = QLabel(self.t[self.current_lang]["lang_label"])
        self.lang_label.setFont(QFont(FONT_FAMILY, 9))

        self.lang_combo = QComboBox()
        self.lang_combo.addItem("Deutsch", userData="de")
        self.lang_combo.addItem("English", userData="en")
        self.lang_combo.setCurrentIndex(0)
        self.lang_combo.currentIndexChanged.connect(self._on_language_changed)

        self.github_button = QPushButton(self.t[self.current_lang]["btn_github"])
        self.github_button.setToolTip(self.t[self.current_lang]["btn_github_tooltip"])
        self.github_button.clicked.connect(self._on_github_clicked)

        self.info_button = QPushButton(self.t[self.current_lang]["btn_info"])
        self.info_button.setToolTip(self.t[self.current_lang]["btn_info_tooltip"])
        self.info_button.clicked.connect(self._on_info_clicked)

        self.profile_button = QPushButton(self.t[self.current_lang]["btn_profile"])
        self.profile_button.setToolTip(self.t[self.current_lang]["btn_profile_tooltip"])
        self.profile_button.clicked.connect(self._on_profile_clicked)

        self.export_button = QPushButton(self.t[self.current_lang]["btn_export"])
        self.export_button.setToolTip(self.t[self.current_lang]["btn_export_tooltip"])
        self.export_button.clicked.connect(self._on_export_clicked)

        top_bar.addWidget(self.lang_label)
        top_bar.addWidget(self.lang_combo)
        top_bar.addWidget(self.github_button)
        top_bar.addWidget(self.info_button)
        top_bar.addWidget(self.profile_button)
        top_bar.addWidget(self.export_button)

        self.tagline_label = QLabel(self.t[self.current_lang]["tagline"])
        self.tagline_label.setFont(QFont(FONT_FAMILY, 9))

        self.tab_widget = QTabWidget()

        self.dashboard_tab = QWidget()
        self._build_dashboard_tab()

        self.process_tab = QWidget()
        self._build_process_tab()

        self.analytics_tab = QWidget()
        self._build_analytics_tab()

        self.settings_tab = QWidget()
        self._build_settings_tab()

        self.tab_widget.addTab(self.dashboard_tab, self.t[self.current_lang]["tab_dashboard"])
        self.tab_widget.addTab(self.process_tab, self.t[self.current_lang]["tab_processes"])
        self.tab_widget.addTab(self.analytics_tab, self.t[self.current_lang]["tab_analytics"])
        self.tab_widget.addTab(self.settings_tab, self.t[self.current_lang]["tab_settings"])

        self.footer_label = QLabel(self.t[self.current_lang]["footer"])
        self.footer_label.setFont(QFont(FONT_FAMILY, 8))
        self.footer_label.setAlignment(Qt.AlignRight)

        root.addLayout(top_bar)
        root.addWidget(self.tagline_label)
        root.addWidget(self.tab_widget)
        root.addWidget(self.footer_label)

        self.setLayout(root)

    def _apply_stylesheet(self):
        if self.neon_enabled:
            bg = NEON_BACKGROUND
            text = NEON_TEXT
        else:
            bg = THEME_BACKGROUND
            text = THEME_TEXT

        self.setStyleSheet(f"""
        QWidget {{
            background-color: {bg};
            color: {text};
            font-family: {FONT_FAMILY};
        }}
        QPushButton {{
            padding: 6px 12px;
            border-radius: 6px;
            border: 1px solid #4b5563;
            background-color: #111827;
        }}
        QPushButton:hover {{
            border-color: #9ca3af;
            background-color: #1f2937;
        }}
        QComboBox {{
            padding: 3px 8px;
            border-radius: 4px;
            border: 1px solid #4b5563;
            background-color: #020617;
            color: {text};
        }}
        QComboBox QAbstractItemView {{
            background-color: #020617;
            color: {text};
            selection-background-color: #1f2937;
        }}
        QTabWidget::pane {{
            border: 1px solid #1f2937;
            border-radius: 6px;
        }}
        QTabBar::tab {{
            padding: 6px 12px;
        }}
        """)

    def _build_dashboard_tab(self):
        from PySide6.QtWidgets import QGridLayout

        layout = QVBoxLayout()
        grid = QGridLayout()
        grid.setSpacing(10)

        self.metric_title_keys = {
            "CPU (%)": "metric_cpu",
            "RAM (%)": "metric_ram",
            "Disk (%)": "metric_disk",
            "Net Up (kB/s)": "metric_net_up",
            "Net Down (kB/s)": "metric_net_down",
        }

        self.metric_cards = {}
        self.metric_graphs = {}

        positions = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)]

        for (metric_key, title_key), (row, col) in zip(self.metric_title_keys.items(), positions):
            title = self.t[self.current_lang][title_key]
            card = MetricCard(title, TRANSLATIONS, self.current_lang)
            graph = LiveGraphWidget()

            container = QVBoxLayout()
            container.addWidget(card)
            container.addWidget(graph)

            wrapper = QWidget()
            wrapper.setLayout(container)

            grid.addWidget(wrapper, row, col)

            self.metric_cards[metric_key] = card
            self.metric_graphs[metric_key] = graph

        layout.addLayout(grid)
        self.dashboard_tab.setLayout(layout)

    def _build_process_tab(self):
        layout = QVBoxLayout()
        self.process_monitor = ProcessMonitorWidget()
        layout.addWidget(self.process_monitor)
        self.process_tab.setLayout(layout)

    def _build_analytics_tab(self):
        layout = QVBoxLayout()

        self.heatmap_title_label = QLabel(self.t[self.current_lang]["heatmap_title"])
        self.heatmap_title_label.setFont(QFont(FONT_FAMILY, 10, QFont.Bold))

        self.heatmap_widget = HeatmapWidget()

        self.eventlog_title_label = QLabel(self.t[self.current_lang]["eventlog_title"])
        self.eventlog_title_label.setFont(QFont(FONT_FAMILY, 10, QFont.Bold))

        self.eventlog_widget = EventLogWidget()

        layout.addWidget(self.heatmap_title_label)
        layout.addWidget(self.heatmap_widget)
        layout.addSpacing(10)
        layout.addWidget(self.eventlog_title_label)
        layout.addWidget(self.eventlog_widget)

        self.analytics_tab.setLayout(layout)

    def _build_settings_tab(self):
        layout = QVBoxLayout()
        layout.setSpacing(8)

        self.chk_autostart = QCheckBox(self.t[self.current_lang]["settings_autostart"])
        self.chk_autostart.setChecked(is_autostart_enabled())
        self.chk_autostart.stateChanged.connect(self._on_autostart_changed)

        self.chk_neon = QCheckBox(self.t[self.current_lang]["settings_neon"])
        self.chk_neon.setChecked(self.neon_enabled)
        self.chk_neon.stateChanged.connect(self._on_neon_changed)

        layout.addWidget(self.chk_autostart)
        layout.addWidget(self.chk_neon)
        layout.addStretch()

        self.settings_tab.setLayout(layout)

    def _on_language_changed(self, index: int):
        lang_code = self.lang_combo.itemData(index)
        if lang_code not in ("de", "en"):
            return
        self.current_lang = lang_code
        self._apply_translations()

    def _apply_translations(self):
        tr = self.t[self.current_lang]

        self.header_label.setText(tr["title_bar"])
        self.tagline_label.setText(tr["tagline"])
        self.lang_label.setText(tr["lang_label"])
        self.github_button.setText(tr["btn_github"])
        self.github_button.setToolTip(tr["btn_github_tooltip"])
        self.info_button.setText(tr["btn_info"])
        self.info_button.setToolTip(tr["btn_info_tooltip"])
        self.profile_button.setText(tr["btn_profile"])
        self.profile_button.setToolTip(tr["btn_profile_tooltip"])
        self.export_button.setText(tr["btn_export"])
        self.export_button.setToolTip(tr["btn_export_tooltip"])
        self.footer_label.setText(tr["footer"])

        self.tab_widget.setTabText(0, tr["tab_dashboard"])
        self.tab_widget.setTabText(1, tr["tab_processes"])
        self.tab_widget.setTabText(2, tr["tab_analytics"])
        self.tab_widget.setTabText(3, tr["tab_settings"])

        for metric_key, card in self.metric_cards.items():
            title_key = self.metric_title_keys[metric_key]
            card.title_label.setText(tr[title_key])
            card.update_language(self.current_lang)

        self.heatmap_title_label.setText(tr["heatmap_title"])
        self.eventlog_title_label.setText(tr["eventlog_title"])
        self.chk_autostart.setText(tr["settings_autostart"])
        self.chk_neon.setText(tr["settings_neon"])

    def _on_github_clicked(self):
        if GITHUB_URL:
            webbrowser.open(GITHUB_URL)

    def _on_info_clicked(self):
        tr = self.t[self.current_lang]
        QMessageBox.information(self, tr["info_title"], tr["info_text"])

    def _on_profile_clicked(self):
        if self.profiling_active:
            return
        self.profiling_active = True
        self.profiling_data = []

        self.profile_timer = QTimer(self)
        self.profile_timer.setSingleShot(True)
        self.profile_timer.timeout.connect(self._on_profile_done)
        self.profile_timer.start(60_000)

    def _on_profile_done(self):
        tr = self.t[self.current_lang]

        if not self.profiling_data:
            self.profiling_active = False
            QMessageBox.information(self, tr["msg_profile_done_title"], tr["msg_profile_done_text"])
            return

        default_name = f"systemmonitor_profiling_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            tr["msg_profile_done_title"],
            default_name,
            "JSON Files (*.json)",
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(self.profiling_data, f, indent=2)
            except Exception as e:
                QMessageBox.warning(self, tr["msg_export_error"], str(e))

        self.profiling_active = False
        QMessageBox.information(self, tr["msg_profile_done_title"], tr["msg_profile_done_text"])

    def _on_export_clicked(self):
        tr = self.t[self.current_lang]
        events = self.eventlog_widget.get_events()
        if not events:
            QMessageBox.information(self, tr["msg_export_success"], "Keine Events zum Export vorhanden.")
            return

        default_name = f"systemmonitor_events_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            tr["btn_export"],
            default_name,
            "JSON Files (*.json)",
        )
        if not file_path:
            return

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(events, f, indent=2)
            QMessageBox.information(self, tr["msg_export_success"], tr["msg_export_success"])
        except Exception as e:
            QMessageBox.warning(self, tr["msg_export_error"], f"{tr['msg_export_error']}: {e}")

    def _on_autostart_changed(self, state: int):
        enabled = state == Qt.Checked
        set_autostart_enabled(enabled)

    def _on_neon_changed(self, state: int):
        self.neon_enabled = state == Qt.Checked
        self._apply_stylesheet()

    def _start_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_metrics)
        self.timer.start(UPDATE_INTERVAL_MS)

    def _format_status_details(self, status: MetricStatus) -> str:
        tr = self.t[self.current_lang]

        if status.state == "LEARN":
            return tr["state_LEARN"].format(samples=status.samples)

        if status.mean is None or status.stdev is None or status.z_score is None:
            return tr["state_UNKNOWN"]

        if status.state == "STABLE":
            return tr["state_STABLE"].format(mean=status.mean, stdev=status.stdev)
        elif status.state == "OK":
            return tr["state_OK"].format(z=status.z_score, mean=status.mean, stdev=status.stdev)
        elif status.state == "WARN":
            return tr["state_WARN"].format(z=status.z_score, mean=status.mean, stdev=status.stdev)
        elif status.state == "ALERT":
            return tr["state_ALERT"].format(z=status.z_score, mean=status.mean, stdev=status.stdev)

        return tr["state_UNKNOWN"]

    def _forecast_high_load_minutes(self, metric_name: str, threshold: float = 80.0):
        history = self.history_for_forecast[metric_name]
        if len(history) < 10:
            return None

        n = len(history)
        xs = list(range(n))
        ys = list(history)

        mean_x = sum(xs) / n
        mean_y = sum(ys) / n

        num = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
        den = sum((x - mean_x) ** 2 for x in xs) or 1.0
        slope = num / den
        intercept = mean_y - slope * mean_x

        if slope <= 0:
            return None

        t_index = (threshold - intercept) / slope
        if t_index <= n - 1:
            return 0.0

        steps_ahead = t_index - (n - 1)
        seconds_per_step = UPDATE_INTERVAL_MS / 1000.0
        minutes = steps_ahead * seconds_per_step / 60.0
        if 0 < minutes <= 30:
            return minutes
        return None

    def _format_prediction_text(self, metric_name: str) -> str:
        tr = self.t[self.current_lang]
        minutes = self._forecast_high_load_minutes(metric_name)
        if minutes is None:
            history = self.history_for_forecast[metric_name]
            if len(history) < 10:
                return tr["prediction_insufficient"]
            return tr["prediction_normal"]
        return tr["prediction_high_load"].format(minutes=minutes)

    def _update_metrics(self):
        raw_metrics = self.backend.collect()

        if self.profiling_active:
            snapshot = {
                "timestamp": datetime.now().isoformat(),
                "metrics": {},
            }
        else:
            snapshot = None

        for metric_key, (value, unit) in raw_metrics.items():
            self.history_for_forecast[metric_key].append(value)

            status = self.detector.evaluate(metric_key, value, unit)
            details_text = self._format_status_details(status)
            prediction_text = self._format_prediction_text(metric_key)

            card = self.metric_cards.get(metric_key)
            graph = self.metric_graphs.get(metric_key)
            if card:
                card.update_metric(status, details_text, prediction_text)
            if graph:
                if unit == "%":
                    graph.add_value(max(0.0, min(100.0, value)))
                else:
                    graph.add_value(max(0.0, min(100.0, value / 10.0)))

            if status.state in ("WARN", "ALERT"):
                self.eventlog_widget.add_event(metric_key, status.state, value)
                self.heatmap_widget.add_event(status.state)

            if snapshot is not None:
                snapshot["metrics"][metric_key] = {"value": value, "unit": unit}

        if snapshot is not None:
            self.profiling_data.append(snapshot)