# this run the game in 4 min interval and send it to redis pub/sub 


import json
from app.config.settings import Settings
from app.constants.constant_strings import ConstantStrnigs
from app.core.game_engine import GameEngine, generate_server_seed
import asyncio
import json
from redis.asyncio import Redis 

settings = Settings()

async def game_runner():
    print(f"url:{settings.REDIS_URL}")
    redis = await Redis.from_url(settings.REDIS_URL)
    pubsub=redis.pubsub()


    print("Game runner started")
    round_number=0
    game = GameEngine()
    server_seed_info = generate_server_seed()
    client_seed = game.generate_client_seed()

    num_rounds = 1_000_000
    multipliers = []

    while True:
        result = game.simulate_round(server_seed_info.seed, client_seed, round_number)
        round_number+=1
        multipliers.append(result['multiplier'])
        print(f"Multipler:{result['multiplier']}")
        # await redis.publish(
        #     ConstantStrnigs.MULTIPLIER_CHANNEL.value,
        #     json.dumps({
        #     ConstantStrnigs.MULTIPLIER.value:result['multiplier'],
        #     ConstantStrnigs.ROUND.value:round_number
        # })

        

        #   )

        subscriber_count=await redis.publish(
    ConstantStrnigs.MULTIPLIER_CHANNEL.value,
    json.dumps({
        ConstantStrnigs.MULTIPLIER.value:result['multiplier'],
        ConstantStrnigs.ROUND.value:round_number
    })
)           
        print(f"Published to {subscriber_count} subscribers")


        
        
        await asyncio.sleep(2)
        yield result['multiplier']
        # publish it to redis 


async def run_game():
    async for multiplier in game_runner():
        pass


if __name__ == "__main__":

    asyncio.run(run_game())

    # for round_number in range(1, num_rounds + 1):
    #     result = game.simulate_round(server_seed_info.seed, client_seed, round_number)
    #     multipliers.append(result['multiplier'])
        # print(f"Ml:{result['multiplier']}")

    # high = max(multipliers)
    # low = min(multipliers)
    # avg = sum(multipliers) / len(multipliers)

    # print(f"Simulated {num_rounds} rounds.")
    # print(f"Highest multiplier: {high}")
    # print(f"Lowest multiplier: {low}")
    # print(f"Average multiplier: {avg:.4f}")