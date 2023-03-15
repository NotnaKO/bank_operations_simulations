from source.python.data_adapter import DataAdapter


class Checker:
    _adapter = DataAdapter()

    @classmethod
    def check_if_user_exists(cls, name: str, surname: str):
        cls._adapter.get_client(name, surname)
