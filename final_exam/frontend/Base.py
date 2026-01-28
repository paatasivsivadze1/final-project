from PyQt5 import QtWidgets, QtCore


class BasePage(QtWidgets.QWidget):
    """
        ეს კლასი არის ყველა სხვა კლასის მშობელი საიდანაც მოდის ძირითადი style-ები და მეთოდები რომლებსაც სხვადასხვაგან ვიყენებ
    """
    def __init__(self, app=None):
        super().__init__()
        self.app = app
        self.current_theme = "light"

    @staticmethod
    def button_style():
        """
        მეთოდი რომელშიც ინახება ღილაკების style
        """
        return """
            QPushButton {
                font-size: 15px;
                background-color: #5dade2;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #3498db;
            }
        """

    @staticmethod
    def dark_theme():
        """
        მეთოდი რომელშიც ინახება dark mode-ის style
        """
        return """
        QWidget {
            background-color: #121212;
            color: #eaeaea;
            font-family: Arial;
        }

        QLineEdit {
            font-size: 14px;
            background-color: #1e1e1e;
            color: white;
            border: 2px solid #555;
            border-radius: 5px;
            padding: 5px;
        }

        QPushButton {
            background-color: #2980b9;
            color: white;
            border-radius: 5px;
            padding: 6px;
        }

        QPushButton:hover {
            background-color: #1f618d;
        } 
        QTabBar::tab {
            border: 1px solid #2980b9;
        }
        QHeaderView::section {
            font-size: 21px;
            background-color: #5dade2;
            color: black;
        }
        QTableWidget {
            background-color: #1e1e1e;   
            gridline-color: #555;
            color: white;                  
            font-size: 19px;
            font-weight: bold;
        }
        QTabWidget::pane {
            border: 1px solid white;
        }
        QComboBox {
            border: 2px solid #555;
            border-radius: 5px;
        }
        QLabel {
            font-size: 25px;
            font-weight: bold;
            color: #5dade2;
            padding-bottom: 20px;
        }
        QTabBar::tab {
            height: 30px;
            width: 140px;
            font-size: 14px;
        }
        QTabBar::tab:selected {
            background: #5dade2;
            color: white;
        }
        QComboBox {
            font-size: 15px;
            color: white;
            border-radius: 5px;
            padding: 5px;
        } 
    """
    @staticmethod
    def light_theme():
        """
        მეთოდი რომელსიც ინახება light mode-ის style
        """
        return """
        QWidget {
            background-color: #f4f6f7;
            color: #2c3e50;
            font-family: Arial;
        }
        QLabel {
            font-size: 25px;
            font-weight: bold;
            color: #5dade2;
            padding-bottom: 20px;
        }
        QLineEdit {
            font-size: 14px;
            border: 2px solid #aaa;
            border-radius: 5px;
            border-color: rgb(0, 0, 0);
        }

        QPushButton {
            background-color: #5dade2;
            color: white;
            border-radius: 5px;
            padding: 6px;
        }

        QPushButton:hover {
            background-color: #3498db;
        }

        QTabWidget::pane {
            border: 1px solid #ccc;
        }
        QTableWidget {
            font-size: 19px;
            background: white;
        }
        QTabBar::tab {
            height: 30px;
            width: 140px;
            font-size: 14px;
        }
        QTabBar::tab:selected {
            background: #5dade2;
            color: white;
        }

        QTabBar::tab {
            height: 30px;
            width: 140px;
            font-size: 14px;
        }
        QTabBar::tab:selected {
            background: #5dade2;
            color: white;
        }
        QHeaderView::section {
            font-weight: bold;
            font-size: 21px;
            background-color: #5dade2;
            color: white;
        }

        QComboBox {
            font-size: 15px;
            background-color: #5dade2;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 5px;
        } 
    """

    def toggle_theme(self):
        """
            მეთოდი რომელსიც ინახება light mode-ისა და dark mode-ის შეცვლის ლოგიკა
        """
        if self.current_theme == "light":
            self.app.setStyleSheet(self.dark_theme())
            self.current_theme = "dark"
        else:
            self.app.setStyleSheet(self.light_theme())
            self.current_theme = "light"

    @staticmethod
    def add_to_table(data, table):
        """
            მეთოდი რომელიც ამატებს ინფორმაციას ცხრილში
        """
        if not data: return
        row = table.rowCount()
        table.insertRow(row)
        for col, value in enumerate(data):
            if col < table.columnCount():
                item = QtWidgets.QTableWidgetItem(str(value) if value is not None else "")
                table.setItem(row, col, item)
    @staticmethod
    def search(search_input, table, index=0):
        """
            მეთოდი რომელიც ეძებს ინფორმაციას ცხრილში
        """
        search_text = search_input.text().strip().lower()
        for row in range(table.rowCount()):
            subject_item = table.item(row, index)
            if subject_item is not None:
                subject_name = subject_item.text().lower()
                table.setRowHidden(row, search_text not in subject_name)

    @staticmethod
    def apply_input_style(widget):
        widget.setMinimumHeight(40)
        widget.setMaximumWidth(400)
        widget.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)


    def create_lineedit(self, placeholder):
        """
            მეთოდი რომელიც ქმნის ჩასაწერ სივრცეს(lineedit)
        """
        lineedit = QtWidgets.QLineEdit()
        lineedit.setPlaceholderText(placeholder)
        self.apply_input_style(lineedit)
        return lineedit
