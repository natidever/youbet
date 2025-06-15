import random

def simulate_user_bet(min_bet, max_bet, low_cap, mid_low, mid_high, p_low=0.02, p_mid=0.88):
    """
    Generate a bet in [min_bet, max_bet] with three controlled zones:
    - p_low: percentage of values under mid_low (e.g., < $100)
    - p_mid: percentage of values between [mid_low, mid_high] (e.g., $100–$500)
    - remainder goes above mid_high
    """
    assert 0 <= p_low + p_mid <= 1.0, "Invalid probabilities"

    r = random.random()
    if r < p_low:
        return random.randint(min_bet, mid_low - 1)
    elif r < p_low + p_mid:
        return random.randint(mid_low, mid_high)
    else:
        return random.randint(mid_high + 1, max_bet)

# Configurable values
min_bet = 20
max_bet = 10_000
low_cap = 100
mid_low = 100
mid_high = 500
p_low = 0.02     # 2% below $100
p_mid = 0.88     # 88% between $100–$500
# 10% will be above $500

# Generate samples
N = 10_000
results = [simulate_user_bet(min_bet, max_bet, low_cap, mid_low, mid_high, p_low, p_mid) for _ in range(N)]

# Count
under_100 = sum(x < 100 for x in results)
within_100_500 = sum(100 <= x <= 500 for x in results)
above_500 = sum(x > 500 for x in results)

print(f"Under $100: {under_100}")
print(f"$100–$500: {within_100_500}")
print(f"Above $500: {above_500}")
