from datetime import datetime ,timezone
import hashlib

def geneate_tikcet_code(casino_id:int,round_number:int,guessed_multiplier:int,timestamp:datetime):
    ticket=f"{round_number}-{casino_id}-{guessed_multiplier}-{timestamp}"
    ticket_code=hashlib.sha256(ticket.encode()).hexdigest()[:16]
    # print(f"code:{ticket_code}")
    print(f"code:{ticket_code}")
    return ticket_code





 