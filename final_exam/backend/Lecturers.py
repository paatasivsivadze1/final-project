from backend.validations import validate_user_methods, rollback_decorator


class Lecturer:
    """ლექტორის მართვის კლასი."""

    def __init__(self, user_id: int, db_object):
        """:param user_id:
            :param db_object:
            :type  db_object: AppDatabase"""
        self._user_id = user_id
        self._db_object = db_object

    @validate_user_methods
    def get_profile(self):

        query = '''SELECT l.name,
                          l.last_name,
                          u.email,
                          l.age,
                          l.address
                   FROM lecturers l
                            JOIN users u
                                 ON l.id = u.user_id
                   WHERE l.id = ? \
                '''
        res = self._db_object.execute_query(query, params=(self._user_id,), mode='one')

        if res is not None:
            return res
        else:
            raise ValueError('Invalid data')

    @validate_user_methods
    def get_schedule(self):
        """საკუთარი განრიგის ნახვა.
            :return: ((course_name, group_name, schedule, auditorium),(), ())"""
        query = '''SELECT cg.day_of_week,
                          c.course_name,
                          '-',
                          cg.group_name || ' - ' || cg.auditorium,
                          cg.class_time as time,
                          '-'

                   FROM courses_groups cg
                            JOIN courses c
                                 ON c.id = cg.course_id
                   WHERE cg.lecturer_id = ?
                   ORDER BY CASE cg.day_of_week
                                WHEN 'ორშაბათი' THEN 1
                                WHEN 'სამშაბათი' THEN 2
                                WHEN 'ოთხშაბათი' THEN 3
                                WHEN 'ხუთშაბათი' THEN 4
                                WHEN 'პარასკევი' THEN 5
                                WHEN 'შაბათი' THEN 6
                                ELSE 7
                       END \
                          , cg.class_time
                '''
        return self._db_object.execute_query(query, (self._user_id,), mode='all')

    @validate_user_methods
    def show_students_in_group(self):
        """ყველა ჯგუფის მოსწავლის ნახვა ერთად.

            :return: [[(course_name, fullname, group_name, grade) (st_id, group_id)]]"""

        query = """SELECT c.course_name, \
                          st.name || ' ' || st.last_name, \
                          cg.group_name, \
                          en.grade, \
                          st.id, \
                          cg.id


                   FROM enrollments en
                            JOIN courses_groups cg
                                 ON cg.id = en.group_id
                            JOIN courses c
                                 ON c.id = cg.course_id
                            JOIN students st
                                 ON st.id = en.student_id
                   WHERE cg.lecturer_id = ?
                     AND en.status = 'active'"""

        res = self._db_object.execute_query(query, (self._user_id,), mode='iter')

        return [[(tp[0], tp[1], tp[2], tp[3]), (tp[4], tp[5])] for tp in res]

    @rollback_decorator
    @validate_user_methods
    def set_grade(self, group_id, std_id, grade):

        if not isinstance(std_id, int):
            raise TypeError('Student ID must be a integer')

        if not isinstance(grade, int):
            raise TypeError('Grade must be a integer')

        if not 0 <= grade <= 100:
            raise ValueError('Grade must be between 0 and 100')

        query = """UPDATE enrollments
                   SET grade = ?
                   WHERE group_id = ?
                     AND student_id = ?
                     AND status = 'active'"""

        self._db_object.execute_query(query, (grade, group_id, std_id), mode='exec')
