from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def create_db_engine(database_url):
    # Используем переданный URL базы данных
    engine = create_engine(database_url)
    return engine

def create_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()
