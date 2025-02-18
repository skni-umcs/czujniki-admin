from sqlalchemy.orm import Session
from src.user.models import DBUser

def get_or_create_user(session: Session, keycloak_id: str, login: str):
    user = session.query(DBUser).filter(DBUser.keycloak_id == keycloak_id).first()
    if user is None:
        user = DBUser(keycloak_id=keycloak_id, login=login)
        session.add(user)
        session.commit()
    return user