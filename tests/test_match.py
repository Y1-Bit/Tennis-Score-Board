import pytest
from tennis_score_board.domain.match import Match

def test_deuce_scenario():
    match = Match.create(player1_id=1, player2_id=2)
    
    for _ in range(3):
        match.add_point("player1")
        match.add_point("player2")
    
    assert match.score["player1"] == 3  
    assert match.score["player2"] == 3  
    assert match.score["set1"]["player1"] == 0
    assert match.score["set1"]["player2"] == 0

    match.add_point("player1")
    
    assert match.score["player1"] == 4 
    assert match.score["player2"] == 3
    assert match.score["set1"]["player1"] == 0
    assert match.score["set1"]["player2"] == 0

def test_win_game_40_0():
    match = Match.create(player1_id=1, player2_id=2)
    
    for _ in range(3):
        match.add_point("player1")
    
    assert match.score["player1"] == 3  
    assert match.score["player2"] == 0
    assert match.score["set1"]["player1"] == 0
    assert match.score["set1"]["player2"] == 0

    match.add_point("player1")
    
    assert match.score["player1"] == 0
    assert match.score["player2"] == 0
    assert match.score["set1"]["player1"] == 1
    assert match.score["set1"]["player2"] == 0

def test_tiebreak_at_6_6():
    match = Match.create(player1_id=1, player2_id=2)
    
    for _ in range(6):
        match.add_point("player1")
        match.add_point("player2")

    assert match.score["player1"] == 6
    assert match.score["player2"] == 6

    match.add_point("player1")

    assert match.score["player1"] == 7
    assert match.score["player2"] == 6

    match.add_point("player1")

    assert match.score["player1"] == 0
    assert match.score["player2"] == 0

    assert match.score["set1"]["player1"] == 1
    assert match.score["set1"]["player2"] == 0

if __name__ == "__main__":
    pytest.main()