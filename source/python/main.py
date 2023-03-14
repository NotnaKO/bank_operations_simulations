import logging

from source.python.facade import SessionFacade

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w",
                        encoding='utf-8', format="%(levelname)s %(message)s")
    facade = SessionFacade()
    facade.start_session()
