import sqlite3
import os
from backend.validations import validate_db_status


class AppDatabase:
    """ კლასი მონაცემთა ბაზასთან სამუშაოდ.

        უზრუნველყოფს კავშირის მართვას, ქუერების შესრულებას და სქემის ინიციალიზაციას.
        """

    def __init__(self, db_name):
        """ბაზის ინიციალიზაცია, იქმნება საჭირო დირექტორია - თუ არ არსებობს.

           :param db_name: მონაცემთა ბაზის ფაილის სახელი
           :type db_name: str"""

        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir, _ = os.path.split(current_dir)
        self.db_dir = os.path.join(parent_dir, "database")

        if not os.path.exists(self.db_dir):
            os.makedirs(self.db_dir)

        self.db_file = os.path.join(self.db_dir, db_name)
        self._status = False
        self.conn = None
        self.cursor = None

    def open(self):
        """მონაცემთა ბაზის გახსნა.
        """

        if not self._status:
            self.conn = sqlite3.connect(self.db_file)
            self.conn.execute("PRAGMA foreign_keys = ON;")
            self.cursor = self.conn.cursor()
            self._status = True

    def close(self):
        """მონაცემთა ბაზის დახურვა.
        """

        if self._status:
            self.cursor.close()
            self.conn.close()
            self._status = False

    @validate_db_status
    def commit(self):
        """ცვლილებების დამახსოვრება.

        :raise: DataBaseError თუ მონაცემთა ბაზა დაკეტილია
        :return: None """

        self.conn.commit()
        print("successfully commited")

    @validate_db_status
    def rollback(self):
        """ბაზის წინა მდგომარეობამდე დაბრუნება

        :raise: DataBaseError თუ მონაცემთა ბაზა დაკეტილია
        :return: None"""

        self.conn.rollback()
        print("successfully rollback")

    @validate_db_status
    def execute_query(self, query, params=None, mode="one"):
        """
        SQL ბრძანებების შესრულების მეთოდი. აერთიანებს execute და executemany-ს, მუშაობს 5 რეჟიმში.

        :param query: SQL ბრძანება, რომელიც უნდა დაამუშავოს ბაზამ.
        :type query: str
        :param params: დამატებითი მონაცემები ქუერისთვის.
        :type params: tuple | list[tuple] | tuple[tuple] | None
        :param mode: გამოყენების რეჟიმი:
            * 'many' - იყენებს executemany-ს  ჩაწერისთვის.
            * 'exec' - აბრუნებს lastrowid-ს (INSERT-ისთვის) ან rowcount-ს.
            * 'one'  - აბრუნებს პირველ სტრიქონს (fetchone).
            * 'all'  - აბრუნებს ყველა სტრიქონს (fetchall).
            * 'iter' - აბრუნებს კურსორს.
        :type mode: str
        :return: შედეგი რეჟიმის მიხედვით (ID, count, tuple, list ან iterator).
        :raises TypeError: თუ query არ არის სტრიქონი ან params არასწორი ტიპისაა.
        :raises ValueError: თუ რეჟიმი არ შეესაბამება SQL ოპერაციას.
        """

        if not (query and isinstance(query, str)):
            raise TypeError("query must be a string")

        if params is not None and not isinstance(params, (list, tuple)):
            raise TypeError("param must be a list or tuple of tuples")

        is_select = query.strip().upper().startswith('SELECT')
        is_insert = query.strip().upper().startswith('INSERT')
        match mode:
            case "many":
                if not params or not all(isinstance(tp, tuple) for tp in params):
                    raise TypeError("param must be a list or tuple of tuples")
                res = self.cursor.executemany(query, params)
                return res

            case "exec":
                res = self.cursor.execute(query, params or ())
                if is_insert:
                    return self.cursor.lastrowid
                return res.rowcount

            case "one":
                if not is_select:
                    raise ValueError("'one' mode allowed only for SELECT")
                res = self.cursor.execute(query, params or ())
                return res.fetchone()

            case "all":
                if not is_select:
                    raise ValueError("'one' mode allowed only for SELECT")
                res = self.cursor.execute(query, params or ())
                return res.fetchall()

            case "iter":
                if not is_select:
                    raise ValueError("'iter' mode allowed only for SELECT")
                res = self.cursor.execute(query, params or ())
                return res

            case _:
                raise ValueError(f"Unknown mode: {mode}")

    @validate_db_status
    def init_schema(self):
        """
        მონაცემთა ბაზის სქემის ინიციალიზაცია.

        ქმნის სისტემის ფუნქციონირებისთვის აუცილებელ ყველა ცხრილს, თუ ისინი ჯერ
        არ არსებობს. მეთოდი განსაზღვრავს:
        * მომხმარებლებისა და როლების სტრუქტურას.
        * სტუდენტებისა და ლექტორების პერსონალურ მონაცემებს.
        * კურსებს, ჯგუფებსა და მათ განრიგს.
        * რეგისტრაციების (enrollments) და უკუკავშირის (feedback) სისტემას.
        * ცხრილებს შორის კავშირებს (Foreign Keys) და წაშლის წესებს (ON DELETE CASCADE).
        """
        tables = ["""CREATE TABLE IF NOT EXISTS users
                     (
                         user_id  INTEGER PRIMARY KEY AUTOINCREMENT,
                         email    TEXT NOT NULL UNIQUE,
                         password BLOB NOT NULL,
                         role     Text NOT NULL
                     );""",

                  """CREATE TABLE IF NOT EXISTS students
                     (
                         id        INTEGER PRIMARY KEY,
                         name      TEXT NOT NULL,
                         last_name TEXT NOT NULL,
                         age       INTEGER,
                         address   TEXT,
                         FOREIGN KEY (id) REFERENCES users (user_id) ON DELETE CASCADE
                     );""",

                  """CREATE TABLE IF NOT EXISTS lecturers
                     (
                         id        INTEGER PRIMARY KEY,
                         name      TEXT    NOT NULL,
                         last_name TEXT    NOT NULL,
                         age       INTEGER NOT NULL,
                         address   TEXT,
                         FOREIGN KEY (id) REFERENCES users (user_id) ON DELETE CASCADE
                     );""",

                  """CREATE TABLE IF NOT EXISTS courses
                     (
                         id          INTEGER PRIMARY KEY AUTOINCREMENT,
                         course_name TEXT    NOT NULL,
                         credits     INTEGER NOT NULL
                     )""",

                  """CREATE TABLE IF NOT EXISTS courses_groups
                     (
                         id           INTEGER PRIMARY KEY AUTOINCREMENT,
                         course_id    INTEGER NOT NULL,
                         lecturer_id  INTEGER NOT NULL,
                         group_name   TEXT    NOT NULL,
                         day_of_week  TEXT    NOT NULL,
                         auditorium   TEXT    NOT NULL,
                         class_time   TEXT    NOT NULL,
                         max_students INTEGER NOT NULL,
                         FOREIGN KEY (course_id) REFERENCES courses (id) ON DELETE CASCADE,
                         FOREIGN KEY (lecturer_id) REFERENCES lecturers (id) ON DELETE CASCADE
                     )""",

                  """CREATE TABLE IF NOT EXISTS enrollments
                     (
                         student_id INTEGER NOT NULL,
                         group_id   INTEGER NOT NULL,
                         grade      INTEGER NOT NULL,
                         semester   INTEGER NOT NULL,
                         status     text    NOT NULL,
                         PRIMARY KEY (student_id, group_id),
                         FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE,
                         FOREIGN KEY (group_id) REFERENCES courses_groups (id) ON DELETE CASCADE
                     )""",

                  """CREATE TABLE IF NOT EXISTS feedback
                     (
                         lecturer_id INTEGER NOT NULL,
                         stars       INTEGER NOT NULL,
                         desc        TEXT,
                         FOREIGN KEY (lecturer_id) REFERENCES lecturers (id) ON DELETE CASCADE
                     )""",

                  """CREATE TABLE IF NOT EXISTS admins
                     (  
                        id INTEGER PRIMARY KEY,
                        name      TEXT NOT NULL,
                        last_name TEXT NOT NULL,
                        age      INTEGER NOT NULL,
                        address   TEXT,
                        FOREIGN KEY (id) REFERENCES users (user_id) ON DELETE CASCADE
                        )"""
                  ]
        for table in tables:
            self.execute_query(table, mode='exec')

    def show_tables(self):
        """გამოაქვს ბაზაში არსებული ცხრილების სახელები."""

        query = "SELECT name FROM sqlite_master WHERE type='table';"
        tables = self.execute_query(query, mode='all')
        for table in tables:
            print(f"tablename: {table[0]}")
