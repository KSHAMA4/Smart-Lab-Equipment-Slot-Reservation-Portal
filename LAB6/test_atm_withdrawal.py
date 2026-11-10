import pytest
from atm_withdrawal import withdraw, pin_check, note_breakup

#Example test cases:
def test_simple_withdrawal():
    assert withdraw(5000, 1000, "savings", True) == 4000

def test_correct_pin():
    assert pin_check(1234, 1234, 0) == "ok"

#Write the rest of the test cases so that the code is 90- 100% covered.
