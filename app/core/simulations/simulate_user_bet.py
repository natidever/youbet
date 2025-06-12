import random

min_bet=20,
max_bet=10_000,

def beta_skewed(min_val=min_bet, max_val=max_bet ,a=0.2, b=5):
    r = random.betavariate(a, b)
    # print(r)
    return int(min_val + r * (max_val - min_val))



# Counters
low_count = 0
high_count = 0

# Generate many samples
N = 10  # number of samples

for _ in range(N):
    num = beta_skewed()
    if 100 <= num <= 500:
        low_count += 1
    else:
        high_count += 1

print(f"Out of {N} numbers:")
print(f" - Between 100 and 500: {low_count}")
print(f" - Between 501 and 10,000: {high_count}")
