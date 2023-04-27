import pytest

from conftest import KillInput, sequence_to_create_complete_client, sequence_to_create_credit, \
    sequence_to_create_debit
from src import Credit, Debit, Deposit


def test_debit_creation(adapter, session, io_for_test):
    io_for_test.extend_answers(sequence_to_create_complete_client)
    io_for_test.push_answer("tmp tmp")
    io_for_test.push_answer('1')
    io_for_test.extend_answers(sequence_to_create_debit)
    io_for_test.set_end(len(io_for_test.answers) + 1)
    with pytest.raises(KillInput, match="view your accounts"):
        session.start_session()
    assert isinstance(adapter.get_client("tmp tmp").accounts[0], Debit)


def test_deposit_creation(adapter, session, io_for_test):
    io_for_test.extend_answers(sequence_to_create_complete_client)
    io_for_test.push_answer("tmp tmp")
    io_for_test.push_answer('1')
    io_for_test.extend_answers(['2'] + sequence_to_create_debit[1:])
    io_for_test.push_answer("1")
    io_for_test.set_end(len(io_for_test.answers) + 1)
    with pytest.raises(KillInput, match="Debit"):
        session.start_session()
    assert isinstance(adapter.get_client("tmp tmp").accounts[0], Deposit)


def test_credit_creation(adapter, session, io_for_test):
    io_for_test.extend_answers(sequence_to_create_complete_client)
    io_for_test.push_answer("tmp tmp")
    io_for_test.push_answer('1')
    io_for_test.extend_answers(sequence_to_create_credit)
    io_for_test.set_end(len(io_for_test.answers) + 1)
    with pytest.raises(KillInput, match="view your accounts"):
        session.start_session()
    assert isinstance(adapter.get_client("tmp tmp").accounts[0], Credit)


def test_negative_sum(session, io_for_test):
    io_for_test.extend_answers(sequence_to_create_complete_client)
    io_for_test.push_answer("tmp tmp")
    io_for_test.push_answer('1')
    io_for_test.extend_answers(['1', '-478', "01.01.2002", '3'])
    io_for_test.set_end(len(io_for_test.answers) + 1)
    with pytest.raises(KillInput):
        session.start_session()
    assert "negative sum" in io_for_test.questions[-2]


def test_not_sum(session, io_for_test):
    io_for_test.extend_answers(sequence_to_create_complete_client)
    io_for_test.push_answer("tmp tmp")
    io_for_test.push_answer('1')
    io_for_test.extend_answers(['1', 'aaaa'])
    io_for_test.set_end(len(io_for_test.answers) + 1)
    with pytest.raises(KillInput):
        session.start_session()
    assert "should be integer" in io_for_test.questions[-2]
