# simulation 001 assuming every player is smart choise between(1.2 -2 ) with cash cap 10 

import random
from app.core.game_engine import GameEngine, generate_server_seed
from app.core.simulations.constants import LOW_CAP, MID_HIGH, MID_LOW
from app.core.simulations.simulate_user_bet import simulate_user_bet

def simulation001():
    NUM_ROUNDS = 1050
    BET_MIN = 50
    BET_MAX = 1000
    CASHOUT_MIN =1.5
    CASHOUT_MAX = 3
    PLAYERS_MIN = 20
    PLAYERS_MAX = 400

    game = GameEngine()
    server_seed_info = generate_server_seed()
    client_seed = game.generate_client_seed()

    total_wagered = 0
    total_paid_out = 0

    for round_number in range(1, NUM_ROUNDS + 1):
        # Simulate the round's crash multiplier
        result = game.simulate_round(server_seed_info.seed, client_seed, round_number)
        crash_multiplier = result['multiplier']
        # print(f"result:{result['multiplier']}")

        # Random number of players this round
        num_players = random.randint(PLAYERS_MIN, PLAYERS_MAX)

        min_bet = 50
        max_bet = 1_000
        low_cap = 100
        mid_low = 100
        mid_high = 500
        p_low = 0.02     # 2% below $100
        p_mid = 0.88     # 88% between $100–$500
# 10% will be above $500

        
        

        for _ in range(num_players):
            # bet = random.uniform(BET_MIN, BET_MAX)
            bet=simulate_user_bet(BET_MIN,BET_MAX, LOW_CAP, MID_LOW, MID_HIGH, p_low=0.02, p_mid=0.88 )
            # print(f"bet:{bet}")
            
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
