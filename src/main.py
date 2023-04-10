import logging

from src.data_adapter import DataAdapter
from src.session import SessionFacade

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="a",
                        encoding='utf-8', format="%(levelname)s %(message)s")
    with DataAdapter() as adapter:
        facade = SessionFacade(adapter)
        facade.start_session()
