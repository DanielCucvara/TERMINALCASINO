import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from casino.games.roulette.roulette import Roulette, STANDARD_AMERICAN_ROULETTE_WHEEL

import unittest
from unittest.mock import patch

from casino.games.roulette.roulette import AmericanRoulette

class FakeAccount:
    def __init__(self, balance=100):
        self.balance = balance
        self.aid = id(self)

    def withdraw(self, amount):
        self.balance -= amount

    def deposit(self, amount):
        self.balance += amount


class TestRouletteWithMock(unittest.TestCase):

    @patch("casino.games.roulette.roulette.random.randint")
    def test_spin_wheel_with_mocked_random(self, mock_randint):

        # mock: random.randint vždy vráti index 0
        mock_randint.return_value = 0

        accounts = [FakeAccount()]
        roulette = AmericanRoulette(accounts)

        result = roulette.spin_wheel()

        # očakávame prvý prvok na kolese
        self.assertEqual(result, roulette.wheel[0])



class TestRoulette:
    
    def test_normalize_color(self):
        """Test color normalization"""
        assert Roulette.normalize_color("r") == "red"
        assert Roulette.normalize_color("red") == "red"
        assert Roulette.normalize_color("g") == "green"
        assert Roulette.normalize_color("green") == "green"
        assert Roulette.normalize_color("b") == "black"
        assert Roulette.normalize_color("black") == "black"
    
    def test_normalize_type(self):
        """Test bet type normalization"""
        assert Roulette.normalize_type("c") == "color"
        assert Roulette.normalize_type("color") == "color"
        assert Roulette.normalize_type("n") == "number"
        assert Roulette.normalize_type("number") == "number"
    
    def test_roulette_sort_key(self):
        """Test roulette number sorting"""
        assert Roulette.roulette_sort_key("0") == -1
        assert Roulette.roulette_sort_key("00") == 0
        assert Roulette.roulette_sort_key("5") == 5
        assert Roulette.roulette_sort_key("36") == 36
    
    def test_wheel_constants(self):
        """Test that the wheel constants are correct"""
        assert len(STANDARD_AMERICAN_ROULETTE_WHEEL) > 0
        # Check that it contains expected values
        numbers = [item[0] for item in STANDARD_AMERICAN_ROULETTE_WHEEL]
        colors = [item[1] for item in STANDARD_AMERICAN_ROULETTE_WHEEL]
        
        assert "0" in numbers
        assert "00" in numbers
        assert "red" in colors
        assert "black" in colors
        assert "green" in colors