import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from casino.games.poker.poker import hand_score, hand_name, get_card_value, evaluate_hand
from casino.cards import StandardCard


class TestPoker:
    
    def test_get_card_value(self):
        """Test card value conversion"""
        assert get_card_value("2") == 2
        assert get_card_value("10") == 10
        assert get_card_value("J") == 11
        assert get_card_value("Q") == 12
        assert get_card_value("K") == 13
        assert get_card_value("A") == 14
    
    def test_evaluate_hand_high_card(self):
        """Test high card hand evaluation"""
        cards = [
            StandardCard("2", "hearts"),
            StandardCard("5", "spades"),
            StandardCard("8", "diamonds"),
            StandardCard("J", "clubs"),
            StandardCard("A", "hearts")
        ]
        assert evaluate_hand(cards) == 1  # High card
    
    def test_evaluate_hand_one_pair(self):
        """Test one pair hand evaluation"""
        cards = [
            StandardCard("2", "hearts"),
            StandardCard("2", "spades"),
            StandardCard("8", "diamonds"),
            StandardCard("J", "clubs"),
            StandardCard("A", "hearts")
        ]
        assert evaluate_hand(cards) == 2  # One pair
    
    def test_evaluate_hand_two_pair(self):
        """Test two pair hand evaluation"""
        cards = [
            StandardCard("2", "hearts"),
            StandardCard("2", "spades"),
            StandardCard("8", "diamonds"),
            StandardCard("8", "clubs"),
            StandardCard("A", "hearts")
        ]
        assert evaluate_hand(cards) == 3  # Two pair
    
    def test_evaluate_hand_three_of_a_kind(self):
        """Test three of a kind hand evaluation"""
        cards = [
            StandardCard("2", "hearts"),
            StandardCard("2", "spades"),
            StandardCard("2", "diamonds"),
            StandardCard("J", "clubs"),
            StandardCard("A", "hearts")
        ]
        assert evaluate_hand(cards) == 4  # Three of a kind
    
    def test_hand_name(self):
        """Test hand name conversion"""
        assert hand_name(1) == "High Card"
        assert hand_name(2) == "One Pair"
        assert hand_name(3) == "Two Pair"
        assert hand_name(4) == "Three of a Kind"
        assert hand_name(5) == "Straight"
        assert hand_name(6) == "Flush"
        assert hand_name(7) == "Full House"
        assert hand_name(8) == "Four of a Kind"
        assert hand_name(9) == "Straight Flush"
        assert hand_name(999) == "Unknown Hand"
    
    def test_hand_score_with_board(self):
        """Test hand scoring with board cards"""
        player_hand = [
            StandardCard("A", "hearts"),
            StandardCard("A", "spades")
        ]
        board = [
            StandardCard("K", "hearts"),
            StandardCard("Q", "hearts"),
            StandardCard("J", "hearts")
        ]
        # Should be three of a kind or better depending on full 5-card hand
        score = hand_score(player_hand, board)
        assert score >= 2  # At least one pair