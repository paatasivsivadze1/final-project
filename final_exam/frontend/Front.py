from PyQt5 import QtWidgets, QtCore
from frontend.Base import BasePage
from frontend.Stars import StarRatingWidget



class LoginRegisterPage(BasePage):
    """
        ეს არის პირველი გვერდის კლასი სადაც ნაჩვენებია login და register
    """
    def __init__(self, stacked, app=None):
        super().__init__(app)
        self.Login_Register_Page = QtWidgets.QWidget()

        self.Login_Register_Page.setObjectName("Login_Register")
        self.Login_Register_Page.setWindowTitle("Login_Register")

        self.stacked = stacked
        self.build_ui()

    def build_ui(self):
        title = QtWidgets.QLabel("Login or Register")
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        login_button = QtWidgets.QPushButton("Login")
        login_button.setFixedSize(400, 40)
        login_button.setStyleSheet(self.button_style())

        register_button = QtWidgets.QPushButton("Register")
        register_button.setFixedSize(400, 40)

        register_button.setStyleSheet(self.button_style())

        inner_layout = QtWidgets.QVBoxLayout(self.Login_Register_Page)
        inner_layout.setSpacing(40)
        inner_layout.addWidget(title)
        inner_layout.addWidget(login_button)
        inner_layout.addWidget(register_button)
        inner_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addStretch()
        main_layout.addLayout(inner_layout)
        main_layout.addStretch()
        main_layout.setContentsMargins(0, 100, 0, 0)

        theme_button = QtWidgets.QPushButton(" Dark / Light")
        theme_button.setFixedSize(200, 40)
        theme_button.clicked.connect(self.toggle_theme)
        inner_layout.addWidget(theme_button)
        main_layout.addWidget(theme_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        login_button.clicked.connect(lambda: self.stacked.setCurrentIndex(1))
        register_button.clicked.connect(lambda: self.stacked.setCurrentIndex(2))

        return self.Login_Register_Page


class LoginPage(BasePage):
    """
        ეს კლასი ქმნის login-ის გვერდს
    """
    login_attempted = QtCore.pyqtSignal(str, str)

    def __init__(self, stacked, app=None):
        super().__init__(app)
        self.stacked = stacked
        self.Login_page = QtWidgets.QWidget()
        self.Login_page.setObjectName("Login_Page")
        self.Login_page.setWindowTitle("Login")
        self.build_ui()

    def build_ui(self):
        login_title_label = QtWidgets.QLabel("Log-in")
        login_title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.login_email_input = self.create_lineedit("Email")
        self.login_password_input = self.create_lineedit("Password")
        self.login_password_input.setEchoMode(QtWidgets.QLineEdit.Password)

        login_button = QtWidgets.QPushButton("Login")
        login_button.setFixedSize(400, 40)
        login_button.setStyleSheet(self.button_style())

        register_button = QtWidgets.QPushButton("Register")
        register_button.setFixedSize(200, 40)
        register_button.setStyleSheet(self.button_style())

        theme_button = QtWidgets.QPushButton(" Dark /  Light")
        theme_button.setFixedSize(100, 40)
        theme_button.clicked.connect(self.toggle_theme)

        inner_layout = QtWidgets.QVBoxLayout()
        inner_layout.addWidget(self.login_email_input)
        inner_layout.addWidget(self.login_password_input)
        inner_layout.setSpacing(30)
        inner_layout.addWidget(login_button)
        inner_layout.addWidget(register_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        inner_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        wrapper = QtWidgets.QWidget()
        wrapper.setLayout(inner_layout)

        main_layout = QtWidgets.QVBoxLayout(self.Login_page)
        main_layout.addWidget(theme_button)
        main_layout.addWidget(login_title_label)
        main_layout.addStretch()
        main_layout.addWidget(wrapper, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        main_layout.addStretch()
        register_button.clicked.connect(lambda: self.stacked.setCurrentIndex(2))
        login_button.clicked.connect(self.send_login_data)
        return self.Login_page

    def send_login_data(self):
        """
            მონაცემებს, რომლის საშუალებითაც მომხმარებელმა გაიარა ავტორიზაცია, ვუგზავნი ბექენდს
        """
        email = self.login_email_input.text()
        print(f"DEBUG: Button clicked! Email: {email}")  # <--- დაამატე ეს
        password = self.login_password_input.text().strip()
        if email and password:
            self.login_attempted.emit(email, password)


class RegisterPage(BasePage):
    """
        ეს კლასი ქმნის register გვერდს
    """
    register_attempted = QtCore.pyqtSignal(str, str,str,str,int,str)

    def __init__(self, stacked, app=None):
        super().__init__(app)

        self.Register_page = QtWidgets.QWidget()
        self.Register_page.setObjectName("Register_Page")
        self.Register_page.setWindowTitle("Register")

        self.register_title_label = QtWidgets.QLabel("Register")
        self.register_title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.register_name_input = self.create_lineedit("Name")
        self.register_lastname_input = self.create_lineedit("LastName")
        self.register_email_input = self.create_lineedit("Email")
        self.register_password_input = self.create_lineedit("Password")
        self.register_age_input = self.create_lineedit("age")
        self.register_address_input = self.create_lineedit("City, Street")

        self.stacked = stacked
        self.build_ui()

    def build_ui(self):
        register_button = QtWidgets.QPushButton("Register")
        register_button.setFixedSize(400, 40)
        register_button.setStyleSheet(self.button_style())

        login_button = QtWidgets.QPushButton("Log-in")
        login_button.setFixedSize(200, 40)
        login_button.setStyleSheet(self.button_style())

        theme_button = QtWidgets.QPushButton(" Dark /  Light")
        theme_button.setFixedSize(200, 40)
        theme_button.clicked.connect(self.toggle_theme)

        inner_layout = QtWidgets.QVBoxLayout(self.Register_page)
        inner_layout.setSpacing(40)

        inner_layout.addWidget(self.register_name_input)
        inner_layout.addWidget(self.register_lastname_input)
        inner_layout.addWidget(self.register_email_input)
        inner_layout.addWidget(self.register_password_input)
        inner_layout.addWidget(self.register_age_input)
        inner_layout.addWidget(self.register_address_input)
        inner_layout.addWidget(register_button)

        inner_layout.addWidget(login_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        inner_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        wrapper_conteiner = QtWidgets.QWidget()
        wrapper_conteiner.setLayout(inner_layout)

        main_layout = QtWidgets.QVBoxLayout(self.Register_page)
        main_layout.addWidget(theme_button)
        main_layout.addWidget(self.register_title_label)
        main_layout.addStretch()
        main_layout.addWidget(wrapper_conteiner, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        main_layout.addStretch()
        main_layout.setContentsMargins(0, 50, 0, 0)


        register_button.clicked.connect(self.send_register_data)
        login_button.clicked.connect(lambda: self.stacked.setCurrentIndex(1))
        return self.Register_page

    def send_register_data(self):
        """
            მონაცემებს, რომლის საშუალებითაც მომხმარებელმა გაიარა რეგისტრაცია, ვუგზავნი ბექენდს
        """
        first_name = self.register_name_input.text()
        last_name = self.register_lastname_input.text()
        email = self.register_email_input.text()
        password = self.register_password_input.text()
        age = self.register_age_input.text()
        address = self.register_address_input.text()

        self.register_attempted.emit(first_name, last_name,email,password,age,address)

class PersonalInfoTab(BasePage):
    """
        ეს კლაცი ქმნის პერსონალური ინფორმაციის ტაბს სადაც არის მომხმარებლის პირადი ინფორმაცია და ცხრილი
    """
    review_submitted = QtCore.pyqtSignal(int, int, str)
    def __init__(self,data,table_data,show_lecturer, role, app=None):
        super().__init__(app)
        self.app = app
        self.data = data
        self.role = role
        self.table_data = table_data
        if show_lecturer:
            self.show_lecturer = show_lecturer
        else:
            self.show_lecturer = [("None",1),("None",2)]

        if data:
            if len(data) >= 7:
                self.name, self.last_name, self.email, self.age, self.address, self.semester, self.credit = data
            else:
                self.name, self.last_name, self.email, self.age, self.address = data[:5]
        else:
            self.name = self.last_name = self.email = self.address = ""
            self.age = 0

        self.name_info = QtWidgets.QLabel(self.name)
        self.lastname_info = QtWidgets.QLabel(self.last_name)
        self.email_info = QtWidgets.QLabel(self.email)
        self.age_info = QtWidgets.QLabel(str(self.age))
        self.address_info = QtWidgets.QLabel(self.address)
        if self.role != "lecturer":
            self.semester_info = QtWidgets.QLabel(str(self.semester))
            self.credit_info = QtWidgets.QLabel(str(self.credit))

        self.lecturer_feedback_title = QtWidgets.QLabel("-ლექტორების შეფასება-")
        self.lecturer_feedback = QtWidgets.QTextEdit()
        self.lecturer_feedback.setPlaceholderText("ლექტორების შეფასება")
        self.lecturer_feedback.setStyleSheet("font-size: 18px;")
        self.lecturer_feedback.setMaximumHeight(200)

        self.title = QtWidgets.QLabel("Personal Information")
        self.title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("font-size: 35px; font-weight: bold;")

        self.theme_button = QtWidgets.QPushButton(" Dark /  Light")
        self.theme_button.setFixedSize(200, 40)
        self.theme_button.clicked.connect(self.toggle_theme)

        self.star_rating = StarRatingWidget()

        self.tab = QtWidgets.QWidget()
        self.init_ui()

    def init_ui(self):
        main_layout = QtWidgets.QVBoxLayout(self.tab)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        title_layout = QtWidgets.QHBoxLayout()
        title_layout.addWidget(self.title)
        title_layout.addWidget(self.theme_button)

        self.lecturer_combobox = QtWidgets.QComboBox()
        self.lecturer_combobox.setEditable(False)
        self.lecturer_combobox.setMinimumWidth(250)
        self.lecturer_combobox.setStyleSheet("""
                QComboBox {
                    padding: 6px;
                    font-size: 14px;
                }
            """)

        for lector, l_id in self.show_lecturer:
            self.lecturer_combobox.addItem(lector, l_id)

        for lbl in [self.name_info, self.lastname_info, self.age_info, self.email_info,
                    self.address_info]:  # -------------------------------------------
            lbl.setStyleSheet("font-size: 20px; font-weight: bold; color: #3498DB;")
            lbl.setFixedHeight(50)

        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow("სახელი:", self.name_info)
        form_layout.addRow("გვარი:", self.lastname_info)
        form_layout.addRow("ასაკი:", self.age_info)
        form_layout.addRow("Email:", self.email_info)
        form_layout.addRow("მისამართი:", self.address_info)
        if self.role != "lecturer":
            form_layout.addRow("სემესტრი:",self.semester_info)
            form_layout.addRow("მიმდინარე კრედიტები:", self.credit_info)
            form_layout.addRow(self.lecturer_feedback_title)
            self.lecturer_feedback_title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            form_layout.addRow(self.lecturer_combobox, self.lecturer_feedback)
            form_layout.setVerticalSpacing(10)


            form_layout.addRow(self.star_rating)
            send_button = QtWidgets.QPushButton("გაგზავნა")
            send_button.setStyleSheet(self.button_style())
            form_layout.addRow(send_button)
            send_button.clicked.connect(self.on_send)
        else:

            form_layout.setVerticalSpacing(60)
            form_layout.setContentsMargins(20, 40, 20, 40)
            for lbl in [self.name_info, self.lastname_info, self.age_info, self.email_info, self.address_info]:
                lbl.setStyleSheet("font-size: 22px; font-weight: bold; margin-bottom: 5px;")

        self.table = QtWidgets.QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(["დღე", "საგანი", "ლექტორი", "ჯგუფი", "დრო", "შეფასება"])
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        content_layout = QtWidgets.QHBoxLayout()

        left_widget = QtWidgets.QWidget()
        left_widget.setLayout(form_layout)
        if self.role == "lecturer":
            left_widget.setStyleSheet("""
                QWidget {
                    background-color: #F0F0F0;
                    border-radius: 10px;       
                }
                QLabel {
                    background-color: transparent;
                }
            """)
            content_layout.setContentsMargins(0, 50, 0, 0)


        content_layout.addWidget(left_widget, 1)
        content_layout.addWidget(self.table, 2)

        main_layout.addLayout(title_layout)
        main_layout.addLayout(content_layout)

        if self.table_data:
            for row in self.table_data:
                self.add_to_table(row,self.table)


        self.apply_role_rules()


        return self.tab

    def on_send(self):
        """
            ბექენდ ვუგზავნი ლექტორის შეფასებას
        """
        feedback_text = self.lecturer_feedback.toPlainText()
        rating = self.star_rating.get_rating()


        lecturer_id = self.lecturer_combobox.currentData()

        if lecturer_id is None:
            QtWidgets.QMessageBox.warning(self.tab, "შეცდომა", "გთხოვთ, აირჩიოთ ლექტორი!")
            return

        self.review_submitted.emit(int(lecturer_id), int(rating), feedback_text)

        self.lecturer_feedback.clear()
        self.star_rating.set_rating(0)

    def apply_role_rules(self):
        """
            ამ მეთოდის საშუალებიით, ცხრილში იმალება რამდენიმე სვეტი იმ შემთხვევაში თუ ლექტორი შედის
        """
        if self.role == "lecturer":
            self.table.setColumnHidden(2, True)
            self.table.setColumnHidden(5, True)

        elif self.role == "student":
            self.table.setColumnHidden(5, False)

    def update_schedule_table(self, row_data):
        """ეს მეთოდი დაამატებს ახალ ხაზს პირველ ცხრილში"""
        if not row_data:
            return
        row = self.table.rowCount()
        self.table.insertRow(row)
        for col, value in enumerate(row_data):
            item = QtWidgets.QTableWidgetItem(str(value) if value is not None else "-")
            self.table.setItem(row, col, item)



class ChooseSubjectsTab(BasePage):
    """
        ეს კლასი ქმნის პერსონალური ინფორმაციის ტაბს სადაც არის სტუდენტს შეუძლია საგნების არჩევა
    """
    subject_added = QtCore.pyqtSignal(list)

    def __init__(self, subject_data,change_subject, app=None):
        super().__init__(app)
        self.app = app
        self.tab = QtWidgets.QWidget()
        self.subject_data = subject_data
        self.change_subject = change_subject
        self.subject_combos = {}
        self.init_ui()

    def init_ui(self):
        main_layout = QtWidgets.QHBoxLayout(self.tab)
        main_layout.setSpacing(40)
        main_layout.setContentsMargins(40, 30, 40, 30)

        # --------------------მარცხენა მხარე--------------------------

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QtWidgets.QFrame.NoFrame)
        scroll.setFixedWidth(480)

        left_widget = QtWidgets.QWidget()
        left_layout = QtWidgets.QVBoxLayout(left_widget)
        left_layout.setSpacing(25)

        title = QtWidgets.QLabel("Choose Subjects")
        left_layout.addWidget(title)

        for subject, options in self.subject_data.items():
            left_row = QtWidgets.QHBoxLayout()

            subjects_lbl = QtWidgets.QLabel(subject)
            subjects_lbl.setMinimumWidth(110)
            subjects_lbl.setStyleSheet("""
                font-size: 19px;
            """)

            combo_box = QtWidgets.QComboBox()
            combo_box.setMinimumWidth(250)
            combo_box.setStyleSheet("""
                QComboBox {
                    padding: 6px;
                    font-size: 14px;
                }
            """)
            combo_box.setEditable(False)
            combo_box.addItem("აირჩიეთ...", None)

            for option in options:
                (lecturer, group), s_id = option
                combo_box.addItem(f"{lecturer} – {group}", (subject, lecturer, group, s_id))

            combo_box.currentIndexChanged.connect(
                lambda _, c=combo_box: self.add_subject_to_table(c)
            )
            combo_box.setEditable(False)
            combo_box.setInsertPolicy(QtWidgets.QComboBox.NoInsert)

            left_row.addWidget(subjects_lbl)
            left_row.addWidget(combo_box)
            left_layout.addLayout(left_row)

            self.subject_combos[subject] = combo_box

        left_layout.addStretch()
        scroll.setWidget(left_widget)

        # --------------------მარჯვენა მხარე--------------------------
        right_widget = QtWidgets.QWidget()
        right_layout = QtWidgets.QVBoxLayout(right_widget)

        theme_button = QtWidgets.QPushButton(" Dark /  Light")
        theme_button.setFixedSize(200, 40)
        theme_button.clicked.connect(self.toggle_theme)

        right_layout.addWidget(theme_button, alignment=QtCore.Qt.AlignmentFlag.AlignRight)

        self.table = QtWidgets.QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(
            ["საგანი", "ლექტორი", "ჯგუფი"]
        )
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        table_header = self.table.horizontalHeader()
        table_header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        table_header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        table_header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)

        if self.change_subject:
            for row in self.change_subject:
                self.add_to_table(row,self.table)

        right_layout.addWidget(self.table)

        # -----------------გაერთიანება--------------------------
        main_layout.addWidget(scroll, 1)
        main_layout.addWidget(right_widget)

        return self.tab

    def add_subject_to_table(self, combo):
        """
            არჩეული საგანი გამოჩნდეს ცხრილში და ინფორმაცია გაიგზავნოს ბექენდში (მონაცემთა ბაზაში)
        :param combo: combobox რომელშიც ჩაწერილია ლექტორი და ჯფუფი(რაც ჩანს)
        :return: ინფორმაცია იგზავნება ბექენდში (მონაცემთა ბაზაში)
        """
        index = combo.currentIndex()
        data = combo.itemData(index) #საგანი, ლექტორი, ჯგუფი, id

        old_id = combo.property("old_id")
        subject_name = combo.property("subject_name")

        if index == 0:
            if old_id is not None:
                for r in range(self.table.rowCount()):
                    if self.table.item(r, 0).text() == subject_name:
                        self.table.removeRow(r)
                        break
                self.subject_added.emit([subject_name, "", "", old_id, False])
                combo.setProperty("old_id", None)
            return

        subject, lecturer, group, s_id = data

        if old_id == s_id:
            QtWidgets.QMessageBox.information(self.tab, "ინფორმაცია", "ეს საგანი ამ ლექტორით უკვე არჩეული გაქვთ.")
            return

        if old_id is not None and old_id != s_id:
            self.subject_added.emit([subject, "", "", old_id, False])

        combo.setProperty("old_id", s_id)
        combo.setProperty("subject_name", subject)

        found_row = -1
        for row in range(self.table.rowCount()):
            if self.table.item(row, 0).text() == subject:
                found_row = row
                break

        if found_row != -1:
            self.table.setItem(found_row, 1, QtWidgets.QTableWidgetItem(str(lecturer)))
            self.table.setItem(found_row, 2, QtWidgets.QTableWidgetItem(str(group)))
        else:
            row_pos = self.table.rowCount()
            self.table.insertRow(row_pos)
            self.table.setItem(row_pos, 0, QtWidgets.QTableWidgetItem(str(subject)))
            self.table.setItem(row_pos, 1, QtWidgets.QTableWidgetItem(str(lecturer)))
            self.table.setItem(row_pos, 2, QtWidgets.QTableWidgetItem(str(group)))

        self.subject_added.emit([subject, lecturer, group, int(s_id), True])

class ChangeScoreTab(BasePage):
    """
        ეს კლასი ქმნის ტაბს ლექტორისთვის,სადაც შესაძლებელია სტუდენტის ქულის შეცვლა
    """
    score_updated = QtCore.pyqtSignal(int,int,int)
    def __init__(self, show_students,app=None):
        super().__init__(app)

        self.show_students = show_students

        self.search_subject = QtWidgets.QLineEdit()
        self.search_subject.setPlaceholderText("საგანი")
        self.search_group = QtWidgets.QLineEdit()
        self.search_group.setPlaceholderText("სტუდენტის სახელი")
        self.search_student = QtWidgets.QLineEdit()
        self.search_student.setPlaceholderText("ჯგუფის ნომერი")

        self.score_table = QtWidgets.QTableWidget(0, 4)
        self.score_table.setHorizontalHeaderLabels(
            ["საგანი", "სტუდენტი", "ჯგუფის ნომერი", "შეფასება"]
        )
        self.tab = QtWidgets.QWidget()
        self.build_ui()

    def build_ui(self):
        main_layout = QtWidgets.QVBoxLayout(self.tab)
        main_layout.setSpacing(25)
        main_layout.setContentsMargins(40, 30, 40, 30)

        theme_button = QtWidgets.QPushButton(" Dark /  Light")
        theme_button.setFixedSize(200, 40)
        theme_button.clicked.connect(self.toggle_theme)

        title = QtWidgets.QLabel("Change Score")
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold;")

        search_layout = QtWidgets.QHBoxLayout()
        search_layout.setSpacing(20)

        for le in (self.search_subject, self.search_student, self.search_group):
            self.apply_input_style(le)
            le.textChanged.connect(self.filter_score_table)

        search_layout.addWidget(self.search_subject)
        search_layout.addWidget(self.search_group)
        search_layout.addWidget(self.search_student)

        search_layout.addWidget(theme_button)
        main_layout.addWidget(title)
        main_layout.addLayout(search_layout)

        self.score_table.setEditTriggers(
            QtWidgets.QAbstractItemView.DoubleClicked |
            QtWidgets.QAbstractItemView.SelectedClicked
        )

        header = self.score_table.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        main_layout.addWidget(self.score_table)

        for info_tuple, ids_tuple in self.show_students:

            self.add_to_table(info_tuple, self.score_table)

            last_row = self.score_table.rowCount() - 1
            item = self.score_table.item(last_row, 0)

            if item:
                item.setData(QtCore.Qt.UserRole, ids_tuple)

        self.score_table.itemChanged.connect(self.item_changed)
        return self.tab

    def item_changed(self, item):
        """
            ეს მეთოდი ბექენდს უგზავნის იმ სტუდენტის id-სა და ქულას, რომლის ქულაც შეიცვალა(და ერორსაც გამოიტანს თუ ქულა არასწორადაა შეყვანილი)
        :param item არის სტუდენტის შეფასება(უნდა იყოს)
        """
        if item.column() != 3:
            return

        self.score_table.blockSignals(True)

        try:
            row = item.row()
            score_text = item.text().strip()
            subj_item = self.score_table.item(row, 0)
            score_item = self.score_table.item(row, 3)

            if not subj_item or not score_item:
                return

            score_text = item.text()
            if not score_text.replace('-', '', 1).isdigit():
                QtWidgets.QMessageBox.warning(self.tab,"არასწორი ქულა","ქულა უნდა იყოს რიცხვი")
                item.setText("0")

            grade = int(score_text)

            if grade > 100:
                QtWidgets.QMessageBox.warning(self.tab, "არასწორი ქულა", "ქულა არ შეიძლება იყოს 100-ზე მეტი!")
                item.setText("0")

            elif grade < 0:
                QtWidgets.QMessageBox.warning(self.tab, "არასწორი ქულა", "ქულა არ შეიძლება იყოს 0-ზე ნაკლები!")
                item.setText("0")

            ids_tuple = subj_item.data(QtCore.Qt.UserRole)
            new_score = score_item.text().strip()

            st_id, group_id = ids_tuple
            grade = int(new_score)

            self.score_updated.emit(group_id,st_id,grade)

        except Exception as e:
            print(f"UI Error: {e}")
        finally:
            self.score_table.blockSignals(False)

    def filter_score_table(self):
        """
        ეს არის search მეთოდი
        """
        subject_query = self.search_subject.text().strip().lower()
        student_query = self.search_group.text().strip().lower()
        group_query = self.search_student.text().strip().lower()

        self.score_table.setUpdatesEnabled(False)

        try:
            for row in range(self.score_table.rowCount()):

                subj_item = self.score_table.item(row, 0)
                stud_item = self.score_table.item(row, 1)
                grp_item = self.score_table.item(row, 2)

                subj_val = subj_item.text().lower() if subj_item else ""
                stud_val = stud_item.text().lower() if stud_item else ""
                grp_val = grp_item.text().lower() if grp_item else ""

                match = (subject_query in subj_val) and (student_query in stud_val) and (group_query in grp_val)

                self.score_table.setRowHidden(row, not match)
        finally:
            self.score_table.setUpdatesEnabled(True)


class InformationManagementTab(BasePage):
    """
        ეს კლასი ქმნის ტაბს ადმინისთვის,სადაც შესაძლებელია სტუდენტის, ლექტორის ან ადმინის დამატება, წაშლა და მათი ინფორმაციის შეცვლა
    """
    user_added_signal = QtCore.pyqtSignal(tuple)
    user_update_signal = QtCore.pyqtSignal(int, str,str,str,str,int,str,str)
    user_deleted_signal = QtCore.pyqtSignal(int)

    def __init__(self, show_all_users,app=None):
        super().__init__(app)

        self.show_all_users = show_all_users

        self.first_name = self.create_lineedit("სახელი")
        self.last_name = self.create_lineedit("გვარი")
        self.email = self.create_lineedit("Email")
        self.password = self.create_lineedit("პაროლი")
        self.age = self.create_lineedit("ასაკი")
        self.address = self.create_lineedit("მისამართი")
        self.id = self.create_lineedit("ID")
        self.id.setReadOnly(True)

        self.role = QtWidgets.QComboBox()
        self.role.addItem("student")
        self.role.addItem("admin")
        self.role.addItem("lecturer")

        self.btn_add = QtWidgets.QPushButton("➕ Add")
        self.btn_update = QtWidgets.QPushButton("🔄 Update")
        self.btn_select = QtWidgets.QPushButton("✔ Select")
        self.btn_search = QtWidgets.QPushButton("🔍 Search")
        self.btn_delete = QtWidgets.QPushButton("🗑 Delete")

        self.table = QtWidgets.QTableWidget(0, 8)
        self.table.setHorizontalHeaderLabels(
            ["First Name", "Last Name", "Age", "Email", "Password", "Address", "Role", "ID"]
        )

        self.tab = QtWidgets.QWidget()
        self.build_ui()

    def build_ui(self):
        main_layout = QtWidgets.QVBoxLayout(self.tab)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(30, 20, 30, 20)

        title = QtWidgets.QLabel("Information Management")
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold;")
        main_layout.addWidget(title)

        form_layout = QtWidgets.QGridLayout()
        form_layout.setHorizontalSpacing(30)
        form_layout.setVerticalSpacing(15)

        for w in [self.first_name, self.last_name, self.age, self.address, self.email, self.password, self.id]:
            self.apply_input_style(w)

        form_layout.addWidget(QtWidgets.QLabel("First Name"), 0, 0)
        form_layout.addWidget(self.first_name, 0, 1)

        form_layout.addWidget(QtWidgets.QLabel("Email"), 0, 2)
        form_layout.addWidget(self.email, 0, 3)

        form_layout.addWidget(QtWidgets.QLabel("Last Name"), 1, 0)
        form_layout.addWidget(self.last_name, 1, 1)

        form_layout.addWidget(QtWidgets.QLabel("Password"), 1, 2)
        form_layout.addWidget(self.password, 1, 3)

        form_layout.addWidget(QtWidgets.QLabel("Age"), 2, 0)
        form_layout.addWidget(self.age, 2, 1)

        form_layout.addWidget(QtWidgets.QLabel("Address"), 2, 2)
        form_layout.addWidget(self.address, 2, 3)

        form_layout.addWidget(QtWidgets.QLabel("ID"), 3, 0)
        form_layout.addWidget(self.id, 3, 1)

        form_layout.addWidget(QtWidgets.QLabel("Role"), 3, 2)
        form_layout.addWidget(self.role, 3, 3)

        main_layout.addLayout(form_layout)

        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.setSpacing(15)

        for btn in [self.btn_add, self.btn_update, self.btn_select, self.btn_search, self.btn_delete]:
            btn.setStyleSheet(self.button_style())
            btn_layout.addWidget(btn)

        self.btn_delete.setStyleSheet(self.button_style() + "QPushButton { background-color: red; }")
        btn_layout.setContentsMargins(0, 40, 0, 40)
        main_layout.addLayout(btn_layout)

        self.table.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch
        )
        self.table.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows
        )
        self.table.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers
        )
        main_layout.addWidget(self.table)

        for row in self.show_all_users:
            self.add_to_table(row, self.table)

        self.btn_add.clicked.connect(self.add_user)
        self.btn_update.clicked.connect(self.update_student)
        self.btn_select.clicked.connect(self.select_student)
        self.btn_delete.clicked.connect(self.delete_student)
        self.btn_search.clicked.connect(lambda: self.search(self.first_name, self.table, 0))

        return self.tab

    def add_user(self):
        """
        ბექენდს(მონაცემთა ბაზას) უგზავნის იმ სტუდენტის,ლექტორის ან ადმინის ინფორმაციას, რომელიც უნდა დაემატოს მონაცემთა ბაზაში
        """
        data = (
            self.first_name.text(),
            self.last_name.text(),
            self.age.text(),
            self.email.text(),
            self.password.text(),
            self.address.text(),
            self.role.currentText(),
        )

        if not data[0] or not data[1] or not data[2] or not data[3] or not data[4] or not data[5]:
            return

        self.user_added_signal.emit(data)

        self.first_name.clear()
        self.last_name.clear()
        self.email.clear()
        self.password.clear()
        self.age.clear()
        self.address.clear()



    def select_student(self):
        """
            ღილაკზე დაჭერის შემთხვევაში ასელექთებს იმ ადამიანის ინფორმაციას რომელიც მონიშნულია ცხრილში და lineedit-ში ტექსტის სახით წერს
        """
        row = self.table.currentRow()
        if row < 0:
            return

        self.first_name.setText(self.table.item(row, 0).text())
        self.last_name.setText(self.table.item(row, 1).text())
        self.age.setText(self.table.item(row, 2).text())
        self.email.setText(self.table.item(row, 3).text())
        self.password.setText(self.table.item(row, 4).text())
        self.address.setText(self.table.item(row, 5).text())
        self.role.setCurrentText(self.table.item(row, 6).text())
        self.id.setText(self.table.item(row, 7).text())

    def update_student(self):
        """
            ღილაკზე დაჭერის შევთხვევაში, ააბდეითებს მონიშნული ადამიანის მონაცემებს და უგზავნის ბექენდს
        """
        row = self.table.currentRow()
        if row < 0:
            return
        try:
            values = [
                self.first_name.text(),
                self.last_name.text(),
                self.age.text(),
                self.email.text(),
                self.password.text(),
                self.address.text(),
                self.role.currentText(),
                self.id.text()
            ]

            self.user_update_signal.emit(int(values[7]),str(values[3]),str(values[4]),str(values[0]),str(values[1]),int(values[2]),str(values[5]),str(values[6]))
            for col, value in enumerate(values):
                self.table.setItem(row, col, QtWidgets.QTableWidgetItem(value))
        except Exception as e:
            QtWidgets.QMessageBox.warning(self.tab, "შეცდომა", f"მონაცემების განახლება ვერ მოხერხდა: {e}")
    def delete_student(self):
        """
        შლის მონიშნულ ადამიანი ინფორმაციას
        :return: უგზავნის ბექენდს იმ ადამიანის id-ს რომელიც უნდა წაიშალოს
        """

        row = self.table.currentRow()
        if row >= 0:
            user_id = self.table.item(row, 7).text()

            self.user_deleted_signal.emit(user_id)
            self.table.removeRow(row)



class AnalyticTab(BasePage):
    """
        ეს კლასი ქმნის ტაბს ადმინისთვის,სადაც შესაძლებელია სტატისტიკის ნახვა
    """
    def __init__(self,courses_data,students_data,lector_data,lector_rating_data,app=None):
        super().__init__(app)

        self.tab = QtWidgets.QWidget()
        self.courses_data = courses_data
        self.students_data = students_data
        self.lector_data = lector_data
        self.lector_rating_data = lector_rating_data

        self.btn1 = QtWidgets.QPushButton("✔")
        self.btn2 = QtWidgets.QPushButton("✔")
        self.btn3 = QtWidgets.QPushButton("✔")
        self.btn4 = QtWidgets.QPushButton("✔")

        self.stack = QtWidgets.QStackedWidget()
        self.page1 = self.create_all_table_page(["კურსი", "საშ.ქ", "ჩაჭრის პროცენტი"], self.courses_data)
        self.page2 = self.create_all_table_page(["სტუდენტი", "სემესტრი", "საშ.ქ", "საშ.ქ გადახრა"], self.students_data, "სტუდენტი")
        self.page3 = self.create_all_table_page(["საგანი", "ლექტორი", "საშ.ქ","საშ.ქ გადახრა"], self.lector_data,  "საგანი")
        self.page4 = self.create_all_table_page(["საგანი", "ლექტორი", "საშ.ქ", "რეიტინგი","რეიტინგის გადახრა"], self.lector_rating_data, "საგანი")
        self.build_ui()


    def build_ui(self):
        main_layout = QtWidgets.QVBoxLayout(self.tab)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 20, 30, 20)

        title = QtWidgets.QLabel("Analytic")
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold;")

        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.setSpacing(30)
        btn_layout.setContentsMargins(350, 20, 30, 20)

        labels_texts = [
            "კურსების სირთულე",
            "სტუდენტების პროგრესი",
            "ლექტორების ობიექტურობა",
            "ლექტორების რეიტინგი"
        ]
        theme_button = QtWidgets.QPushButton(" Dark /  Light")
        theme_button.setFixedSize(150, 40)
        theme_button.clicked.connect(self.toggle_theme)

        for btn, text in zip(
                (self.btn1, self.btn2, self.btn3, self.btn4), labels_texts):
            btn.setFixedSize(30, 30)
            btn.setStyleSheet(self.button_style())

            label = QtWidgets.QLabel(text)
            label.setStyleSheet("font-size: 18px;")

            item_layout = QtWidgets.QHBoxLayout()
            item_layout.setSpacing(8)
            item_layout.addWidget(btn)
            item_layout.addWidget(label)

            btn_layout.addLayout(item_layout)

        btn_layout.addStretch()
        btn_layout.addWidget(theme_button)

        main_layout.addWidget(title)
        main_layout.addLayout(btn_layout)
        main_layout.addWidget(self.stack)

        self.stack.addWidget(self.page1)
        self.stack.addWidget(self.page2)
        self.stack.addWidget(self.page3)
        self.stack.addWidget(self.page4)

        self.btn1.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.btn2.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.btn3.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        self.btn4.clicked.connect(lambda: self.stack.setCurrentIndex(3))

    def create_all_table_page(self, data_list, data, placeholder=None):
        """
            ეს მეთოდი ქმნის ცხრილს, და lineedit-ს რომლის საშუალებითაც შესაძლებელია ცხრილში მონაცემების მოძებნა
        """
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)
        layout.setSpacing(15)

        search_layout = QtWidgets.QHBoxLayout()
        search_input = QtWidgets.QLineEdit()
        search_input.setPlaceholderText(placeholder)
        self.apply_input_style(search_input)

        search_btn = QtWidgets.QPushButton("Search")
        search_btn.setStyleSheet(self.button_style())
        search_btn.setMaximumHeight(40)
        search_btn.clicked.connect(lambda: self.search(search_input, table))

        if len(data_list) >= 4:
            search_layout.addWidget(search_input)
            search_layout.addWidget(search_btn)
        search_layout.addStretch()

        table = QtWidgets.QTableWidget(0, len(data_list))
        table.setHorizontalHeaderLabels(list(data_list))
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        for i in data:
            self.add_to_table(i, table)

        layout.addLayout(search_layout)
        layout.addWidget(table)
        return widget


class MainApp(QtWidgets.QMainWindow):
    def __init__(self, CreateTabs, main_logic):
        super().__init__()

        self.main_logic = main_logic
        self.CreateTabs = CreateTabs

        self.setWindowTitle("Student Management System")
        self.setMinimumSize(1280, 800)
        self.stacked = QtWidgets.QStackedWidget()

        self.login_page_obj = LoginPage(self.stacked, app=self)
        self.login_reg_page_obj = LoginRegisterPage(self.stacked, app=self)
        self.register_page_obj = RegisterPage(self.stacked, app=self)

        self.tabs_page_obj = QtWidgets.QWidget()

        self.init_ui()

    def init_ui(self):
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QVBoxLayout(central_widget)
        layout.addWidget(self.stacked)

        self.stacked.addWidget(self.login_reg_page_obj.Login_Register_Page)
        self.stacked.addWidget(self.login_page_obj.Login_page)
        self.stacked.addWidget(self.register_page_obj.Register_page)
        self.tabs_index = self.stacked.addWidget(self.tabs_page_obj)

        self.setStyleSheet(BasePage().light_theme())
        self.stacked.setCurrentIndex(0)

    def setup_tabs(self):
        """ეს მეთოდი გამოიძახება main.py-დან ლოგინის შემდეგ"""
        old_widget = self.stacked.widget(self.tabs_index)
        self.stacked.removeWidget(old_widget)

        self.tabs_controller = self.CreateTabs(app=self,main_obj=self.main_logic)
        self.tabs_page_obj = self.tabs_controller.tabs
        self.tabs_index = self.stacked.addWidget(self.tabs_page_obj)
        self.stacked.setCurrentIndex(self.tabs_index)

