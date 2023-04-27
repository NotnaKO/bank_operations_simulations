import pytest

from conftest import KillInput, sequence_to_create_complete_client, sequence_to_create_debit

sequence_to_make_withdraw = ['3', '1', '1', '1']
sequence_to_make_put = ['3', '1', '2', '1']
sequence_to_make_transfer = ['3', '1', '3', '1', '2']


def test_withdraw(adapter, session, io_for_test):
    io_for_test.extend_answers(
        sequence_to_create_complete_client + ['tmp tmp', '1'] + sequence_to_create_debit
        + sequence_to_make_withdraw)
    with pytest.raises(KillInput):
        session.start_session()
    assert "succeeded" in io_for_test.questions[-2]
    assert adapter.get_client("tmp tmp").accounts[0].balance.value == 4999


def test_put(adapter, session, io_for_test):
    io_for_test.extend_answers(
        sequence_to_create_complete_client + ['tmp tmp', '1'] + sequence_to_create_debit
        + sequence_to_make_put)
    with pytest.raises(KillInput):
        session.start_session()
    assert "succeeded" in io_for_test.questions[-2]
    assert adapter.get_client("tmp tmp").accounts[0].balance.value == 5001


def test_transfer(adapter, session, io_for_test):
    io_for_test.extend_answers(
        sequence_to_create_complete_client + ['tmp tmp',
                                              '1'] + sequence_to_create_debit + ['1']
        + sequence_to_create_debit + sequence_to_make_transfer)
    with pytest.raises(KillInput):
        session.start_session()
    assert "succeeded" in io_for_test.questions[-2]
    assert adapter.get_client("tmp tmp").accounts[1].balance.value == 5001 and \
           adapter.get_client("tmp tmp").accounts[0].balance.value == 4999
