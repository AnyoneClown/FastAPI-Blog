from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID

from backend.app.models.base import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    pass
