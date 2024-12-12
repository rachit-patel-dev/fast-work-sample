import pytest

from internal.club.league import (
    generate_rounds_and_matches,
    get_total_matches_for_a_season,
    get_total_rounds_for_a_season,
)


@pytest.fixture
def odd_team():
    teams = ["A", "B", "C", "D", "E"]
    return teams


@pytest.fixture
def even_team():
    teams = ["A", "B", "C", "D", "E", "F"]
    return teams


def test_total_round_and_matches(odd_team, even_team):
    total_odd_team = len(odd_team)
    total_match_for_odd_team = get_total_matches_for_a_season(total_odd_team)
    total_round_for_odd_team = get_total_rounds_for_a_season(total_odd_team)
    round_and_matches_odd_team = generate_rounds_and_matches(odd_team)
    assert total_match_for_odd_team == 10
    assert total_round_for_odd_team == 5
    assert round_and_matches_odd_team == [
        [("B", "E"), ("C", "D")],
        [("A", "E"), ("B", "C")],
        [("A", "D"), ("E", "C")],
        [("A", "C"), ("D", "B")],
        [("A", "B"), ("D", "E")],
    ]
    total_even_team = len(even_team)
    total_match_for_even_team = get_total_matches_for_a_season(total_even_team)
    total_round_for_even_team = get_total_rounds_for_a_season(total_even_team)
    round_and_matches_even_team = generate_rounds_and_matches(even_team)
    assert total_match_for_even_team == 15
    assert total_round_for_even_team == 5
    assert round_and_matches_even_team == [
        [("A", "F"), ("B", "E"), ("C", "D")],
        [("A", "E"), ("F", "D"), ("B", "C")],
        [("A", "D"), ("E", "C"), ("F", "B")],
        [("A", "C"), ("D", "B"), ("E", "F")],
        [("A", "B"), ("C", "F"), ("D", "E")],
    ]
