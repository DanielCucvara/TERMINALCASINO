import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import Mock, patch
from casino.games.blackjack.blackjack import hand_total, deal_card
from casino.cards import StandardCard, StandardDeck


class TestBlackjack:
    
    def test_hand_total_basic(self):
        """Test basic hand total calculation"""
        hand = [
            StandardCard("5", "hearts"),
            StandardCard("10", "spades")
        ]
        assert hand_total(hand) == 15
    
    def test_hand_total_with_aces(self):
        """Test hand total with aces"""
        # Ace as 11
        hand1 = [
            StandardCard("A", "hearts"),
            StandardCard("7", "spades")
        ]
        assert hand_total(hand1) == 18
        
        # Ace as 1 (bust prevention)
        hand2 = [
            StandardCard("A", "hearts"),
            StandardCard("10", "spades"),
            StandardCard("5", "diamonds")
        ]
        assert hand_total(hand2) == 16
    
    def test_hand_total_face_cards(self):
        """Test hand total with face cards"""
        hand = [
            StandardCard("K", "hearts"),
            StandardCard("Q", "spades")
        ]
        assert hand_total(hand) == 20
    
    def test_hand_total_blackjack(self):
        """Test blackjack detection"""
        hand = [
            StandardCard("A", "hearts"),
            StandardCard("K", "spades")
        ]
        assert hand_total(hand) == 21
    
    def test_deal_card(self):
        """Test dealing cards from deck"""
        deck = StandardDeck(1)
        initial_size = len(deck.cards)
        hand = []
        
        deal_card(hand, deck)
        
        assert len(hand) == 1
        assert len(deck.cards) == initial_size - 1
        assert isinstance(hand[0], StandardCard)
    
    def test_hand_total_edge_cases(self):
        """Test edge cases for hand total calculation"""
        # Multiple aces
        hand = [
            StandardCard("A", "hearts"),
            StandardCard("A", "spades"),
            StandardCard("5", "diamonds")
        ]
        assert hand_total(hand) == 17  # A=11, A=1, 5