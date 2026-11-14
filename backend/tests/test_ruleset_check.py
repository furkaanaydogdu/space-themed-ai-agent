# Deliberately failing test to check that the main ruleset blocks a red CI run.
# Delete this file once the ruleset test is done; it must never reach main.


def test_fails_on_purpose_to_check_ruleset() -> None:
    expected = 2
    assert expected + 1 == 1 + 1
