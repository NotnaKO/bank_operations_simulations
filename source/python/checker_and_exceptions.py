class UserNotExists(Exception):
    pass


class UserAlreadyExists(Exception):
    pass


class Checker:
    @classmethod
    def check_if_user_exists(cls, name: str, surname: str):
        pass  # Todo: сделать, когда будет запись в файл
