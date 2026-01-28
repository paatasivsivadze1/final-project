from backend.validations import cls_str_checker, error_catcher


class Admin:
    """ადმინის უფლებების მართვის კლასი.
        ძირითადი ფუნქიონალი:"""

    def __init__(self, user_id, db_object, auth_object):
        self._user_id = user_id
        self._db_object = db_object
        self._auth_object = auth_object



    def show_all_users(self):

        tables = ('students', 'lecturers', 'admins')
        lst = []

        for table in tables:
            query = (f"""SELECT {table[0]}.name,
                                {table[0]}.last_name,
                                {table[0]}.age,     
                                u.email,
                                u.password,
                                {table[0]}.address,
                                u.role, 
                                u.user_id
                        FROM {table} {table[0]}
                             JOIN users u
                                  ON {table[0]}.id = u.user_id""")

            res = self._db_object.execute_query(query, mode='iter')
            lst.extend([i for i in res])

        return lst

    def add_user(self, mail: str, password: str, name: str, last_name: str, age: int, address: str, role: str):
        if not self._auth_object:
            raise AttributeError('missed Authentication class object')

        user_id = self._auth_object.add_user(mail, password, name, last_name, age, address, role)

        role = role + 's'

        query = f"""SELECT {role[0]}.name,
                                  {role[0]}.last_name,
                                  {role[0]}.age,
                                  u.email,
                                  u.password,
                                  {role[0]}.address,
                                  u.role,
                                  u.user_id
                           FROM users u
                           JOIN {role} {role[0]}
                           ON {role[0]}.id = u.user_id
                           WHERE u.user_id = ?"""

        return self._db_object.execute_query(query, (user_id,), mode='one')

    def update_user(self, user_id, mail: str, password: str, name: str, last_name: str,
                    age: int, address: str, role: str):

        self._auth_object.update_user(user_id, mail, password, name, last_name, age, address, role)

    @error_catcher
    def delete_user(self, user_id: int):

        self._auth_object.delete_user(user_id)

    def overview_courses(self):
        """
        ითვლის დასრულებული კურსების (passed/failed) საშუალო ქულას
        და ჩაჭრის პროცენტს.
        """
        query = """
                SELECT c.course_name,
                       ROUND(AVG(e.grade), 2) AS avg_finished_grade,
                       ROUND(
                               SUM(CASE
                                       WHEN e.status = 'failed' THEN 1
                                       ELSE 0
                                   END) * 100.0 / COUNT(e.student_id),
                               2
                       )                      AS failure_rate,
                       SUM(CASE
                               WHEN e.status = 'passed' THEN 1
                               ELSE 0
                           END)               AS passed_students_count

                FROM courses c
                         JOIN courses_groups cg
                              ON c.id = cg.course_id
                         JOIN enrollments e
                              ON cg.id = e.group_id
                WHERE e.status IN ('passed', 'failed')
                GROUP BY c.id
                ORDER BY failure_rate DESC
                """
        res = self._db_object.execute_query(query, mode='all')
        r = tuple((i[0], i[1], str(i[2]) + '%') for i in res)
        print(r)
        return r

    def overview_all_students_progress(self):
        query = """
                SELECT s.name || ' ' || s.last_name AS fullname,
                       e.semester,
                       ROUND(AVG(e.grade), 2)
                FROM enrollments e
                         JOIN students s ON e.student_id = s.id
                WHERE e.status IN ('passed', 'failed')
                GROUP BY e.student_id, e.semester
                ORDER BY e.student_id, e.semester 
                """
        res = self._db_object.execute_query(query, mode='all')

        lst = []
        last_name = ''
        for i in range(len(res)):
            if i == 0:
                lst.append((res[i][0], res[i][1], res[i][2], '0%'))
                last_name = res[i][0]
                continue

            current_name = res[i][0]
            if current_name != last_name:
                lst.append((res[i][0], res[i][1], res[i][2], '0%'))


            else:
                prev_avg = res[i - 1][2]
                curr_avg = res[i][2]
                percent = round(((curr_avg - prev_avg) / prev_avg) * 100, 2)
                percent_diff = str(percent) + '%'
                lst.append((res[i][0], res[i][1], res[i][2], percent_diff))

            last_name = current_name

        return lst

    def compare_lecturers(self):
        query = """SELECT c.course_name,
                          l.name || ' ' || l.last_name AS fullname,
                          ROUND(AVG(e.grade), 2)       AS avg_finished_grade,
                          ROUND(
                                  (AVG(e.grade) -
                                   (SELECT AVG(grade) FROM enrollments WHERE status IN ('passed', 'failed'))) * 100.0 /
                                  (SELECT AVG(grade) FROM enrollments WHERE status IN ('passed', 'failed')),
                                  2
                          )                            AS avg_percent_deviation
                   FROM enrollments e
                            JOIN courses_groups cg ON cg.id = e.group_id
                            JOIN lecturers l ON cg.lecturer_id = l.id
                            JOIN courses c ON cg.course_id = c.id
                   WHERE e.status IN ('passed', 'failed')
                   GROUP BY c.course_name, l.id, l.name, l.last_name
                   ORDER BY c.course_name; 
                """
        res =  self._db_object.execute_query(query, mode='iter')

        return [(i[0], i[1], i[2], str(i[3]) + '%') for i in res]

    def compare_feedback_and_grades(self):
        query = """
                SELECT c.course_name, 
                       l.name || ' ' || l.last_name                                         AS fullname, 
                       ROUND(AVG(e.grade), 2)                                               AS avg_grade, 
                       (SELECT ROUND(AVG(stars), 2) FROM feedback
                        WHERE lecturer_id = l.id) AS lecturer_rating, 
                       
                       (SELECT ROUND(AVG(stars), 2) FROM feedback)                          AS total_avg_rating
                
                FROM lecturers l
                         JOIN courses_groups cg ON l.id = cg.lecturer_id
                         JOIN courses c ON cg.course_id = c.id
                         JOIN enrollments e ON cg.id = e.group_id
                AND e.status IN ('passed', 'failed')
                GROUP BY l.id, c.course_name, l.name, l.last_name
                ORDER BY lecturer_rating DESC \
                """

        res = self._db_object.execute_query(query, mode='all')


        lst = []
        for i in res:
            course, name, grade, rating, total_avg = i
            percent_diff = round((rating / total_avg) * 100 - 100, 2)
            lst.append((course, name, grade, rating, str(percent_diff) + '%'))

        return lst