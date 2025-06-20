from sqlmodel import Session, select

from app.core.schemas import RoundCreate
from app.models.core_models import Round

from app.config.logger import logger


def create_round(session:Session,round:RoundCreate):
    try:

        db_round = Round(
            round_number=round.round_number,
            server_seed=round.server_seed,
            commitment_hash=round.commitment_hash
        )
        existing_round = session.exec(
            select(Round).where(Round.round_number == round.round_number)
        ).first()
        """
TODO :CHECK THE ROUND IN PROD AND CHANGE 
THE IMPLEMETNATION OF THE ROUND TOO TO START
 FROM WHERE IT WAS EXACTLY 


        """
        # if existing_round:
        #     error_msg = f"Round number {round.round_number} already exists"
        #     logger.warning(error_msg)
        #     return None
        session.add(db_round)
        session.commit()
        session.refresh(db_round)
        return db_round

    except Exception as e:
        session.rollback()
        error_msg = f"Error creating round: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return None
    





def update_file_value(filename, variable_name, new_value):
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    with open(filename, 'w') as file:
        for line in lines:
            if line.startswith(variable_name + '='):
                line = f"{variable_name}={new_value}\n"
            file.write(line)



def read_file_value(filename, variable_name):
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith(variable_name + '='):
                return line.split('=')[1].strip()
    return None