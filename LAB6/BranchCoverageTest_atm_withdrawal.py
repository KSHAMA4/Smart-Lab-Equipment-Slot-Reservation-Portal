"""Lab 6 - Branch coverage tests for atm_withdrawal.py.

Every decision (if / else) is exercised with both a True and a False outcome,
plus boundary values around each condition.
"""
import pytest
from atm_withdrawal import withdraw, pin_check, note_breakup


# ---------- withdraw: account type ----------
def test_simple_withdrawal():
    assert withdraw(5000, 1000, "savings", True) == 4000


def test_current_account_is_accepted():
    assert withdraw(60000, 40000, "current", True) == 20000


def test_unknown_account_type():
    with pytest.raises(ValueError, match="unknown account"):
        withdraw(5000, 1000, "student", True)


# ---------- withdraw: amount validation ----------
@pytest.mark.parametrize("amount", [0, -100, 150, 1050])
def test_invalid_amounts(amount):
    with pytest.raises(ValueError, match="invalid amount"):
        withdraw(5000, amount, "savings", True)


# ---------- withdraw: daily limit (True / False / boundary) ----------
def test_savings_limit_exceeded():
    assert withdraw(100000, 30000, "savings", True) == "limit exceeded"


def test_savings_exactly_at_limit_is_allowed():
    assert withdraw(30000, 25000, "savings", True) == 5000


def test_savings_just_above_limit_is_rejected():
    assert withdraw(100000, 25100, "savings", True) == "limit exceeded"


def test_current_limit_exceeded():
    assert withdraw(100000, 50100, "current", True) == "limit exceeded"


# ---------- withdraw: fee branches ----------
def test_own_bank_has_no_fee():
    assert withdraw(2000, 2000, "savings", True) == 0


def test_other_bank_small_withdrawal_charges_20():
    assert withdraw(5000, 2000, "savings", False) == 2980


def test_other_bank_exactly_10000_charges_only_20():
    assert withdraw(20000, 10000, "savings", False) == 9980


def test_other_bank_above_10000_charges_30():
    assert withdraw(20000, 10100, "savings", False) == 9870


def test_other_bank_large_withdrawal_charges_extra_fee():
    assert withdraw(20000, 15000, "savings", False) == 4970


# ---------- withdraw: balance check (True / False / boundary) ----------
def test_insufficient_funds():
    assert withdraw(500, 1000, "savings", True) == "insufficient funds"


def test_fee_makes_withdrawal_unaffordable():
    # amount alone fits (1000) but amount + 20 fee does not
    assert withdraw(1000, 1000, "savings", False) == "insufficient funds"


def test_balance_exactly_equal_to_amount_plus_fee():
    assert withdraw(1020, 1000, "savings", False) == 0


# ---------- pin_check ----------
def test_correct_pin():
    assert pin_check(1234, 1234, 0) == "ok"


def test_correct_pin_on_third_try():
    assert pin_check(1234, 1234, 2) == "ok"


def test_wrong_pin_first_attempt_allows_retry():
    assert pin_check(1111, 1234, 0) == "retry"


def test_wrong_pin_second_attempt_allows_retry():
    assert pin_check(1111, 1234, 1) == "retry"


def test_wrong_pin_on_last_attempt_blocks_card():
    assert pin_check(1111, 1234, 2) == "card blocked"


def test_card_blocked_with_three_attempts_even_if_pin_correct():
    assert pin_check(1234, 1234, 3) == "card blocked"


def test_card_blocked_with_more_than_three_attempts():
    assert pin_check(1111, 1234, 5) == "card blocked"


# ---------- note_breakup ----------
@pytest.mark.parametrize("amount", [50, 250, 1001])
def test_note_breakup_invalid_amount(amount):
    with pytest.raises(ValueError, match="invalid amount"):
        note_breakup(amount)


@pytest.mark.parametrize(
    "amount, expected",
    [
        (0, (0, 0, 0)),       # nothing to dispense
        (100, (0, 0, 1)),     # remaining < 200  -> no 200 notes
        (300, (0, 1, 1)),     # remaining >= 200 -> uses a 200 note
        (400, (0, 2, 0)),
        (500, (1, 0, 0)),
        (600, (1, 0, 1)),     # 500 + 100, remaining < 200
        (700, (1, 1, 0)),     # remaining exactly 200
        (2700, (5, 1, 0)),
    ],
)
def test_note_breakup_values(amount, expected):
    assert note_breakup(amount) == expected