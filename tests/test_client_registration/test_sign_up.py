from contextlib import suppress

import pytest

from conftest import KillInput, sequence_to_create_complete_client, sequence_to_create_tmp_client
from src.clients import NotReliable, Reliable
from src.session import SessionFacade


def test_not_reliable_type_in_registration(adapter, io_for_test):
    session = SessionFacade(adapter, io_for_test)
    io_for_test.extend_answers(sequence_to_create_tmp_client)
    with suppress(KillInput):
        session.start_session()
    assert adapter.get_client("tmp tmp").type is NotReliable


def test_reliable_type_in_registration(adapter, io_for_test):
    session = SessionFacade(adapter, io_for_test)
    io_for_test.extend_answers(sequence_to_create_complete_client)
    with suppress(KillInput):
        session.start_session()
    assert adapter.get_client("tmp tmp").type is Reliable


def test_start_bad_input(session, io_for_test):
    io_for_test.push_answer('0')
    with pytest.raises(KillInput, match="should be 1 or 2"):
        session.start_session()
    io_for_test.push_answer('1')
    io_for_test.push_answer('aaa')
    with pytest.raises(KillInput):
        session.start_session()
    assert "two words" in io_for_test.questions[-2]


def test_double_sign_up(session, io_for_test):
    for i in range(2):
        io_for_test.push_answer('1')
        io_for_test.extend_answers(sequence_to_create_complete_client)
        with pytest.raises(KillInput, match="Enter your name and surname" if i == 0 else ''):
            session.start_session()
    assert "already exists" in io_for_test.questions[-2]


def test_with_passport_and_without_address(adapter, io_for_test):
    session = SessionFacade(adapter, io_for_test)
    io_for_test.extend_answers(sequence_to_create_complete_client[:-1] + [''])
    with suppress(KillInput):
        session.start_session()
    assert adapter.get_client("tmp tmp").type is NotReliable


def test_with_address_and_without_passport(adapter, io_for_test):
    session = SessionFacade(adapter, io_for_test)
    io_for_test.extend_answers(sequence_to_create_tmp_client[:-1] + ["passport"])
    with suppress(KillInput):
        session.start_session()
    assert adapter.get_client("tmp tmp").type is NotReliable
