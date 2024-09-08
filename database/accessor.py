from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql+psycopg2://my_admin:my_password@localhost:5430/my_db")

Session = sessionmaker(engine)

def get_db_session() -> Session:
    return Session