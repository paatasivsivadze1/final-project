import re, bcrypt
from backend.MDatabase import AppDatabase
from backend.validations import (cls_str_checker, validate_registration_update, rollback_decorator, error_catcher,
                                 AuthentificationError)


class Authentification:
    """ორი ძირითადი მეთოდი, add_user, login.
        add_user: სტუდენტის/ლექტორის რეგისტრაცია,
        login: სტუდენტის/ლექტორის/ადმინის ავტორიზაცია"""

    def __init__(self, db_object: AppDatabase):
        """ინიციალიზაცია - მონაცემთა ბაზის შემოწმება და მიბმა"""
        if not isinstance(db_object, AppDatabase):
            raise TypeError("db_object must be a AppDatabase")
        self._db_object = db_object

    @cls_str_checker
    def _validate_mail(self, mail: str):
        """მეილის ვალიდაცია re-ს გამოყენებით,
           ერროის ამოგდება მცდარი ფორმატის შემთხვევეაში,
           შედეგი: None"""

        example = r'^[\w\d]+(\.[\w\d]+)*\.?\@\w+(\.\w+)+$'
        res = re.match(example, mail)

        if not bool(res):
            raise ValueError("Invalid Mail Format")

    @cls_str_checker
    def _validate_password(self, password: str):
        """პაროლის ვალიდაცია,
           ერრორის ამოგდება მცდარი ფორმატის შემთხვევაში,
           შედეგი: None """
        example = r'(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[._!*]).{8,}'
        res = re.match(example, password)

        if not bool(res):
            raise ValueError("Unsupported Password Format")

    @cls_str_checker
    def _mail_is_exists(self, mail: str):
        """იუზერის მეილის შემოწმება მონაცემთა ბაზაში
            შედეგი: bool"""
        query = """SELECT email
                   FROM users
                   where email = ?"""
        return bool(self._db_object.execute_query(query, params=(mail,)))

    @rollback_decorator
    @validate_registration_update
    def add_user(self, mail: str, password: str, name: str, last_name: str, age: int, address: str, role: str):
        """მომხმარებლის დამატება როლის მიხედვით (სტუდენტი/ლექტორი),
            შედეგი: None"""

        password_hash = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt(12))

        users_query = """INSERT INTO users (email,
                                            password,
                                            role)
                         VALUES (?, ?, ?)"""

        students_query = """INSERT INTO students (id,
                                                  name,
                                                  last_name,
                                                  age,
                                                  address)
                            Values (?, ?, ?, ?, ?)"""

        lecturers_query = """INSERT INTO lecturers (id,
                                                    name,
                                                    last_name,
                                                    age,
                                                    address)
                             VALUES (?, ?, ?, ?, ?)"""

        admins_query = """INSERT INTO admins (id,
                                              name,
                                              last_name,
                                              age,
                                              address)
                          VALUES (?, ?, ?, ?, ?)"""

        # მონაცემთა ბაზაში მომხმარებლის დამატება:

        user_id = self._db_object.execute_query(users_query, params=(mail, password_hash, role), mode="exec")

        match role:
            case "student":
                self._db_object.execute_query(students_query, params=(user_id, name, last_name, age, address),
                                              mode="exec")

            case "lecturer":
                self._db_object.execute_query(lecturers_query, params=(user_id, name, last_name, age, address),
                                              mode="exec")

            case "admin":
                self._db_object.execute_query(admins_query, params=(user_id, name, last_name, age, address),
                                              mode="exec")

            case _:
                pass

        return user_id

    def login(self, mail: str, password: str):
        """იუზერის ავტორიზაცია
            შედეგი: მომხმარებლის id და როლი"""

        self._validate_mail(mail)
        self._validate_password(password)

        # მომხმარებლის მოძებნა

        query = """SELECT user_id,
                          password,
                          role
                   FROM users
                   WHERE email = ?"""

        res = self._db_object.execute_query(query, params=(mail,), mode="one")

        if not res:
            raise AuthentificationError("Mail Not Found")

        user_id, hashed_password, role = res

        if bcrypt.checkpw(password.encode('utf8'), hashed_password):
            print(f"User {mail} successfully logged in!")
            return user_id, role
        else:
            raise AuthentificationError("Invalid password")

    @rollback_decorator
    @validate_registration_update
    def update_user(self, user_id: int, mail: str, password: str, name: str, last_name: str,
                    age: int, address: str, role: str):
        """მომხმარებლის ინფორმააციის განახლება მისი user_id-ით.

        """
        if '$' not in password:
            password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt(12))

            query = """UPDATE users
                       SET email    = ?,
                           password = ?,
                           role     = ?
                       WHERE user_id = ?"""
            self._db_object.execute_query(query, params=(mail, password, role, user_id), mode="exec")
        else:
            query = """UPDATE users
                       SET email    = ?,
                           role     = ?
                       WHERE user_id = ?"""

            self._db_object.execute_query(query, params=(mail, role, user_id), mode="exec")

        del_students = """DELETE
                          FROM students
                          WHERE id = ?"""

        del_lecturers = """DELETE
                           FROM Lecturers
                           WHERE id = ?"""

        del_admins = """DELETE
                        FROM admins
                        WHERE id = ?"""

        self._db_object.execute_query(del_students, params=(user_id,), mode="exec")
        self._db_object.execute_query(del_lecturers, params=(user_id,), mode="exec")
        self._db_object.execute_query(del_admins, params=(user_id,), mode="exec")

        params = (user_id, name, last_name, age, address)

        match role:

            case "student":
                insert_query = """INSERT INTO students (id,
                                                        name,
                                                        last_name,
                                                        age,
                                                        address)
                                  Values (?, ?, ?, ?, ?)"""

                self._db_object.execute_query(insert_query, params, mode="exec")

            case "lecturer":

                insert_query = """INSERT INTO lecturers (id,
                                                         name,
                                                         last_name,
                                                         age,
                                                         address)
                                  Values (?, ?, ?, ?, ?)"""

                self._db_object.execute_query(insert_query, params, mode="exec")

            case "admin":
                insert_query = """INSERT INTO admins (id,
                                                      name,
                                                      last_name,
                                                      age,
                                                      address)
                                  Values (?, ?, ?, ?, ?)"""

                self._db_object.execute_query(insert_query, params, mode="exec")

            case _:
                pass

    @rollback_decorator
    def delete_user(self, user_id: int):
        query = """DELETE
                   FROM users
                   WHERE user_id = ?"""

        self._db_object.execute_query(query, params=(user_id,), mode="exec")
