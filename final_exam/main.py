import sys

from PyQt5 import QtWidgets, QtCore
from backend.MDatabase import AppDatabase
from backend.Authentification import Authentification
from backend import Students, Lecturers, Admins
from frontend import Front


class Main:
    def __init__(self, db_object, auth_handler):
        self.db_object = db_object
        self.db_object.open()
        self.auth_handler = auth_handler
        self.app = QtWidgets.QApplication(sys.argv)
        self.main_win = Front.MainApp(CreateTabs, main_logic=self)
        self.main_win.login_page_obj.login_attempted.connect(self.process_login)
        self.main_win.register_page_obj.register_attempted.connect(self.process_register)

        self.role = None
        self._user_id = None
        self.user = None

        self.main_win.show()
        sys.exit(self.app.exec_())
    def _create_user_by_role(self, user_id,role):
        match role:
            case "student":
                return Students.Student(user_id, self.db_object)
            case "lecturer":
                return Lecturers.Lecturer(user_id, self.db_object)
            case "admin":
                return Admins.Admin(user_id, self.db_object, self.auth_handler)
            case _:
                raise ValueError("invalid role")


    def process_login(self, email, password):
        try:
            print(self.auth_handler.login(email, password))
            user_id, role = self.auth_handler.login(email, password)
            self._user_id = user_id
            self.role = role
            self.user = self._create_user_by_role(self._user_id, role)

            self.main_win.setup_tabs()
            self.main_win.stacked.setCurrentIndex(3)

        except Exception as e:
            QtWidgets.QMessageBox.warning(self.main_win, "შეცდომა", str(e))

        return self.user

    def process_register(self, first_name, last_name, email, password, age, address):
        try:
            self.auth_handler.add_user(email, password, first_name, last_name, age, address, 'student')

            self.main_win.stacked.setCurrentIndex(0)
        except Exception as e:
            QtWidgets.QMessageBox.warning(self.main_win, "შეცდომა", str(e))


    def get_role(self):
        return self.role



class CreateTabs(Front.BasePage):
    """ქმნის ტაბებს"""
    def __init__(self, app=None, main_obj=None):
        super().__init__(app)

        self.main_obj = main_obj
        self.role = main_obj.get_role()

        match self.role:
            case "student":
                self._setup_student()
            case "lecturer":
                self._setup_lecturer()
            case "admin":
                self._setup_admin()
            case _:
                print(f"Warning: Unknown role {self.role}")
                raise ValueError(f'Invalid role: {self.role}')


        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setParent(self.app)
        self.build()

    def _setup_student(self):
        """სტუდენტისთვის საჭირო მონაცემების და ტაბების მომზადება"""
        self.subject_data = self.main_obj.user.show_available_groups()
        self.table_data = self.main_obj.user.get_schedule()
        self.personal_info_data = self.main_obj.user.show_personal_info()
        self.change_subject = self.main_obj.user.get_active_enrollments()
        self.show_lecturer = self.main_obj.user.show_lecturers_to_review()

        self.choose_subjects_obj = Front.ChooseSubjectsTab(self.subject_data,self.change_subject, self.app)
        self.choose_subjects = self.choose_subjects_obj.tab

        self.personal_info_obj = Front.PersonalInfoTab(self.personal_info_data, self.table_data,self.show_lecturer, self.role, self.app)
        self.personal_info_tab = self.personal_info_obj.tab

        self.choose_subjects_obj.subject_added.connect(self.handle_subject_addition)
        self.personal_info_obj.review_submitted.connect(self.main_obj.user.add_review)

    def _setup_lecturer(self):
        """ლექტორისთვის საჭირო მონაცემების და ტაბების მომზადება"""
        self.table_data = self.main_obj.user.get_schedule()
        print(self.table_data)
        self.personal_info_data = self.main_obj.user.get_profile()
        self.show_students = self.main_obj.user.show_students_in_group()
        self.show_lecturer = None

        self.personal_info_obj = Front.PersonalInfoTab(self.personal_info_data, self.table_data, self.show_lecturer,self.role, self.app)
        self.personal_info_tab = self.personal_info_obj.tab

        self.change_score_obj = Front.ChangeScoreTab(self.show_students,self.app)
        self.change_score = self.change_score_obj.tab

        self.change_score_obj.score_updated.connect(self.main_obj.user.set_grade)

    def _setup_admin(self):
        """ადმინისთვის საჭირო მონაცემების მომზადება"""
        self.personal_info_tab = None
        self.choose_subjects = None
        self.show_all_users = self.main_obj.user.show_all_users()
        self.overview_courses = self.main_obj.user.overview_courses()
        self.overview_students_progress = self.main_obj.user.overview_all_students_progress()
        self.compare_lecturers = self.main_obj.user.compare_lecturers()
        self.compare_feedback = self.main_obj.user.compare_feedback_and_grades()

        self.information_management_obj = Front.InformationManagementTab(self.show_all_users, self.app)
        self.information_management_tab = self.information_management_obj.tab

        self.analytic_obj = Front.AnalyticTab(self.overview_courses ,self.overview_students_progress,self.compare_lecturers,self.compare_feedback,self.app)
        self.analytic_tab = self.analytic_obj.tab

        self.information_management_obj.user_added_signal.connect(self.handle_admin_add_user)
        self.information_management_obj.user_update_signal.connect(self.main_obj.user.update_user)
        self.information_management_obj.user_deleted_signal.connect(self.main_obj.user.delete_user)

    def handle_admin_add_user(self, data):
        """ დამატება როლების მიხედვით."""
        try:
            result = self.main_obj.user.add_user(data[3],data[4], data[0],data[1],int(data[2]), data[5], data[6])
            self.information_management_obj.add_to_table(result, self.information_management_obj.table)

        except Exception as e:
            QtWidgets.QMessageBox.warning(None, "შეცდომა", f"ბაზაში ჩაწერა ვერ მოხერხდა: {e}")

    def handle_subject_addition(self, subject_info):
        subject, lecturer, group, s_id, is_added = subject_info

        try:
            if is_added:
                self.main_obj.user.add_subject(s_id)
            else:
                self.main_obj.user.drop_subject(s_id)

            updated_schedule = self.main_obj.user.get_schedule()

            if hasattr(self, 'personal_info_obj'):
                p_table = self.personal_info_obj.table
                p_table.setRowCount(0)

                if updated_schedule:
                    for row_data in updated_schedule:
                        self.personal_info_obj.update_schedule_table(row_data)

                p_table.viewport().update()
                QtWidgets.QApplication.processEvents()

        except Exception as e:
            print(f"DB Error: {e}")


    def build(self):
        """ტაბების დამატება როლების მიხედვით."""
        if self.role == "student":
            self.tabs.addTab(self.personal_info_tab, "Personal Info")
            self.tabs.addTab(self.choose_subjects, "Choose Subjects")

        elif self.role == "lecturer":
            self.tabs.addTab(self.personal_info_tab, "Personal Info")
            self.tabs.addTab(self.change_score, "Change Score")

        elif self.role == "admin":
            self.tabs.addTab(self.information_management_tab, "Info Management")
            self.tabs.addTab(self.analytic_tab, "Analytic")



if __name__ == "__main__":
    db_object = AppDatabase('app.db')
    auth_handler = Authentification(db_object)
    app = Main(db_object, auth_handler)

