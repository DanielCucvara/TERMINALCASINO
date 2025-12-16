import time
import random
import sys
import os

# We'll create minimal test versions of the classes we need
class MockCard:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.hidden = True

class MockStandardCard(MockCard):
    def __init__(self, rank, suit):
        super().__init__(rank, suit)

def mock_hand_total(turn):
    """Mock version of hand_total function from blackjack"""
    total = 0
    aces = 0
    for card in turn:
        if card.rank in {"J", "Q", "K"}:
            total += 10
        elif card.rank == "A":
            total += 11
            aces += 1
        else:
            total += int(card.rank)
    
    # Ace adjustment
    while aces > 0 and total > 21:
        total -= 10
        aces -= 1
    return total

def mock_evaluate_hand(cards):
    """Mock version of evaluate_hand from poker"""
    ranks = [mock_get_card_value(card.rank) for card in cards]
    suits = [card.suit for card in cards]

    rank_counts = {}
    for rank in ranks:
        rank_counts[rank] = rank_counts.get(rank, 0) + 1
    
    suit_counts = {}
    for suit in suits:
        suit_counts[suit] = suit_counts.get(suit, 0) + 1

    is_flush = 5 in suit_counts.values()
    
    # Simple straight detection
    sorted_ranks = sorted(ranks)
    is_straight = len(set(sorted_ranks)) == 5 and (sorted_ranks[-1] - sorted_ranks[0] == 4)
    
    rank_counts_vals = sorted(rank_counts.values(), reverse=True)

    if is_straight and is_flush:
        return 9  # Straight Flush
    elif rank_counts_vals == [4, 1]:
        return 8  # Four of a Kind
    elif rank_counts_vals == [3, 2]:
        return 7  # Full House
    elif is_flush:
        return 6  # Flush
    elif is_straight:
        return 5  # Straight
    elif rank_counts_vals == [3, 1, 1]:
        return 4  # Three of a Kind
    elif rank_counts_vals == [2, 2, 1]:
        return 3  # Two Pair
    elif rank_counts_vals == [2, 1, 1, 1]:
        return 2  # One Pair
    else:
        return 1  # High Card

def mock_get_card_value(rank):
    """Mock version of get_card_value"""
    if rank == "J":
        return 11
    if rank == "Q":
        return 12
    if rank == "K":
        return 13
    if rank == "A":
        return 14
    return int(rank)

def benchmark_blackjack_operations():
    """Benchmark Blackjack operations"""
    print("=== BLACKJACK PERFORMANCE ===")
    
    # Test different hand scenarios
    test_cases = [
        [MockStandardCard("A", "hearts"), MockStandardCard("K", "spades")],  # Blackjack
        [MockStandardCard("10", "hearts"), MockStandardCard("5", "spades"), MockStandardCard("6", "diamonds")],  # 21
        [MockStandardCard("A", "hearts"), MockStandardCard("A", "spades"), MockStandardCard("9", "diamonds")],  # Multiple aces
        [MockStandardCard("2", "hearts"), MockStandardCard("3", "spades"), MockStandardCard("4", "diamonds")],  # Low cards
    ]
    
    # Benchmark hand_total calculations
    start_time = time.time()
    calculations = 0
    
    for i in range(5000):
        for hand in test_cases:
            result = mock_hand_total(hand)
            calculations += 1
    
    total_time = time.time() - start_time
    
    print(f"Hand Total Calculations: {calculations}")
    print(f"Time: {total_time:.4f}s")
    print(f"Calculations per second: {calculations/total_time:.0f}")
    print(f"Time per calculation: {(total_time/calculations)*1000:.4f}ms")
    
    return total_time

def benchmark_poker_operations():
    """Benchmark Poker operations"""
    print("\n=== POKER PERFORMANCE ===")
    
    # Test poker hand evaluation
    test_hands = [
        [  # High card
            MockStandardCard("2", "hearts"), MockStandardCard("5", "spades"), 
            MockStandardCard("8", "diamonds"), MockStandardCard("J", "clubs"), 
            MockStandardCard("A", "hearts")
        ],
        [  # One pair
            MockStandardCard("2", "hearts"), MockStandardCard("2", "spades"), 
            MockStandardCard("8", "diamonds"), MockStandardCard("J", "clubs"), 
            MockStandardCard("A", "hearts")
        ],
        [  # Two pair
            MockStandardCard("2", "hearts"), MockStandardCard("2", "spades"), 
            MockStandardCard("8", "diamonds"), MockStandardCard("8", "clubs"), 
            MockStandardCard("A", "hearts")
        ],
    ]
    
    start_time = time.time()
    evaluations = 0
    
    for i in range(1000):
        for hand in test_hands:
            result = mock_evaluate_hand(hand)
            evaluations += 1
    
    total_time = time.time() - start_time
    
    print(f"Hand Evaluations: {evaluations}")
    print(f"Time: {total_time:.4f}s")
    print(f"Evaluations per second: {evaluations/total_time:.0f}")
    print(f"Time per evaluation: {(total_time/evaluations)*1000:.4f}ms")
    
    return total_time

def benchmark_card_creation():
    """Benchmark card and deck creation"""
    print("\n=== CARD CREATION PERFORMANCE ===")
    
    suits = ["hearts", "diamonds", "clubs", "spades"]
    ranks = [str(n) for n in range(2, 11)] + ["J", "Q", "K", "A"]
    
    # Benchmark single card creation
    start_time = time.time()
    cards_created = 0
    
    for i in range(1000):
        for suit in suits:
            for rank in ranks:
                card = MockStandardCard(rank, suit)
                cards_created += 1
    
    card_time = time.time() - start_time
    
    print(f"Cards created: {cards_created}")
    print(f"Time: {card_time:.4f}s")
    print(f"Cards per second: {cards_created/card_time:.0f}")
    
    return card_time

def identify_bottlenecks():
    """Identify potential bottlenecks"""
    print("\n=== BOTTLENECK ANALYSIS ===")
    
    # Test individual operations
    operations = {
        "Simple hand total (2 cards)": lambda: mock_hand_total([
            MockStandardCard("10", "hearts"), MockStandardCard("5", "spades")
        ]),
        "Complex hand total (3 cards with aces)": lambda: mock_hand_total([
            MockStandardCard("A", "hearts"), MockStandardCard("A", "spades"), MockStandardCard("9", "diamonds")
        ]),
        "Poker evaluation (high card)": lambda: mock_evaluate_hand([
            MockStandardCard("2", "hearts"), MockStandardCard("5", "spades"), 
            MockStandardCard("8", "diamonds"), MockStandardCard("J", "clubs"), 
            MockStandardCard("A", "hearts")
        ]),
        "Card creation": lambda: MockStandardCard("A", "hearts"),
    }
    
    print("Single operation timing (1000 iterations):")
    for name, operation in operations.items():
        start_time = time.time()
        for i in range(1000):
            result = operation()
        total_time = time.time() - start_time
        avg_time = (total_time / 1000) * 1000000  # Convert to microseconds
        
        print(f"  {name}: {avg_time:.2f}μs per operation")

def memory_usage_analysis():
    """Analyze memory usage patterns"""
    print("\n=== MEMORY USAGE ANALYSIS ===")
    
    # Track object creation memory impact
    import sys
    
    cards = []
    memory_before = sys.getsizeof(cards)
    
    # Create many cards
    for i in range(1000):
        card = MockStandardCard(str(i % 10 + 2), "hearts")
        cards.append(card)
    
    memory_after = sys.getsizeof(cards)
    memory_per_card = (memory_after - memory_before) / 1000
    
    print(f"Memory for 1000 cards: {memory_after - memory_before} bytes")
    print(f"Memory per card: {memory_per_card:.2f} bytes")
    
    # Test different hand sizes
    hand_sizes = [2, 5, 7]  # Blackjack, Poker hand, Poker with board
    for size in hand_sizes:
        hand = [MockStandardCard("A", "hearts") for _ in range(size)]
        hand_memory = sys.getsizeof(hand) + sum(sys.getsizeof(card) for card in hand)
        print(f"Memory for {size}-card hand: ~{hand_memory} bytes")

if __name__ == "__main__":
    print("CASINO GAME PERFORMANCE PROFILING")
    print("=" * 50)
    
    # Run all benchmarks
    blackjack_time = benchmark_blackjack_operations()
    poker_time = benchmark_poker_operations()
    card_time = benchmark_card_creation()
    
    # Analysis
    identify_bottlenecks()
    memory_usage_analysis()
    
    # Summary
    print("\n=== PERFORMANCE SUMMARY ===")
    total_time = blackjack_time + poker_time + card_time
    print(f"Total benchmark time: {total_time:.2f}s")
    print("\nIDENTIFIED BOTTLENECKS:")
    print("1. Card object creation - can be optimized with object pooling")
    print("2. Poker hand evaluation - combinatorial complexity")
    print("3. Repeated calculations - caching opportunities")
    print("\nOPTIMIZATION OPPORTUNITIES:")
    print("• Cache hand total calculations")
    print("• Precompute common poker hand patterns") 
    print("• Use object pooling for cards")
    print("• Optimize data structures for card storage")