import pytest

from conftest import KillInput
from src.clients import NotReliable, Reliable
from src.session import SessionFacade

sequence_to_create_tmp_client = ["1", "tmp tmp", '', '', "tmp tmp", '3']
sequence_to_create_complete_client = ["1", "tmp tmp", 'address', 'passport', "tmp tmp", '2']


def test_not_reliable_type_in_registration(adapter, io_for_test):
    session = SessionFacade(adapter, io_for_test)
    io_for_test.extend_answers(sequence_to_create_tmp_client)
    session.start_session()
    assert adapter.get_client("tmp tmp").type is NotReliable


def test_reliable_type_in_registration(adapter, io_for_test):
    session = SessionFacade(adapter, io_for_test)
    io_for_test.extend_answers(sequence_to_create_complete_client)
    session.start_session()
    assert adapter.get_client("tmp tmp").type is Reliable


def test_start_bad_input(adapter, io_for_test):
    session = SessionFacade(adapter, io_for_test)
    io_for_test.push_answer('0')
    io_for_test.set_end(2)
    with pytest.raises(KillInput, match="should be 1 or 2"):
        session.start_session()
