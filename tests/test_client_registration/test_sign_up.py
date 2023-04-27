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
