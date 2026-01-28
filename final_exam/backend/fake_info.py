
from faker import Faker
import random
from bcrypt import hashpw, gensalt

from backend.validations import rollback_decorator


class FakeInfo:
    """მონაცემთა ბაზის ყალბი ინფორმაციის შესავსები კლასი."""

    def __init__(self, db_object):
        """:param db_object: მონაცემთა ბაზის სამართავი ობიექტი
            :type db_object: AppDatabase"""
        self._db_object = db_object
        self._faker = Faker(['ka_GE'])
        self._students_ids = []
        self._lecturers_ids = []
        self._courses_ids = []

    @staticmethod
    def translate(word):
        """თარგმნის ქართულ ასოებს ინგლისურ ენაზე.
            :param word: სიტყვა რომლის თარგმნაც გვვსურს
            :return: ლათინური str-ი
            """
        ka_to_en = str.maketrans({
            'ა': 'a', 'ბ': 'b', 'გ': 'g', 'დ': 'd', 'ე': 'e', 'ვ': 'v', 'ზ': 'z',
            'თ': 'T', 'ი': 'i', 'კ': 'k', 'ლ': 'l', 'მ': 'm', 'ნ': 'n', 'ო': 'o',
            'პ': 'k', 'ჟ': 'J', 'რ': 'r', 'ს': 's', 'ტ': 't', 'უ': 'u', 'ფ': 'f',
            'ქ': 'q', 'ღ': 'R', 'ყ': 'y', 'შ': 'S', 'ჩ': 'C', 'ც': 'c', 'ძ': 'Z',
            'წ': 'w', 'ჭ': 'W', 'ხ': 'x', 'ჯ': 'j', 'ჰ': 'h'
        })
        return word.translate(ka_to_en)

    @rollback_decorator
    def insert_fake_users(self, count: int = 50, role: str = 'student'):
        """ყალბი მომხმარებლების გენერაცია და მონაცემთა ბაზის ფაილში ჩაწერა.
            :param count: მომხმარებელთა რაოდენობა
            :param role: მომხმარებლის როლი: lecturer, student
            """

        role = role.lower()
        if role not in ('student', 'lecturer'):
            raise ValueError('role must be student or lecturer')

        for i in range(count):
            user_query = """INSERT INTO users(email,
                                              password,
                                              role)
                            VALUES (?, ?, ?)"""

            name = self._faker.first_name()
            last_name = self._faker.last_name()
            age = random.randint(18, 50)
            address = self._faker.address()
            email = self.translate(name) + '.' + self.translate(last_name) + str(age % 10) + "@uni.edu.ge"
            password = hashpw(self._faker.password().encode('utf8'), gensalt(12))
            user_id = self._db_object.execute_query(user_query, (email, password, role), mode='exec')

            # სტუდენტის ჩასმა
            if role == 'student':
                self._students_ids.append(user_id)

                query = """INSERT INTO students(id,
                                                name,
                                                last_name,
                                                age,
                                                address)
                           Values (?, ?, ?, ?, ?)"""

                self._db_object.execute_query(query, (user_id, name, last_name, age, address), mode='exec')

                # ლექტორის ჩასმა
            elif role == 'lecturer':
                self._lecturers_ids.append(user_id)

                query = """INSERT INTO lecturers(id,
                                                 name,
                                                 last_name,
                                                 age,
                                                 address)
                           Values (?, ?, ?, ?, ?)"""

                self._db_object.execute_query(query, (user_id, name, last_name, age, address), mode='exec')

    @rollback_decorator
    def generate_fake_subjects(self):
        """საგნების და კრედიტების სტატიკური გენერირება."""
        courses_data = {"პროგრამირების საფუძვლები (Python)": 6,
                        "მონაცემთა სტრუქტურები და ალგორითმები": 6,
                        "მონაცემთა ბაზების მართვის სისტემები": 5,
                        "ვებ-ტექნოლოგიები (HTML/CSS/JS)": 5,
                        "კალკულუსი I": 6,
                        "კალკულუსი II": 6,
                        "კომპიუტერული ქსელები": 5,
                        "ოპერაციული სისტემები": 5,
                        "ობიექტზე ორიენტირებული პროგრამირება (C++)": 6,
                        "პროგრამული ინჟინერია": 5,
                        "ხელოვნური ინტელექტი": 6,
                        "კიბერუსაფრთხოების საფუძვლები": 5,
                        "დისკრეტული მათემატიკა": 5,
                        "კომპიუტერული არქიტექტურა": 5,
                        "მობილური აპლიკაციების დეველოპმენტი": 6,
                        "ციფრული მარკეტინგი": 4,
                        "ბიზნესის ადმინისტრირება": 4,
                        "სტატისტიკა და ალბათობის თეორია": 5,
                        "ღრუბლოვანი გამოთვლები (Cloud Computing)": 5,
                        "მანქანური სწავლება (Machine Learning)": 6}

        query = '''INSERT INTO courses(course_name,
                                       credits)
                   VALUES (?, ?)
                '''

        for key, value in courses_data.items():
            course_id = self._db_object.execute_query(query, (key, value), mode='exec')
            self._courses_ids.append(course_id)

    @rollback_decorator
    def generate_fake_groups_and_enrollments(self, students_per_course: int = 80):
        """ჯგუფების და enrollments ცხრილის შევსება.
            :param students_per_course: სტუდენტთა რაოდენობა კურსზე."""
        days = ['ორშაბათი', 'სამშაბათი', 'ოთხშაბათი', 'ხუთშაბათი', 'პარასკევი']
        times = ['10:00', '12:00', '14:00', '16:00', '19:00']

        for course_id in self._courses_ids:
            # თითო საგანზე 1-2 ჯგუფი
            for i in range(random.randint(1, 2)):
                lecturer_id = random.choice(self._lecturers_ids)
                group_name = f"{i + 1}0{random.randint(1, 9)}"  # მაგ: 101, 204

                group_query = """INSERT INTO courses_groups (course_id, lecturer_id, group_name,
                                                             day_of_week, auditorium, class_time, max_students)
                                 VALUES (?, ?, ?, ?, ?, ?, ?)"""

                group_params = (course_id, lecturer_id, group_name,
                                random.choice(days), f"Auditorium {random.randint(100, 500)}",
                                random.choice(times), students_per_course)

                group_id = self._db_object.execute_query(group_query, group_params, mode='exec')

                # შემთხვევით ვირჩევთ სტუდენტს და გარანტირებულად ვიტოვებთ თითო ჯგუფიში სულ ცოტა 20 ადგილს.
                selected_students = random.sample(self._students_ids,
                                                  k=min(len(self._students_ids), students_per_course) - 20)

                for std_id in selected_students:
                    # შემთხვევით ვირჩევთ სტუდენტისთვის მის სტატუსს, ნიშანს და სემესტრს
                    status = random.choice(['passed', 'failed', 'active'])
                    grade = random.randint(20, 100) if status != 'active' else 0
                    semester = random.randint(1, 7)

                    enroll_query = """INSERT INTO enrollments (student_id, group_id, grade, semester, status)
                                      VALUES (?, ?, ?, ?, ?)"""
                    self._db_object.execute_query(enroll_query, (std_id, group_id, grade, semester, status),
                                                  mode='exec')

    def generate_fake_reviews(self, min_reviews: int = 50, max_reviews: int = 100):
        """ყალბი ჩანაწერების გენერირება feedback ცხრილში
            :param min_reviews: მინიმალური feedback ჩანაწერების რაოდენობა თითო ლექტორისთვის
            :param max_reviews: მაქსიმალური feedback ჩანაწერების რაოდენობა თითო ლექტორისთვის
            """

        for l_id in self._lecturers_ids:

            query = """INSERT INTO feedback (lecturer_id,
                                             stars,
                                             desc)
                       VALUES (?, ?, ?)"""

            # თითო ლექტორზე  [min_reviews, max_reviews] - დიაპაზონდან ვირჩევთ ჩანაწერთა რაოდენობას
            for _ in range(random.randint(min_reviews, max_reviews)):
                insert_data = (l_id, random.randint(3, 5), '')

                self._db_object.execute_query(query, insert_data, mode='exec')

    @rollback_decorator
    def init_schema(self):
        self.insert_fake_users(500)
        self.insert_fake_users(80, 'lecturer')
        self.generate_fake_subjects()
        self.generate_fake_groups_and_enrollments()
        self.generate_fake_reviews(min_reviews=50, max_reviews=100)
