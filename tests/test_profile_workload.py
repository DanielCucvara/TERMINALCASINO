import unittest
from casino.cards import StandardDeck
from casino.games.poker.poker import hand_score
from casino.cards import StandardCard

class TestProfileWorkload(unittest.TestCase):
    def test_profile_workload(self):
        # 1) veľa deckov -> load_art disk I/O
        for _ in range(30):
            StandardDeck(num_decks=6)

        # 2) poker eval opakovane -> combinations bottleneck
        hand = [StandardCard("A", "hearts"), StandardCard("K", "hearts")]
        board = [
            StandardCard("Q", "hearts"),
            StandardCard("J", "hearts"),
            StandardCard("10", "hearts"),
            StandardCard("2", "clubs"),
            StandardCard("3", "spades"),
        ]
        for _ in range(2000):
            hand_score(hand, board)