from src.data_adapter import DataAdapter
from src.session import SessionFacade

if __name__ == '__main__':
    with DataAdapter() as adapter:
        facade = SessionFacade(adapter)
        facade.start_session()
