from backend.validations import validate_user_methods, rollback_decorator, error_catcher


class StudentClassError(Exception):
    pass


class Student:

    def __init__(self, user_id: int, db_object):
        self._user_id = user_id
        self._db_object = db_object
        self._all_subjects = None
        self._current_semester = self._get_last_semester() + 1

        self.passed_subjects = [i[0] for i in self._get_passed_subjects()]

        current_enrollment = self._get_already_enrolled_subjects()

        self.current_enrollments_info = current_enrollment  # [(course_name, credits, class_time, lecturer group_name),]
        self._enrolled_subjects = [i[0] for i in current_enrollment]
        self.credits = sum(i[1] for i in current_enrollment)

    def get_active_enrollments(self):
        return tuple((i[0], i[3], i[4]) for i in self.current_enrollments_info)

    @validate_user_methods
    def _get_already_enrolled_subjects(self):

        query = """SELECT c.course_name,
                          c.credits,
                          cg.day_of_week || ' ' || cg.class_time as class_time,
                          l.name || ' ' || l.last_name,
                          cg.group_name
                   FROM enrollments en
                            JOIN courses_groups cg
                                 ON cg.id = en.group_id
                            JOIN courses c
                                 ON c.id = cg.course_id
                            JOIN lecturers l
                                 ON cg.lecturer_id = l.id
                   WHERE en.student_id = ?
                     AND en.semester = ?
                     AND en.status = 'active'"""

        res = self._db_object.execute_query(query, (self._user_id, self._current_semester), mode='iter')
        res = list((i[0], i[1], i[2], i[3], i[4]) for i in res)

        return res

    @validate_user_methods
    def _get_passed_subjects(self):

        query = """SELECT c.course_name
                   FROM enrollments en
                            JOIN courses_groups cg
                                 ON cg.id = en.group_id
                            JOIN courses c
                                 ON c.id = cg.course_id
                   WHERE en.student_id = ?
                     AND en.status = 'passed'"""

        return self._db_object.execute_query(query, (self._user_id,), mode='all')

    @validate_user_methods
    def show_available_groups(self):
        """სტუდენტისთვის ხელმისაწვდომი ჯგუფების ჩვენება."""

        query = """
                SELECT c.course_name,
                       l.name || ' ' || l.last_name AS lecturer_name,
                       cg.group_name,
                       cg.id
                FROM courses_groups cg
                         JOIN courses c
                              ON c.id = cg.course_id
                         JOIN lecturers l
                              ON cg.lecturer_id = l.id
                WHERE (SELECT COUNT(*)
                       FROM enrollments
                       WHERE group_id = cg.id
                         AND status = 'active') < cg.max_students \
                """

        res = self._db_object.execute_query(query, mode='iter')
        res_dict = {}

        for tp in res:

            list_key = tp[0]
            fullname = tp[1]
            group_name = tp[2]
            group_id = int(tp[3])

            if not res_dict.get(list_key):
                res_dict[list_key] = [[(fullname, group_name), group_id]]

            else:
                res_dict[list_key].append([(tp[1], tp[2]), tp[3]])

        return res_dict

    @error_catcher
    @validate_user_methods
    def _get_last_semester(self):

        query = """SELECT COALESCE(MAX(semester), 0)
                   FROM enrollments
                   WHERE student_id = ?
                     AND status IN ('failed', 'passed')"""

        res = self._db_object.execute_query(query, (self._user_id,), mode='one')
        return res[0]

    @error_catcher
    def show_personal_info(self):
        """აბრუნებს სრულ ინფრომაციას სტუდენტზე მიმდინარე სემესტრში."""
        return self.get_profile() + (self._current_semester, self.credits)

    @validate_user_methods
    def get_profile(self):

        query = '''SELECT st.name,
                          st.last_name,
                          u.email,
                          st.age,
                          st.address
                   FROM students st
                            JOIN users u
                                 ON st.id = u.user_id
                   WHERE st.id = ? \
                '''
        return self._db_object.execute_query(query, params=(self._user_id,), mode='one')

    @validate_user_methods
    def get_schedule(self):

        query = '''SELECT cg.day_of_week,
                          c.course_name,
                          l.name || ' ' || l.last_name as Lector,
                          cg.group_name || ' - ' || cg.auditorium,
                          cg.class_time,
                          COALESCE(en.grade, 0)        as grade

                   FROM enrollments en
                            JOIN courses_groups cg
                                 ON cg.id = en.group_id
                            JOIN courses c
                                 ON c.id = cg.course_id
                            JOIN lecturers l
                                 ON cg.lecturer_id = l.id
                   WHERE en.student_id = ?
                     AND en.semester = ?
                   ORDER BY CASE cg.day_of_week
                                WHEN 'ორშაბათი' THEN 1
                                WHEN 'სამშაბათი' THEN 2
                                WHEN 'ოთხშაბათი' THEN 3
                                WHEN 'ხუთშაბათი' THEN 4
                                WHEN 'პარასკევი' THEN 5
                                WHEN 'შაბათი' THEN 6
                                ELSE 7
                                END, cg.class_time
                '''
        return self._db_object.execute_query(query, (self._user_id, self._current_semester), mode='all')

    @rollback_decorator
    @validate_user_methods
    def add_subject(self, group_id: int):
        """ჯგუფის აიდით სტუდენტისთვის გასავლელი საგნის დამატება.
            :param group_id: int"""
        if not isinstance(group_id, int):
            raise TypeError(f"group_id {group_id} must be an integer")

        # არჩეული საგნის ინფორმაცია
        query_info = """
                     SELECT c.course_name,
                            c.credits,
                            cg.day_of_week || ' ' || cg.class_time,
                            l.name || ' ' || l.last_name,
                            cg.group_name,
                            cg.max_students,
                            (SELECT COUNT(*)
                             FROM enrollments
                             WHERE group_id = cg.id
                               AND status = 'active') as current_count
                     FROM courses_groups cg
                              JOIN courses c ON cg.course_id = c.id
                              JOIN lecturers l ON cg.lecturer_id = l.id
                     WHERE cg.id = ? \
                     """
        group_info = self._db_object.execute_query(query_info, (group_id,), mode='one')

        if not group_info:
            raise StudentClassError(f'Invalid group_id: {group_id}')

        subject_name, course_credits, class_time, lecturer, group_name, max_students, current_count = group_info

        # ვალიდაციები
        if subject_name in self._enrolled_subjects or subject_name in self.passed_subjects:
            raise StudentClassError(f"Subject: '{subject_name}' has already been chosen/passed.")

        if current_count >= max_students:
            raise StudentClassError(f"max_students count is exceeded!")

        if self.credits + course_credits > 30:
            raise StudentClassError(f"Credit limit is exceed!")

        # ქეშიდან ვამოწმებთ დროებს
        for enrollment in self.current_enrollments_info:
            # enrollment[2] არის კონკრეტული თარიღი ("ორშაბათი 12:00")
            if enrollment[2] == class_time:
                raise StudentClassError(f"You can't chose two subjects at the same time: {enrollment[2]}")

        # მონაცემთა ბაზაში ჩაწერა
        query_insert = """INSERT INTO enrollments(student_id, group_id, grade, semester, status)
                          VALUES (?, ?, ?, ?, ?)"""
        params = (self._user_id, group_id, 0, self._current_semester, "active")

        self._db_object.execute_query(query_insert, params, mode='exec')

        # ქეშის განახლება
        self._enrolled_subjects.append(subject_name)
        self.credits += course_credits
        self.current_enrollments_info.append((subject_name, course_credits, class_time, lecturer, group_name))
        print('successfully added enrollment')

    @rollback_decorator
    @validate_user_methods
    def drop_subject(self, group_id: int):
        """საგნის ამოშლა ჯგუფის აიდის მიხედვით
            :param group_id: int"""
        if not isinstance(group_id, int):
            raise TypeError('group_id must be an integer')

        # საგანზე ინფრომაციის მოძიება
        query_find = """SELECT c.course_name, c.credits
                        FROM courses_groups cg
                                 JOIN courses c ON cg.course_id = c.id
                        WHERE cg.id = ?"""
        res = self._db_object.execute_query(query_find, (group_id,), mode='one')

        if not res:
            raise StudentClassError(f"invalid group_id: {group_id}")

        subject_name, course_credits = res

        # ვამოწმებთა აქვს თუ არა არჩეული ეს საგანი
        if subject_name not in self._enrolled_subjects:
            raise StudentClassError(f"You haven't chosen subject: {subject_name}")

        # წაშლა
        query_delete = """DELETE
                          FROM enrollments
                          WHERE student_id = ?
                            AND group_id = ?
                            AND status = 'active'"""

        self._db_object.execute_query(query_delete, (self._user_id, group_id), mode='exec')

        # ქეშის განახლება
        self._enrolled_subjects.remove(subject_name)
        self.credits -= course_credits
        self.current_enrollments_info = [
            i for i in self.current_enrollments_info if i[0] != subject_name
        ]

    @validate_user_methods
    def show_lecturers_to_review(self):
        """მეთოდი გვიბრუნებს ლექტორებს რომლებიც უნდა შევაფასოთ.
        """

        query = """SELECT DISTINCT l.name || ' ' || l.last_name as lecturer_name,
                                   l.id
                   FROM enrollments en
                            JOIN courses_groups cg
                                 ON en.group_id = cg.id
                            JOIN lecturers l
                                 ON l.id = cg.lecturer_id
                   WHERE en.student_id = ? \
                """

        return self._db_object.execute_query(query, (self._user_id,), mode='all')

    @rollback_decorator
    @validate_user_methods
    def add_review(self, lecturer_id: int, stars: int, description: str = ""):

        if not (1 <= stars <= 5):
            raise ValueError("stars must be from 1 to 5")

        insert_query = """
                       INSERT INTO feedback (lecturer_id, stars, desc)
                       VALUES (?, ?, ?) \
                       """

        self._db_object.execute_query(insert_query, (lecturer_id, stars, description), mode='exec')
        print('successfully added review')
