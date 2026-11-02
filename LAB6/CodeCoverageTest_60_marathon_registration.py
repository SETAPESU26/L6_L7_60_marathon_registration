"""Line/code coverage tests for marathon_registration.py."""
import pytest

from marathon_registration import entry_fee, start_wave, finisher_status


def test_entry_fee_standard_10k():
    assert entry_fee("10k", 30, False, False) == 800


def test_entry_fee_early_bird():
    assert entry_fee("5k", 30, True, False) == 375


def test_entry_fee_senior_discount():
    assert entry_fee("10k", 65, False, False) == 400


def test_entry_fee_tshirt_addon():
    assert entry_fee("5k", 30, False, True) == 800


def test_entry_fee_combined_discounts_and_tshirt():
    # 25% early-bird discount, then senior half-price, then T-shirt.
    assert entry_fee("10k", 70, True, True) == 600


def test_entry_fee_invalid_race():
    with pytest.raises(ValueError, match="unknown race"):
        entry_fee("ultra", 30, False, False)


def test_entry_fee_under_minimum_age():
    with pytest.raises(ValueError, match="too young"):
        entry_fee("5k", 11, False, False)


def test_entry_fee_underage_for_half_marathon():
    with pytest.raises(ValueError, match="too young for this distance"):
        entry_fee("half", 17, False, False)


def test_entry_fee_underage_for_full_marathon():
    with pytest.raises(ValueError, match="too young for this distance"):
        entry_fee("full", 16, False, False)


def test_entry_fee_adult_half_marathon():
    assert entry_fee("half", 18, False, False) == 1200


def test_first_timer_wave():
    assert start_wave(None, "full") == "D"


def test_start_wave_a_full():
    assert start_wave(180, "full") == "A"


def test_start_wave_b_5k():
    assert start_wave(100, "5k") == "B"


def test_start_wave_c_10k():
    assert start_wave(121, "10k") == "C"


def test_finisher_within_5k_limit():
    assert finisher_status(90, "5k", 0) == "finisher"


def test_dnf_after_5k_limit():
    assert finisher_status(91, "5k", 0) == "DNF"


def test_full_marathon_finisher():
    assert finisher_status(360, "full", 0) == "finisher"


def test_half_marathon_dnf():
    assert finisher_status(181, "half", 0) == "DNF"


def test_missed_checkpoint_disqualified():
    assert finisher_status(60, "5k", 1) == "DSQ"
