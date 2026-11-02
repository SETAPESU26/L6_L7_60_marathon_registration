"""Decision/branch coverage tests for marathon_registration.py."""
import pytest

from marathon_registration import entry_fee, start_wave, finisher_status


@pytest.mark.parametrize("race, age, expected", [
    ("5k", 30, 500),       # not half/full; adult
    ("half", 18, 1200),    # half/full condition true; age condition false
    ("full", 18, 1800),    # full distance accepted
    ("5k", 11, "too young"),
    ("half", 17, "too young for this distance"),
    ("full", 17, "too young for this distance"),
])
def test_race_and_age_decision_branches(race, age, expected):
    if isinstance(expected, str):
        with pytest.raises(ValueError, match=expected):
            entry_fee(race, age, False, False)
    else:
        assert entry_fee(race, age, False, False) == expected


def test_unknown_race_branch():
    with pytest.raises(ValueError, match="unknown race"):
        entry_fee("10-mile", 25, False, False)


@pytest.mark.parametrize("early_bird, age, tshirt, expected", [
    (False, 30, False, 500),
    (True, 30, False, 375),
    (False, 65, False, 250),
    (False, 30, True, 800),
    (True, 65, True, 487),
])
def test_fee_adjustment_branches(early_bird, age, tshirt, expected):
    assert entry_fee("5k", age, early_bird, tshirt) == expected


@pytest.mark.parametrize("best_time, race, expected", [
    (None, "full", "D"),
    (180, "full", "A"),
    (90, "5k", "A"),
    (100, "5k", "B"),
    (121, "5k", "C"),
])
def test_start_wave_decision_branches(best_time, race, expected):
    assert start_wave(best_time, race) == expected


@pytest.mark.parametrize("elapsed, race, missed, expected", [
    (60, "5k", 0, "finisher"),
    (91, "5k", 0, "DNF"),
    (360, "full", 0, "finisher"),
    (361, "full", 0, "DNF"),
    (180, "half", 0, "finisher"),
    (181, "half", 0, "DNF"),
    (500, "full", 1, "DSQ"),
])
def test_finisher_status_decision_branches(elapsed, race, missed, expected):
    assert finisher_status(elapsed, race, missed) == expected
