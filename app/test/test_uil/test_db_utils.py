
from app.models.core_models import User
from app.util.db_utils import get_db_record_or_404



def test_get_db_record_or_404(session):
    user=User(name="Test User",
              username="test_name",
              password_hash="testp",
              role="agent",
              email="test@gma.com")
    session.add(user)
    session.commit()
    session.refresh(user)

    user= get_db_record_or_404(
        session=session,
        finder="test_name",
        table=User,
        field="username",
        error_message="User not found"
    )
    assert user.username == "test_name"

    pass


   