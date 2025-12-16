import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from casino.games.slots.slots import get_rand_item, generate_payout_legend


class TestSlots:
    
    def test_get_rand_item(self):
        """Test random item generation"""
        items = set()
        for _ in range(100):
            items.add(get_rand_item())
        
        # Should only return A, B, C, D
        assert items == {"A", "B", "C", "D"}
    
    def test_generate_payout_legend(self):
        """Test payout legend generation"""
        low_items = ["A", "B", "C"]
        high_items = ["D"]
        legend = generate_payout_legend(low_items, high_items)
        
        assert "Matching A | B | C" in legend
        assert "Matching D" in legend
        assert "x1.5" in legend
        assert "x5.0" in legend