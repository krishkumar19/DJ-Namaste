import time
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QFrame, QMessageBox, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QApplication, QSplashScreen, QDialog, QDesktopWidget
import sys

import mainfileeee_rc
import krish
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QWidget, QFormLayout
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QPainterPath
from PyQt5.QtCore import QTimer, Qt, QRectF

class DynamicBarChart(QWidget):
    def __init__(self, parent=None):
        super(DynamicBarChart, self).__init__(parent)
        self.setMinimumHeight(200)
        self.bars = [40, 70, 30, 90, 50, 20, 80]
        self.current_heights = [0]*len(self.bars)
        self.hovered = -1
        self.setMouseTracking(True)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(30)
        self.anim_step = 0
        
    def animate(self):
        if self.anim_step <= 100:
            for i in range(len(self.bars)):
                target = self.bars[i]
                t = self.anim_step / 100.0
                eased = 1 - pow(1 - t, 3)
                self.current_heights[i] = target * eased
            self.anim_step += 2
            self.update()
        else:
            self.timer.stop()

    def mouseMoveEvent(self, event):
        width = self.width()
        bar_width = (width - 40) / len(self.bars) - 10
        for i in range(len(self.bars)):
            x = 20 + i * (bar_width + 10)
            if x <= event.x() <= x + bar_width:
                if self.hovered != i:
                    self.hovered = i
                    self.update()
                return
        if self.hovered != -1:
            self.hovered = -1
            self.update()

    def leaveEvent(self, event):
        self.hovered = -1
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        width = self.width()
        height = self.height()
        painter.fillRect(0, 0, width, height, Qt.transparent)
        bar_width = (width - 40) / len(self.bars) - 10
        max_bar_val = max(self.bars) if self.bars else 100
        labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        painter.setPen(Qt.NoPen)
        for i, val in enumerate(self.current_heights):
            x = 20 + i * (bar_width + 10)
            bar_height = (val / max_bar_val) * (height - 50)
            y = height - 30 - bar_height
            color = QColor("#34d399") if i == self.hovered else QColor("#10b981")
            painter.setBrush(color)
            path = QPainterPath()
            path.addRoundedRect(QRectF(x, y, bar_width, bar_height), 4, 4)
            painter.drawPath(path)
            if i == self.hovered:
                painter.setPen(QPen(QColor("#ffffff")))
                painter.drawText(int(x), int(y) - 5, f"\u20b9{int(val*10000):,}")
                painter.setPen(Qt.NoPen)
            painter.setPen(QPen(QColor("#888888")))
            label = labels[i] if i < len(labels) else str(i)
            painter.drawText(int(x), height - 5, label)
            painter.setPen(Qt.NoPen)


class SplashScreen(QSplashScreen):
    def __init__(self):
        super(QSplashScreen, self).__init__()
        loadUi("splash.ui", self)
        self.center1()

    def center1(self):
       qr = self.frameGeometry()
       cp = QDesktopWidget().availableGeometry().center()
       qr.moveCenter(cp)
       self.move(qr.topLeft())


    # self.setWindowFlags(Qt.FramelessWindowHint)

    def progress(self):
        for i in range(101):
            time.sleep(0.05)  # Make it slightly faster (5 seconds total)
            self.progressBar.setValue(i)
            QApplication.processEvents()  # Keeps the UI responsive!


'''class MainWindow(QDialog):
    def __init__(self):
        super(QDialog, self).__init__()
        loadUi("yesyes.ui", self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.pushButton.clicked.connect(self.goto)

    def goto(self):
        gotodash = DashWindow()
        widget.addWidget(gotodash)
        widget.setCurrentIndex(widget.currentIndex()+1)'''


class DashWindow(QDialog):
    def __init__(self):
        super(DashWindow, self).__init__()
        loadUi("krish.ui", self)
        self.setMinimumSize(1920, 1080)
        self.setStyleSheet("background-color: #121212;")
        if hasattr(self, 'change_btn'):
            self.change_btn.clicked.connect(self.toggle_menu)
            
        # Hook up home button
        if hasattr(self, 'home_btn_2'): self.home_btn_2.clicked.connect(self.goto_home)
        if hasattr(self, 'home_btn'): self.home_btn.clicked.connect(self.goto_home)
        
        # Fix dark blue backgrounds from ui files
        for child in self.findChildren(QWidget):
            if child.styleSheet():
                new_style = child.styleSheet().replace("rgb(13, 9, 36)", "#121212").replace("rgb(8, 8, 8)", "#121212")
                child.setStyleSheet(new_style)
                
        # Connect top bar buttons
        if hasattr(self, 'pushButton_18'): self.pushButton_18.clicked.connect(self.goto) # Analysis -> ShowData
        if hasattr(self, 'pushButton_19'): self.pushButton_19.clicked.connect(self.goto_earnings) # Earnings
        if hasattr(self, 'pushButton_20'): self.pushButton_20.clicked.connect(self.goto_account) # Account
        
        # Hover animation on all QPushButton children via QSS
        hover_qss = """
        QPushButton {
            border-radius: 6px;
        }
        QPushButton:hover {
            background-color: rgba(16, 185, 129, 0.18);
            color: #34d399;
        }
        """
        for btn in self.findChildren(QPushButton):
            btn.setStyleSheet(btn.styleSheet() + hover_qss)
        
        # Wire top insight/progress/treads buttons to real popup screens
        if hasattr(self, 'pushButton_8'):  self.pushButton_8.clicked.connect(lambda: self._open_popup(InsightScreen))
        if hasattr(self, 'pushButton_9'):  self.pushButton_9.clicked.connect(lambda: self._open_popup(ProgressScreen))
        if hasattr(self, 'pushButton_10'): self.pushButton_10.clicked.connect(lambda: self._open_popup(TreadsScreen))
        if hasattr(self, 'pushButton_12'): self.pushButton_12.clicked.connect(lambda: self._open_popup(TreadsScreen))
        if hasattr(self, 'pushButton_14'): self.pushButton_14.clicked.connect(lambda: self._open_popup(InsightScreen))
        if hasattr(self, 'pushButton_15'): self.pushButton_15.clicked.connect(lambda: self._open_popup(ProgressScreen))
        for n in ['pushButton', 'pushButton_2', 'pushButton_3', 'pushButton_11']:
            if hasattr(self, n): getattr(self, n).clicked.connect(lambda: self._open_popup(InsightScreen))
        
        # Inject dynamic chart
        if hasattr(self, 'calenderBox'):
            self.dynamic_chart = DynamicBarChart(self.calenderBox)
            # Find the layout of calenderBox to add it, and hide label_60
            if hasattr(self, 'label_60'):
                self.label_60.hide()
            layout = self.calenderBox.layout()
            if not layout:
                layout = QVBoxLayout(self.calenderBox)
            layout.addWidget(self.dynamic_chart)
            
        self.center2()


    def goto(self):
        createacc = ShowData()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        
    def goto_earnings(self):
        scr = EarningScreen()
        widget.addWidget(scr)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        
    def goto_account(self):
        scr = AccountScreen()
        widget.addWidget(scr)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        
    def goto_home(self):
        # Already home, or reload it
        pass
        
    def toggle_menu(self):
        if hasattr(self, 'full_menu_widget') and hasattr(self, 'icon_only_widget'):
            if self.full_menu_widget.isHidden():
                self.full_menu_widget.show()
                self.icon_only_widget.hide()
            else:
                self.full_menu_widget.hide()
                self.icon_only_widget.show()

    def center2(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def _open_popup(self, screen_cls):
        scr = screen_cls()
        widget.addWidget(scr)
        widget.setCurrentIndex(widget.currentIndex() + 1)


# ── Insight Popup ──────────────────────────────────────────────────────────────
class InsightScreen(QDialog):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background:#121212; color:#e0e0e0;")
        from PyQt5.QtWidgets import QHBoxLayout, QFrame
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 20, 40, 40); layout.setSpacing(16)
        back = QPushButton("\u2190 Back"); back.setStyleSheet("background:transparent;color:#10b981;font-size:16px;border:none;")
        back.clicked.connect(self.gotodash); layout.addWidget(back)
        layout.addWidget(self._h("Business Insights \u2014 DJ Namaste", 28))
        rows = [
            ("Top Service This Month", "DJ Event Booking", "#10b981"),
            ("Peak Booking Hour", "7 PM \u2013 10 PM", "#f59e0b"),
            ("Highest Revenue City", "Mumbai", "#3b82f6"),
            ("New Customers (May)", "38", "#10b981"),
            ("Returning Customers", "62%", "#a78bfa"),
            ("Avg. Ticket Value", "\u20b98,450", "#10b981"),
            ("Cancelled Requests", "4", "#ef4444"),
            ("NPS Score", "82 / 100", "#10b981"),
        ]
        for label, val, color in rows:
            card = QFrame(); card.setStyleSheet("background:#1e1e1e; border-radius:10px; padding:16px;")
            row = QHBoxLayout(card)
            lbl = QLabel(label); lbl.setStyleSheet("font-size:15px; color:#aaa;")
            vl = QLabel(val); vl.setStyleSheet(f"font-size:18px; font-weight:bold; color:{color};")
            row.addWidget(lbl); row.addStretch(); row.addWidget(vl)
            layout.addWidget(card)
        layout.addStretch()

    def _h(self, text, size):
        l = QLabel(text); l.setStyleSheet(f"font-size:{size}px; font-weight:bold; color:#fff;"); return l

    def gotodash(self):
        d = DashWindow(); widget.addWidget(d); widget.setCurrentIndex(widget.currentIndex() + 1)


# ── Progress Popup ─────────────────────────────────────────────────────────────
class ProgressScreen(QDialog):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background:#121212; color:#e0e0e0;")
        from PyQt5.QtWidgets import QProgressBar, QFrame
        layout = QVBoxLayout(self); layout.setContentsMargins(40,20,40,40); layout.setSpacing(16)
        back = QPushButton("\u2190 Back"); back.setStyleSheet("background:transparent;color:#10b981;font-size:16px;border:none;")
        back.clicked.connect(self.gotodash); layout.addWidget(back)
        layout.addWidget(self._h("Operational Progress Tracker", 28))
        targets = [
            ("Monthly Bookings Target", 78),
            ("Employee Efficiency", 91),
            ("Customer Satisfaction", 85),
            ("Revenue Goal (May)", 62),
            ("Pending Requests Resolved", 88),
        ]
        for label, pct in targets:
            card = QFrame(); card.setStyleSheet("background:#1e1e1e; border-radius:10px; padding:20px;")
            cl = QVBoxLayout(card)
            lrow = QLabel(f"{label}  —  {pct}%"); lrow.setStyleSheet("font-size:14px; color:#ccc;")
            bar = QProgressBar(); bar.setValue(pct)
            bar.setStyleSheet("QProgressBar{background:#2a2a2a;border-radius:6px;height:16px;} QProgressBar::chunk{background:#10b981;border-radius:6px;}")
            cl.addWidget(lrow); cl.addWidget(bar); layout.addWidget(card)
        layout.addStretch()

    def _h(self, text, size):
        l = QLabel(text); l.setStyleSheet(f"font-size:{size}px; font-weight:bold; color:#fff;"); return l

    def gotodash(self):
        d = DashWindow(); widget.addWidget(d); widget.setCurrentIndex(widget.currentIndex() + 1)


# ── Treads Popup ───────────────────────────────────────────────────────────────
class TreadsScreen(QDialog):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background:#121212; color:#e0e0e0;")
        from PyQt5.QtWidgets import QFrame
        layout = QVBoxLayout(self); layout.setContentsMargins(40,20,40,40); layout.setSpacing(14)
        back = QPushButton("\u2190 Back"); back.setStyleSheet("background:transparent;color:#10b981;font-size:16px;border:none;")
        back.clicked.connect(self.gotodash); layout.addWidget(back)
        layout.addWidget(self._h("Service Threads & Activity Log", 28))
        threads = [
            ("#1042", "DJ Booking — Rahul Sharma", "Open", "#f59e0b", "2h ago"),
            ("#1041", "Plumbing — Riya Singh", "Resolved", "#10b981", "5h ago"),
            ("#1040", "Cleaning — Vikram Rathore", "In Progress", "#3b82f6", "1d ago"),
            ("#1039", "Technician — Priya Patel", "Resolved", "#10b981", "1d ago"),
            ("#1038", "DJ Booking — Amit Kumar", "Open", "#f59e0b", "2d ago"),
            ("#1037", "Plumbing — Sneha Verma", "Cancelled", "#ef4444", "3d ago"),
        ]
        for tid, title, status, color, time in threads:
            card = QFrame(); card.setStyleSheet("background:#1e1e1e; border-radius:10px; padding:16px;")
            from PyQt5.QtWidgets import QHBoxLayout
            row = QHBoxLayout(card)
            id_l = QLabel(tid); id_l.setStyleSheet("font-size:13px; color:#666; min-width:50px;")
            t_l = QLabel(title); t_l.setStyleSheet("font-size:15px; color:#ddd;")
            s_l = QLabel(status); s_l.setStyleSheet(f"font-size:13px; font-weight:bold; color:{color};")
            tm_l = QLabel(time); tm_l.setStyleSheet("font-size:12px; color:#666;")
            row.addWidget(id_l); row.addWidget(t_l); row.addStretch(); row.addWidget(s_l); row.addWidget(tm_l)
            layout.addWidget(card)
        layout.addStretch()

    def _h(self, text, size):
        l = QLabel(text); l.setStyleSheet(f"font-size:{size}px; font-weight:bold; color:#fff;"); return l

    def gotodash(self):
        d = DashWindow(); widget.addWidget(d); widget.setCurrentIndex(widget.currentIndex() + 1)


class ShowData(QDialog):
    def __init__(self):
        super(ShowData,self).__init__()
        loadUi("mainfile.ui",self)
        self.setMinimumSize(1920, 1080)
        self.setStyleSheet("background-color: #121212;")
        self.dashborad_btn_4.clicked.connect(self.gotodash)
        self.ser3.clicked.connect(self.gotosql)
        self.products_btn_4.clicked.connect(self.gotosdervicedata)

    def gotosdervicedata(self):
        service = ShowserviceData()
        widget.addWidget(service)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    def gotodash(self):
        dashbrd2 = DashWindow()
        widget.addWidget(dashbrd2)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotosql(self):
        sql1 = ShowsqlData()
        widget.addWidget(sql1)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class ShowsqlData(QDialog):
    def __init__(self):
        super(ShowsqlData,self).__init__()
        loadUi("anlysis.ui",self)
        self.setMinimumSize(1920, 1080)
        self.setStyleSheet("background-color: #121212;")
        self.back_btn.clicked.connect(self.gotoshowdata)
        
        # Database Integration
        from database import ConnectDatabase
        self.db = ConnectDatabase()
        
        self.buttons_list = [self.add_btn, self.update_btn, self.delete_btn, self.clear_btn, self.select_btn]
        self.init_signal_slot()
        self.search_info()

    def gotoshowdata(self):
        showdata1 = ShowData()
        widget.addWidget(showdata1)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def init_signal_slot(self):
        # Map actual UI object names to expected attributes
        self.employe_id = getattr(self, "lineEdit", QLineEdit())
        self.first_name = getattr(self, "lineEdit_2", QLineEdit())
        self.last_name = getattr(self, "lineEdit_3", QLineEdit())
        self.email_address = getattr(self, "lineEdit_4", QLineEdit())
        # In PyQt, combo boxes are QComboBox
        from PyQt5.QtWidgets import QComboBox, QTableWidget
        self.state = getattr(self, "comboBox", QComboBox())
        self.city = getattr(self, "comboBox_2", QComboBox())
        self.result_table = getattr(self, "tableWidget", QTableWidget())
        
        # Connect buttons to their respective functions
        if hasattr(self, 'add_btn'): self.add_btn.clicked.connect(self.add_info)
        if hasattr(self, 'clear_btn'): self.clear_btn.clicked.connect(self.clear_form_info)
        if hasattr(self, 'select_btn'): self.select_btn.clicked.connect(self.select_info)
        if hasattr(self, 'update_btn'): self.update_btn.clicked.connect(self.update_info)
        if hasattr(self, 'delete_btn'): self.delete_btn.clicked.connect(self.delete_info)

    def disable_buttons(self):
        for button in self.buttons_list:
            button.setDisabled(True)

    def enable_buttons(self):
        for button in self.buttons_list:
            button.setDisabled(False)

    def add_info(self):
        self.disable_buttons()
        student_info = self.get_student_info()

        if student_info["first_name"]:
            add_result = self.db.add_info(
                Employe_id=student_info["employe_id"] if student_info["employe_id"] else None,
                first_name=student_info["first_name"],
                last_name=student_info["last_name"],
                email_address=student_info["email_address"],
                state=student_info["state"],
                city=student_info["city"]
            )

            if add_result:
                QMessageBox.information(self, "Warning", f"Add fail: {add_result}, Please try again.", QMessageBox.StandardButton.Ok)
            else:
                self.clear_form_info()
        else:
            QMessageBox.information(self, "Warning", "Please input at least a first name.", QMessageBox.StandardButton.Ok)

        self.search_info()
        self.enable_buttons()

    def update_info(self):
        new_student_info = self.get_student_info()

        if new_student_info["employe_id"]:
            update_result = self.db.update_info(
                Employe_id=new_student_info["employe_id"],
                first_name=new_student_info["first_name"],
                last_name=new_student_info["last_name"],
                email_address=new_student_info["email_address"],
                state=new_student_info["state"],
                city=new_student_info["city"]
            )

            if update_result:
                QMessageBox.information(self, "Warning", f"Fail to update the information: {update_result}. Please try again.", QMessageBox.StandardButton.Ok)
            else:
                self.clear_form_info()
                self.search_info()
        else:
            QMessageBox.information(self, "Warning", "Please select one student to update.", QMessageBox.StandardButton.Ok)

    def select_info(self):
        select_row = self.result_table.currentRow()
        if select_row != -1:
            self.employe_id.setEnabled(False)
            employe_id = self.result_table.item(select_row, 0).text().strip()
            fist_name = self.result_table.item(select_row, 1).text().strip()
            last_name = self.result_table.item(select_row, 2).text().strip()
            city = self.result_table.item(select_row, 3).text().strip()
            state = self.result_table.item(select_row, 4).text().strip()
            email_address = self.result_table.item(select_row, 5).text().strip()

            self.employe_id.setText(employe_id)
            self.first_name.setText(fist_name)
            self.last_name.setText(last_name)
            self.state.setCurrentText(state)
            self.city.setCurrentText(city)
            self.email_address.setText(email_address)
        else:
            QMessageBox.information(self, "Warning", "Please select one student information", QMessageBox.StandardButton.Ok)

    def search_info(self):
        self.update_state_city()
        student_info = self.get_student_info()

        search_result = self.db.search_info(
            Employe_id=student_info["employe_id"],
            first_name=student_info["first_name"],
            last_name=student_info["last_name"],
            email_address=student_info["email_address"],
            state=student_info["state"],
            city=student_info["city"]
        )

        self.show_data(search_result)

    def clear_form_info(self):
        self.update_state_city()
        self.employe_id.clear()
        self.employe_id.setEnabled(True)
        self.first_name.clear()
        self.last_name.clear()
        self.email_address.clear()
        self.state.setCurrentText("")
        self.city.setCurrentText("")
        self.search_info()

    def delete_info(self):
        select_row = self.result_table.currentRow()
        if select_row != -1:
            selected_option = QMessageBox.warning(self, "Warning", "Are you Sure to delete it?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)

            if selected_option == QMessageBox.StandardButton.Yes:
                employe_id = self.result_table.item(select_row, 0).text().strip()
                delete_result = self.db.delete_info(employe_id)

                if not delete_result:
                    self.search_info()
                else:
                    QMessageBox.information(self, "Warning", f"Fail to delete the information: {delete_result}. Please try again.", QMessageBox.StandardButton.Ok)
        else:
            QMessageBox.information(self, "Warning", "Please select one student information to delete", QMessageBox.StandardButton.Ok)

    def show_data(self, result):
        if result and not isinstance(result, str):
            self.result_table.setRowCount(0)
            self.result_table.setRowCount(len(result))

            for row, info in enumerate(result):
                info_list = [
                    info.get("employe_id", ""),
                    info.get("first_name", ""),
                    info.get("last_name", ""),
                    info.get("city", ""),
                    info.get("state", ""),
                    info.get("email_address", ""),
                ]

                for column, item in enumerate(info_list):
                    cell_item = QTableWidgetItem(str(item))
                    self.result_table.setItem(row, column, cell_item)
        else:
            self.result_table.setRowCount(0)

    def get_student_info(self):
        employe_id = self.employe_id.text().strip()
        first_name = self.first_name.text().strip()
        last_name = self.last_name.text().strip()
        email_address = self.email_address.text().strip()
        state = self.state.currentText().strip()
        city = self.city.currentText().strip()

        student_info = {
            "employe_id": employe_id,
            "first_name": first_name,
            "last_name": last_name,
            "email_address": email_address,
            "state": state,
            "city": city,
        }
        return student_info

    def check_student_id(self, employe_id):
        result = self.db.search_info(Employe_id=employe_id)
        return result

    def update_state_city(self):
        state_result = self.db.get_all_states()
        city_result = self.db.get_all_cities()

        current_state = self.state.currentText()
        current_city = self.city.currentText()

        self.state.clear()
        self.city.clear()

        state_list = [""]
        for item in state_result:
            if item.get('state'):
                state_list.append(item['state'])

        city_list = [""]
        for item in city_result:
            if item.get('city'):
                city_list.append(item['city'])

        self.state.addItems(state_list)
        self.city.addItems(city_list)
        
        self.state.setCurrentText(current_state)
        self.city.setCurrentText(current_city)

class EarningScreen(QDialog):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #121212; color: #e0e0e0;")
        from PyQt5.QtWidgets import QHBoxLayout, QFrame, QScrollArea

        outer = QVBoxLayout(self)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background: #121212;")
        inner = QWidget()
        inner.setStyleSheet("background: #121212;")
        layout = QVBoxLayout(inner)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 20, 40, 40)
        scroll.setWidget(inner)
        outer.addWidget(scroll)

        HOVER_BTN = "QPushButton { background: transparent; color: #10b981; font-size: 18px; text-align: left; border: none; padding: 4px; } QPushButton:hover { color: #34d399; padding-left: 10px; }"

        back = QPushButton("\u2190 Back to Dashboard")
        back.setStyleSheet(HOVER_BTN)
        back.clicked.connect(self.gotodash)
        layout.addWidget(back)

        title = QLabel("Financial Earnings & Revenue \u2014 DJ Namaste")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #ffffff;")
        layout.addWidget(title)

        kpi_row = QHBoxLayout()
        kpis = [
            ("\u20b9 Monthly Revenue", "\u20b93,54,375", "+12.4% vs last month"),
            ("\u20b9 Pending Payouts", "\u20b926,600", "-3.1% vs last month"),
            ("\u20b9 Net Profit", "\u20b92,36,480", "+8.7% margin"),
            ("\u20b9 Total GST Paid", "\u20b963,787", "Q2 FY2025"),
        ]
        for name, val, change in kpis:
            card = QFrame()
            card.setStyleSheet("background:#1e1e1e; border-radius:12px; padding:20px;")
            cl = QVBoxLayout(card)
            vl = QLabel(val); vl.setStyleSheet("font-size:32px; font-weight:bold; color:#10b981;")
            nl = QLabel(name); nl.setStyleSheet("font-size:13px; color:#a0a0a0;")
            cl2 = QLabel(change); cl2.setStyleSheet("font-size:12px; color:#34d399;")
            cl.addWidget(vl); cl.addWidget(nl); cl.addWidget(cl2)
            kpi_row.addWidget(card)
        layout.addLayout(kpi_row)

        q_title = QLabel("Quarterly Revenue Breakdown")
        q_title.setStyleSheet("font-size:20px; font-weight:bold; color:#ffffff;")
        layout.addWidget(q_title)
        q_row = QHBoxLayout()
        quarters = [
            ("Q1 (Jan\u2013Mar)", "\u20b97,82,500", "Plumbing & Cleaning"),
            ("Q2 (Apr\u2013Jun)", "\u20b99,45,000", "DJ Events Peak"),
            ("Q3 (Jul\u2013Sep)", "\u20b98,10,200", "Festive Season"),
            ("Q4 (Oct\u2013Dec)", "\u20b911,25,750", "Wedding Season"),
        ]
        for q, amt, note in quarters:
            card = QFrame()
            card.setStyleSheet("background:#1a1a2e; border-left:4px solid #10b981; border-radius:8px; padding:16px;")
            cl = QVBoxLayout(card)
            ql = QLabel(q); ql.setStyleSheet("font-size:13px; color:#888;")
            al = QLabel(amt); al.setStyleSheet("font-size:26px; font-weight:bold; color:#10b981;")
            nl = QLabel(note); nl.setStyleSheet("font-size:12px; color:#aaa;")
            cl.addWidget(ql); cl.addWidget(al); cl.addWidget(nl)
            q_row.addWidget(card)
        layout.addLayout(q_row)

        ct = QLabel("Monthly Revenue Trend (Hover to Inspect)")
        ct.setStyleSheet("font-size:18px; font-weight:bold; color:#ffffff;")
        layout.addWidget(ct)

        class HoverLineChart(QWidget):
            MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
            VALUES = [354375, 310000, 420000, 375000, 490000, 515000, 480000, 560000, 620000, 710000, 810000, 945750]
            def __init__(self):
                super().__init__()
                self.setMinimumHeight(280)
                self.setMouseTracking(True)
                self.hovered = -1
            def mouseMoveEvent(self, event):
                n = len(self.VALUES); dx = (self.width() - 60) / (n - 1)
                for i in range(n):
                    if abs(event.x() - (30 + i * dx)) < 20:
                        if self.hovered != i: self.hovered = i; self.update()
                        return
                if self.hovered != -1: self.hovered = -1; self.update()
            def leaveEvent(self, e): self.hovered = -1; self.update()
            def paintEvent(self, event):
                p = QPainter(self); p.setRenderHint(QPainter.Antialiasing)
                w, h = self.width(), self.height()
                p.fillRect(0, 0, w, h, QColor("#1e1e1e"))
                vals = self.VALUES; maxv = max(vals); n = len(vals); dx = (w - 60) / (n - 1)
                p.setPen(QPen(QColor("#2a2a2a"), 1))
                for i in range(1, 5):
                    gy = h - 30 - ((h - 50) / 4) * i
                    p.drawLine(30, int(gy), w - 10, int(gy))
                path = QPainterPath(); pts = []
                for i, v in enumerate(vals):
                    x = 30 + i * dx; y = h - 30 - (v / maxv) * (h - 50)
                    pts.append((x, y))
                    if i == 0: path.moveTo(x, y)
                    else: path.lineTo(x, y)
                p.setPen(QPen(QColor("#10b981"), 3)); p.drawPath(path)
                for i, (x, y) in enumerate(pts):
                    if i == self.hovered:
                        p.setBrush(QColor("#34d399")); p.setPen(QPen(QColor("#ffffff"), 2))
                        p.drawEllipse(QRectF(x-7, y-7, 14, 14))
                        p.setPen(QPen(QColor("#ffffff")))
                        p.drawText(int(x) - 30, int(y) - 14, f"\u20b9{vals[i]:,}")
                    else:
                        p.setBrush(QColor("#10b981")); p.setPen(Qt.NoPen)
                        p.drawEllipse(QRectF(x-4, y-4, 8, 8))
                    p.setPen(QPen(QColor("#666")))
                    p.drawText(int(x) - 10, h - 5, self.MONTHS[i])
                    p.setPen(Qt.NoPen)

        self.chart = HoverLineChart()
        layout.addWidget(self.chart)
        layout.addStretch()

    def gotodash(self):
        d = DashWindow()
        widget.addWidget(d)
        widget.setCurrentIndex(widget.currentIndex() + 1)
class AccountScreen(QDialog):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #121212;")
        layout = QVBoxLayout(self)
        
        self.back_btn = QPushButton("← Back to Dashboard")
        self.back_btn.setStyleSheet("background-color: transparent; color: #10b981; font-size: 18px; text-align: left;")
        self.back_btn.clicked.connect(self.gotodash)
        layout.addWidget(self.back_btn)
        
        title = QLabel("Admin Profile & Settings")
        title.setStyleSheet("font-size: 32px; font-weight: bold; color: #ffffff; margin-top: 20px;")
        layout.addWidget(title)
        
        card = QFrame()
        card.setStyleSheet("background-color: #1e1e1e; border-radius: 12px; padding: 40px;")
        cl = QFormLayout(card)
        cl.addRow(QLabel("Admin Name:"), QLabel("Sahil Singh (Superadmin)"))
        cl.addRow(QLabel("Email:"), QLabel("admin@djnamasta.com"))
        cl.addRow(QLabel("System Status:"), QLabel("All Systems Operational ✅"))
        cl.addRow(QLabel("Connected DB:"), QLabel("database.db (SQLite3)"))
        
        for i in range(cl.count()):
            w = cl.itemAt(i).widget()
            if w: w.setStyleSheet("font-size: 18px; color: #e0e0e0; padding: 10px;")
            
        layout.addWidget(card)
        layout.addStretch()
        
    def gotodash(self):
        d = DashWindow()
        widget.addWidget(d)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class ShowserviceData(QDialog):
    def __init__(self):
        super(ShowserviceData, self).__init__()
        loadUi("costumer.ui", self)
        self.setMinimumSize(1920, 1080)
        self.setStyleSheet("background-color: #121212;")
        self.dashborad_btn_6.clicked.connect(self.gotodash)
        self.ser3_3.clicked.connect(self.gotosql)
        
        # Fill empty placeholder with real content
        if hasattr(self, 'result_frame'):
            self.result_frame.setGeometry(270, 360, 1600, 700)
            
            container = QWidget(self)
            container.setGeometry(270, 172, 1600, 180)
            layout = QVBoxLayout(container)
            
            title = QLabel("Customer & Service Analytics")
            title.setStyleSheet("font-size: 24px; font-weight: bold; color: #10b981; margin-bottom: 20px;")
            layout.addWidget(title)
            
            # Add some mock stat cards in a horizontal layout
            from PyQt5.QtWidgets import QHBoxLayout, QFrame
            hlayout = QHBoxLayout()
            
            for stat_name, stat_val in [("Total Customers", "1,248"), ("Active Services", "42"), ("Pending Tickets", "7")]:
                card = QFrame()
                card.setStyleSheet("background-color: #242424; border-radius: 8px; padding: 20px;")
                card_layout = QVBoxLayout(card)
                lbl_val = QLabel(stat_val)
                lbl_val.setStyleSheet("font-size: 32px; font-weight: bold; color: #ffffff;")
                lbl_name = QLabel(stat_name)
                lbl_name.setStyleSheet("font-size: 14px; color: #a0a0a0;")
                card_layout.addWidget(lbl_val)
                card_layout.addWidget(lbl_name)
                hlayout.addWidget(card)
                
            layout.addLayout(hlayout)
            layout.addStretch()
        
    def gotodash(self):
        dashbrd2 = DashWindow()
        widget.addWidget(dashbrd2)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        
    def gotosql(self):
        sql1 = ShowData()
        widget.addWidget(sql1)
        widget.setCurrentIndex(widget.currentIndex() + 1)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    splash = SplashScreen()
    splash.show()
    splash.progress()
    MainWindow1 = DashWindow()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(MainWindow1)
    
    # Wrap in ScrollArea to prevent cut-offs on small screens
    from PyQt5.QtWidgets import QScrollArea
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setWidget(widget)
    scroll.setStyleSheet("border: none; background-color: #121212;")
    
    # Apply modern stylesheet to the main widget
    try:
        with open("style.qss", "r") as f:
            widget.setStyleSheet(f.read())
    except Exception as e:
        print("Could not load style.qss:", e)

    scroll.showMaximized()
    splash.finish(scroll)
    app.exec_()

