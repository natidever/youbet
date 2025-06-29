from contextlib import contextmanager
import os

from sqlmodel import create_engine, SQLModel, Session

# DATABASE_URL = os.environ.get("")
DATABASE_URL = "postgresql://user:password@postgres:5432/mydb"
engine = create_engine(DATABASE_URL, echo=True)



def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


# @contextmanager
# def get_session_sync():
#     with Session(engine) as session:
#         try:
#             yield session
#         except Exception:
#             session.rollback()
#             raise
#         finally:
#             session.close()


@contextmanager
def get_session_sync():
    with Session(engine) as session:
        try:
            yield session
            # 🔍 check session status after yield
           
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

# def get_session_sync() -> Session:
#     return Session(engine)

