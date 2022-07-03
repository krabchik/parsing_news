from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_NAME = 'NEWS_DB.sqlite'

engine = create_engine(f'sqlite:///{DATABASE_NAME}')
Session = sessionmaker(bind=engine)
Session.configure(bind=engine)

Base = declarative_base()


def create_db():
    Base.metadata.create_all(engine)
