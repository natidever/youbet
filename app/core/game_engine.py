# generating the server seed
# class SeedInfo()
import math
import secrets
import uuid
from pydantic import BaseModel,Field
from datetime import datetime,timezone
import hashlib

class ServerSeedInfo(BaseModel):
    uuid: str = Field(..., description="Unique identifier for the server seed")
    seed: str = Field(..., description="The secure server seed")
    created_at:datetime = Field(
        default_factory=lambda:datetime.now(timezone.utc),
        description="Timestamp when the record was created (UTC)"

    )
    commitment_hash: str = Field(..., description="SHA256 hash of the server seed for commitment")



def generate_server_seed()->ServerSeedInfo:
    seed_id=str(uuid.uuid4())
    seed = secrets.token_hex(32)
    commitment=hashlib.sha256(seed.encode()).hexdigest()
    
    server_info=ServerSeedInfo(
        uuid=seed_id,
        seed=seed,
        commitment_hash=commitment
    )
    # print(server_info.model_dump_json)
    return server_info

    

  
class GameEngine:
    def __init__(self,houseedge:float=0.03):
        self.houseedge=houseedge

    def generate_client_seed(self) -> str:
        return "mock-client-seed"
    def get_nonce(self, round_number: int) -> int:
        return round_number
    
    def generate_game_hash(self,server_seed:str,client_seed:str,round_nounce:str)->str:
        combined = f"{server_seed}-{client_seed}-{round_nounce}"
        # print(f"combined:{combined}")
        game_hash=hashlib.sha256(combined.encode()).hexdigest()
        return game_hash
    

    def generate_multiplier(self,game_hash:str)->float:
        if int(game_hash,16) %33 ==0 :
            return 1.00
        
        h=int(game_hash[:13],16)  #this will result 4*13=52 thinking 1 hexa symbol mean 4 byte
        X = h / float(2**52)
        # e=2**52
        

        # multiplier = (100 * e - h) / (e - h)
        multiplier = math.floor((1 / (1 - X)) * 100) / 100.0
        # multiplier *= (1 - self.houseedge)  
        # raw =math.floor(multiplier * 100) / 100.0 
        if multiplier > 10:
            multiplier = 10
        
        
        return multiplier


        return 

    def simulate_round(self, server_seed: str, client_seed: str, round_number: int):
        nonce = self.get_nonce(round_number)
        hash_val = self.generate_game_hash(server_seed, client_seed, nonce)
        multiplier = self.generate_multiplier(hash_val)
        
        return {
            "round": round_number,
            "hash": hash_val[:16] + "...",
            "multiplier": multiplier
        }
    





if __name__ == "__main__":
    game = GameEngine()
    server_seed_info = generate_server_seed()
    client_seed = game.generate_client_seed()

    num_rounds = 1_000_000
    multipliers = []

    for round_number in range(1, num_rounds + 1):
        result = game.simulate_round(server_seed_info.seed, client_seed, round_number)
        multipliers.append(result['multiplier'])
        # print(f"Ml:{result['multiplier']}")

    high = max(multipliers)
    low = min(multipliers)
    avg = sum(multipliers) / len(multipliers)

    print(f"Simulated {num_rounds} rounds.")
    print(f"Highest multiplier: {high}")
    print(f"Lowest multiplier: {low}")
    print(f"Average multiplier: {avg:.4f}")
   

    
  