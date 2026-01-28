"""შემოწმებებისთვის საჭირო დეკორატორები"""

from functools import wraps  # დეკორირებული ფუნქციის ორიგინალური Docstring-ის შესანახად


class DataBaseError(Exception):
    """მონაცემთა ბაზასთან დაკავშირებული Error-ების გენერაციის კლასი"""

    pass


class AuthentificationError(Exception):
    """Authentification კლასთან დაკავშირებული Error-ების გენერაციის კლასი"""
    pass


def validate_db_status(func):
    """მონაცემთა ბაზასთან კავშირის შემოწმება მეთოდის გაშვებამდე.

       გამოიყენება AppDatabase-კლასში.
       :raise: DataBaseError თუ მონაცემთა ბაზა დაკეტილია
        :return: მონაცემთა ბაზის მეთოდი
        """

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self._status:
            raise DataBaseError("DB is closed!")
        return func(self, *args, **kwargs)

    return wrapper


def cls_str_checker(func):
    """უზრუნველყოფს რომ ძირითად ფუნქციას მიეწოდება არაცარიელი სტრინგი.

       :raise: TypeError | ValueError
        """

    @wraps(func)
    def wrapper(self, string, *args, **kwargs):
        if not isinstance(string, str):
            raise TypeError(f'{func.__name__} You must enter str')

        if not string:
            raise ValueError(f'{func.__name__} an empty string')

        return func(self, string, *args, **kwargs)

    return wrapper


def validate_registration_update(func):
    """უზრუნველყოფს რომ რეგისტრაციისთვის საჭირო ინფორმაცია სწორ ფორმატშია.

        მუშაობს Authentification კლასის add_user ან update_user -მეთოდებთან
        :raise: ValueError | TypeError"""

    @wraps(func)
    def wrapper(self, *args, **kwargs):

        if func.__name__ == 'add_user':
            mail, password, name, last_name, age, address, role = args

        else:
            mail, password, name, last_name, age, address, role = args[1:]

        self._validate_mail(mail)

        if '$' not in password:
            self._validate_password(password)


        if func.__name__ == 'add_user' and self._mail_is_exists(mail):
            raise AuthentificationError("Mail Already Exists")

        if not isinstance(name, str):
            raise TypeError("Name must be a string")

        if not isinstance(last_name, str):
            raise TypeError("Last Name must be a string")

        if not isinstance(age, int):
            raise ValueError("Age Must Be An Integer")

        if not isinstance(address, str):
            raise TypeError("Address Must Be An String")

        if not isinstance(role, str):
            raise TypeError("Role Must Be An String")

        if not role in ('student', 'lecturer', 'admin'):
            raise ValueError("You must enter 'student' or 'lecturer' or admin")

        return func(self, *args, **kwargs)

    return wrapper



def validate_user_methods(func):
    """"""

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not hasattr(self, '_user_id') or self._user_id is None:
            raise AttributeError('"user_id" is not identified')

        if not isinstance(self._user_id, int):
            raise TypeError('"user_id" must be an integer')

        if not hasattr(self, '_db_object') or self._db_object is None:
            raise AttributeError('"db_object" is not identified')

        if not hasattr(self._db_object, 'execute_query'):
            raise TypeError('"db_object" must be a Database')

        return func(self, *args, **kwargs)

    return wrapper


def rollback_decorator(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            res = func(self, *args, **kwargs)
            self._db_object.commit()
            return res

        except Exception as e:
            self._db_object.rollback()
            print(f'Unexpected Error during {func.__name__}: {e}')
            raise e

    return wrapper


def error_catcher(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            print(f'Unexpected Error during {func.__name__}: {e}')
            raise e

    return wrapper
