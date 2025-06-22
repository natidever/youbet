from sqlmodel import Session, select
from typing import Type, TypeVar, Any
from fastapi import HTTPException
T = TypeVar('T')

def get_db_record_or_404(
    session: Session, 
    finder: Any, 
    table: Type[T], 
    field: str,
    error_message:str
) -> T | None:

    db_record = session.exec(
        select(table).where(getattr(table, field) == finder)
    ).first()
    if not db_record:
       raise HTTPException(status_code=404,detail=error_message)

    return db_record



def get_db_record(
    session: Session, 
    finder: Any, 
    table: Type[T], 
    field: str,
) -> T | None:

    db_record = session.exec(
        select(table).where(getattr(table, field) == finder)
    ).first()
    if not db_record:
       return None

    return db_record


def create_db_record(session:Session,table_instance :Type[T]):
    try:
        session.add(table_instance)
        session.commit()
        session.refresh(table_instance)
        return table_instance
    except Exception as e :
            raise HTTPException(
                status_code=500,
                detail=f"Failed to create record: {str(e)}"
            )
