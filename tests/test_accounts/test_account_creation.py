import pytest

from conftest import KillInput, sequence_to_create_complete_client, \
    sequence_to_create_credit_with_fixed, \
    sequence_to_create_credit_with_percent, sequence_to_create_debit
from src import Credit, Debit, Deposit, FixedCommission, PercentCommission


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


def test_credit_with_fixed_commission_creation(adapter, session, io_for_test):
    io_for_test.extend_answers(sequence_to_create_complete_client)
    io_for_test.push_answer("tmp tmp")
    io_for_test.push_answer('1')
    io_for_test.extend_answers(sequence_to_create_credit_with_fixed)
    with pytest.raises(KillInput, match="view your accounts"):
        session.start_session()
    account = adapter.get_client("tmp tmp").accounts[0]
    assert isinstance(account, Credit)
    commission = account.commission
    assert isinstance(commission,
                      FixedCommission) and commission.commission.value == 5


def test_credit_with_percent_commission_creation(adapter, session, io_for_test):
    io_for_test.extend_answers(sequence_to_create_complete_client)
    io_for_test.push_answer("tmp tmp")
    io_for_test.push_answer('1')
    io_for_test.extend_answers(sequence_to_create_credit_with_percent)
    with pytest.raises(KillInput, match="view your accounts"):
        session.start_session()
    account = adapter.get_client("tmp tmp").accounts[0]
    assert isinstance(account, Credit)
    commission = account.commission
    assert isinstance(commission,
                      PercentCommission) and isinstance(commission.percent,
                                                        float) and commission.percent == 5


def test_negative_sum(session, io_for_test):
    io_for_test.extend_answers(sequence_to_create_complete_client)
    io_for_test.push_answer("tmp tmp")
    io_for_test.push_answer('1')
    io_for_test.extend_answers(['1', '-478', "01.01.2002", '3'])
    io_for_test.set_end(len(io_for_test.answers) + 1)
    with pytest.raises(KillInput):
        session.start_session()
    assert "negative sum" in io_for_test.questions[-2]


def test_create_many_accounts(session, io_for_test):
    io_for_test.extend_answers(sequence_to_create_complete_client)
    io_for_test.push_answer("tmp tmp")
    for i in (sequence_to_create_debit, sequence_to_create_credit_with_fixed,
              sequence_to_create_credit_with_percent):
        io_for_test.push_answer('1')
        io_for_test.extend_answers(i)
    io_for_test.push_answer('2')
    with pytest.raises(KillInput, match="view your accounts"):
        session.start_session()
    assert "Credit" in io_for_test.questions[-2] and "percent" in io_for_test.questions[-2]
    assert "Credit" in io_for_test.questions[-3] and "fixed" in io_for_test.questions[-3]
    assert "Debit" in io_for_test.questions[-4]


def test_not_sum(session, io_for_test):
    io_for_test.extend_answers(sequence_to_create_complete_client)
    io_for_test.push_answer("tmp tmp")
    io_for_test.push_answer('1')
    io_for_test.extend_answers(['1', 'aaaa'])
    io_for_test.set_end(len(io_for_test.answers) + 1)
    with pytest.raises(KillInput):
        session.start_session()
    assert "should be integer" in io_for_test.questions[-2]


def test_bad_percent_commission(session, io_for_test):
    io_for_test.extend_answers(sequence_to_create_complete_client)
    io_for_test.push_answer("tmp tmp")
    io_for_test.push_answer('1')
    io_for_test.extend_answers(['3', '2', "aaa"])
    with pytest.raises(KillInput, match="Choose the type of "):
        session.start_session()
    assert "should be an integer or a float" in io_for_test.questions[-2]


def test_bad_fixed_commission(session, io_for_test):
    io_for_test.extend_answers(sequence_to_create_complete_client)
    io_for_test.push_answer("tmp tmp")
    io_for_test.push_answer('1')
    io_for_test.extend_answers(['3', '1', "aaa"])
    with pytest.raises(KillInput, match="Choose the type of "):
        session.start_session()
    assert "should be an integer" in io_for_test.questions[-2]


def test_deposit_with_bad_date(adapter, session, io_for_test):
    io_for_test.extend_answers(sequence_to_create_complete_client)
    io_for_test.push_answer("tmp tmp")
    io_for_test.push_answer('1')
    io_for_test.extend_answers(['2'] + ["5000", "aaa"])
    with pytest.raises(KillInput):
        session.start_session()
    assert "DD.MM.YYYY" in io_for_test.questions[-2]
