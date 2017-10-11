import pytest

from testing_language import TestLangCBC


@pytest.mark.parametrize(
    'test_string, weights',
    [
        ((  # round robin safety
            'R B0-A S1-A RR1-B RR1-C RR1-D RR1-E S2-E '
            'S3-E S4-E H0-E H1-E H2-E H3-E H4-E C0-A '
            'C1-A C2-A C3-A C4-A R'
            ), [9.3, 8.2, 7.1, 6, 5]),
    ]
)
def test_via_test_lang(test_string, weights):
    test = TestLangCBC(test_string, weights)
    test.parse()


def test_round_robin_safety():
    test_string = (
        'R B0-A S1-A RR1-B RR1-C RR1-D RR1-E S2-E '
        'S3-E S4-E H0-E H1-E H2-E H3-E H4-E C0-A '
        'C1-A C2-A C3-A C4-A R'
    )
    test = TestLangCBC(test_string, [9.3, 8.2, 7.1, 6, 5])
    test.parse()


def test_majority_fork_safe():
    test_string = (
        # create right hand side of fork and check for safety
        'R B1-A S0-A B0-L0 S1-L0 B1-L1 S0-L1 B0-L2 S1-L2 '
        'B1-L3 S0-L3 B0-L4 S1-L4 H1-L4 C1-L0 H0-L4 C0-L0 R '
        # other fork shows safe fork blocks, but they remain stuck
        'S2-A B2-R0 S0-R0 H0-L4 S1-R0 H0-L4 R'
    )

    test = TestLangCBC(test_string, [5, 6, 7])
    test.parse()


def test_no_majority_fork_unsafe():
    test_string = (
        # create right hand side of fork and check for no safety
        'R B2-A S1-A B1-L0 S0-L0 B0-L1 S1-L1 B1-L2 S0-L2 '
        'B0-L3 S1-L3 B1-L4 S0-L4 H0-L4 U0-L0 H1-L4 U1-L0 R '
        # now, left hand side as well. still no safety
        'S3-A B3-R0 S4-R0 B4-R1 S3-R1 B3-R2 S4-R2 B4-R3 '
        'S3-R3 B3-R4 S4-R4 H4-R4 U4-R0 H3-R4 U3-R0 R'
    )
    test = TestLangCBC(test_string, [5, 4.5, 6, 4, 5.25])
    test.parse()


def test_no_majority_fork_safe_after_union():
    test_string = (
        # generate both sides of an extended fork
        'R B2-A S1-A B1-L0 S0-L0 B0-L1 S1-L1 B1-L2 S0-L2 '
        'B0-L3 S1-L3 B1-L4 S0-L4 H0-L4 U0-L0 H1-L4 U1-L0 R '
        'S3-A B3-R0 S4-R0 B4-R1 S3-R1 B3-R2 S4-R2 B4-R3 '
        'S3-R3 B3-R4 S4-R4 H4-R4 U4-R0 H3-R4 U3-R0 R '
        # show all validators all blocks
        'S0-R4 S1-R4 S2-R4 S2-L4 S3-L4 S4-L4 '
        # check all have correct forkchoice
        'H0-L4 H1-L4 H2-L4 H3-L4 H4-L4 '
        # two rounds of round robin, check have safety on the correct fork
        'RR0-J0 RR0-J1 C0-L0 R'
    )
    test = TestLangCBC(test_string, [5, 4.5, 6, 4, 5.25])
    test.parse()
