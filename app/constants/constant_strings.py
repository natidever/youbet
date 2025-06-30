from enum import Enum

class ConstantStrnigs(str,Enum):
    MULTIPLIER_CHANNEL="multiplier_channel"
    ROUND="round"
    MULTIPLIER="multiplier"



class RoundState(str,Enum):
    PENDING='pending',
    RUNNING="running",
    DONE="done"


class RedisKeys(str,Enum):
    CURRENT_ROUND="current_round"
    CURRENT_ROUND_NUMBER="current_round_number"



class RedisRoundNumberGeneratorCircuitState(Enum):
    CLOSED = 1
    OPEN = 2
    HALF_OPEN = 3