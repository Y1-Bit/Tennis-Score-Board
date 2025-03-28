import pytest

from tennis_score_board.domain.match import Match
from tennis_score_board.domain.player import Player

player1 = Player(id=1, name="Player 1")
player2 = Player(id=2, name="Player 2")


def test_deuce_scenario():
    match = Match.create(player1, player2)

    for _ in range(3):
        match.add_point("player1")
        match.add_point("player2")

    assert match.score.current_game.player1 == 3
    assert match.score.current_game.player1 == 3
    assert match.score.set1.player1 == 0
    assert match.score.set1.player2 == 0

    match.add_point("player1")

    assert match.score.current_game.player1 == 4
    assert match.score.current_game.player2 == 3
    assert match.score.set1.player1 == 0
    assert match.score.set1.player2 == 0


def test_win_game_40_0():
    match = Match.create(player1, player2)

    for _ in range(3):
        match.add_point("player1")

    assert match.score.current_game.player1 == 3
    assert match.score.current_game.player2 == 0
    assert match.score.set1.player1 == 0
    assert match.score.set2.player2 == 0

    match.add_point("player1")

    assert match.score.current_game.player1 == 0
    assert match.score.current_game.player2 == 0
    assert match.score.set1.player1 == 1
    assert match.score.set2.player2 == 0


def test_tiebreak_at_6_6():
    match = Match.create(player1, player2)

    for _ in range(6):
        match.add_point("player1")
        match.add_point("player2")

    assert match.score.current_game.player1 == 6
    assert match.score.current_game.player2 == 6

    match.add_point("player1")

    assert match.score.current_game.player1 == 7
    assert match.score.current_game.player2 == 6

    match.add_point("player1")

    assert match.score.current_game.player1 == 0
    assert match.score.current_game.player2 == 0

    assert match.score.set1.player1 == 1
    assert match.score.set1.player2 == 0


if __name__ == "__main__":
    pytest.main()
