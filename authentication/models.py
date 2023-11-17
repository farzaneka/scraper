from sqlalchemy import Column, Integer, String

from authentication.database import Base


class Member(Base):
    __tablename__ = 'member'

    id = Column(Integer, index=True, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)

