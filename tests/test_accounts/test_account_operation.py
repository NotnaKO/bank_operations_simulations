import pytest

from conftest import KillInput, sequence_to_create_complete_client, \
    sequence_to_create_credit_with_percent, sequence_to_create_debit, \
    sequence_to_create_tmp_client

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


def test_declined_withdraw(adapter, session, io_for_test):
    io_for_test.extend_answers(
        sequence_to_create_tmp_client + ['tmp tmp', '2'] + sequence_to_create_debit + ['4']
        + sequence_to_make_withdraw[:-1] + ['4500'])
    with pytest.raises(KillInput):
        session.start_session()
    assert "you have a bound" in io_for_test.questions[-2]
    assert adapter.get_client("tmp tmp").accounts[0].balance.value == 5000


def test_declined_transfer(adapter, session, io_for_test):
    io_for_test.extend_answers(
        sequence_to_create_tmp_client + ['tmp tmp',
                                         '2'] + sequence_to_create_debit + ['2']
        + sequence_to_create_debit + ['4', '1', '3', "4500", '2'])
    with pytest.raises(KillInput):
        session.start_session()
    assert "you have a bound" in io_for_test.questions[-2]
    assert adapter.get_client("tmp tmp").accounts[1].balance.value == 5000 == \
           adapter.get_client("tmp tmp").accounts[0].balance.value


def test_transfer_to_the_same_account(adapter, session, io_for_test):
    io_for_test.extend_answers(
        sequence_to_create_complete_client + ['tmp tmp',
                                              '1'] + sequence_to_create_debit + ['1']
        + sequence_to_create_debit + sequence_to_make_transfer[:-1] + ['1'])
    with pytest.raises(KillInput):
        session.start_session()
    assert "same account" in io_for_test.questions[-2]
    assert adapter.get_client("tmp tmp").accounts[1].balance.value == 5000 == \
           adapter.get_client("tmp tmp").accounts[0].balance.value


def test_credit_withdraw(adapter, session, io_for_test):
    io_for_test.extend_answers(
        sequence_to_create_complete_client + ['tmp tmp',
                                              '1']
        + sequence_to_create_credit_with_percent + sequence_to_make_withdraw[:-1] + ["1000"])
    with pytest.raises(KillInput):
        session.start_session()
    assert "succeeded" in io_for_test.questions[-2]
    assert adapter.get_client("tmp tmp").accounts[0].balance.value == 4000
