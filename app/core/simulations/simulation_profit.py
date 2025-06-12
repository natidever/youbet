# simulation 001 assuming every player is smart choise between(1.2 -2 ) with cash cap 10 

import random
from app.core.game_engine import GameEngine, generate_server_seed

def simulation001():
    NUM_ROUNDS = 50
    BET_MIN = 10
    BET_MAX = 10
    CASHOUT_MIN =2
    CASHOUT_MAX = 2
    PLAYERS_MIN = 5
    PLAYERS_MAX = 5

    game = GameEngine()
    server_seed_info = generate_server_seed()
    client_seed = game.generate_client_seed()

    total_wagered = 0
    total_paid_out = 0

    for round_number in range(1, NUM_ROUNDS + 1):
        # Simulate the round's crash multiplier
        result = game.simulate_round(server_seed_info.seed, client_seed, round_number)
        crash_multiplier = result['multiplier']
        print(f"result:{result['multiplier']}")

        # Random number of players this round
        num_players = random.randint(PLAYERS_MIN, PLAYERS_MAX)

        for _ in range(num_players):
            bet = random.uniform(BET_MIN, BET_MAX)
            cashout = random.uniform(CASHOUT_MIN, CASHOUT_MAX)

            total_wagered += bet

            if crash_multiplier >= cashout:
                # Player wins: receives bet * cashout (total), so profit is bet * (cashout - 1)
                payout = bet * cashout
            else:
                # Player loses: receives nothing
                payout = 0

            total_paid_out += payout

    house_profit = total_wagered - total_paid_out
    profit_percent = (house_profit / total_wagered) * 100 if total_wagered > 0 else 0

    print(f"Simulated {NUM_ROUNDS:,} rounds.")
    print(f"Total wagered: ${total_wagered:,.2f}")
    print(f"Total paid out: ${total_paid_out:,.2f}")
    print(f"House profit: ${house_profit:,.2f}")
    print(f"House profit percentage: {profit_percent:.4f}%")


simulation001()
