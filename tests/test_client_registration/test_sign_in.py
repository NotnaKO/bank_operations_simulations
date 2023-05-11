import pytest

from conftest import KillInput, sequence_to_create_tmp_client, sequence_to_log_in_with_tmp
from src.clients import Reliable
from test_sign_up import sequence_to_create_complete_client


def test_saving_users_after_end(session, io_for_test):
    io_for_test.extend_answers(sequence_to_create_complete_client)
    io_for_test.set_end(len(io_for_test.answers) + 1)
    io_for_test.extend_answers(sequence_to_log_in_with_tmp + ['2'])
    with pytest.raises(KillInput, match="Enter"):
        session.start_session()
    io_for_test.reset()
    session.start_session()


def test_log_in_without_registration(session, io_for_test):
    io_for_test.extend_answers(sequence_to_log_in_with_tmp)
    with pytest.raises(KillInput, match="sign in"):
        session.start_session()


def test_complete_information(adapter, session, io_for_test):
    io_for_test.extend_answers(sequence_to_create_tmp_client)
    io_for_test.push_answer("tmp tmp")
    io_for_test.push_answer('1')
    io_for_test.extend_answers(["address", "passport"])
    with pytest.raises(KillInput):
        session.start_session()
    assert adapter.get_client("tmp tmp").type is Reliable
