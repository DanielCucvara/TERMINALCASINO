import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from casino.cards import StandardCard, StandardDeck


class TestCardClasses:
    
    def test_standard_card_creation(self):
        """Test StandardCard creation"""
        card = StandardCard("A", "hearts")
        
        assert card.rank == "A"
        assert card.suit == "hearts"
        assert card.category == "hearts"
        assert card.identifier == "A"
        assert card.hidden == True
    
    def test_standard_deck_creation(self):
        """Test StandardDeck creation"""
        deck = StandardDeck(1)
        
        assert len(deck.cards) == 52  # 4 suits * 13 ranks
        assert all(isinstance(card, StandardCard) for card in deck.cards)
    
    def test_standard_deck_multiple_decks(self):
        """Test StandardDeck with multiple decks"""
        deck = StandardDeck(2)
        
        assert len(deck.cards) == 104  # 2 * 52 cards
    
    def test_standard_deck_draw(self):
        """Test drawing cards from deck"""
        deck = StandardDeck(1)
        initial_size = len(deck.cards)
        
        card = deck.draw()
        
        assert isinstance(card, StandardCard)
        assert len(deck.cards) == initial_size - 1
    
    def test_standard_deck_shuffle(self):
        """Test deck shuffling changes order"""
        deck1 = StandardDeck(1)
        deck2 = StandardDeck(1)
        
        # Get string representations of cards in order
        initial_order = [str(card.rank) + card.suit for card in deck1.cards]
        
        # Shuffle one deck
        deck1.shuffle()
        shuffled_order = [str(card.rank) + card.suit for card in deck1.cards]
        
        # The order should be different (very high probability)
        # If by chance they're the same, shuffle again
        if initial_order == shuffled_order:
            deck1.shuffle()
            shuffled_order = [str(card.rank) + card.suit for card in deck1.cards]
        
        assert initial_order != shuffled_order