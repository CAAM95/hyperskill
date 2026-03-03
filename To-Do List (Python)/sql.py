from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, Date, create_engine
from datetime import datetime

Base = declarative_base()

engine = create_engine("sqlite:///todo.db", echo=False)
SessionLocal = sessionmaker(bind=engine)


class Table(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True)
    task = Column(String, default="default_value")
    deadline = Column(Date, default=datetime.today)

    def __repr__(self):
        return f"{self.id}, {self.task}, {self.deadline}"


def init_db():
    Base.metadata.create_all(engine)


def get_session():
    return SessionLocal()