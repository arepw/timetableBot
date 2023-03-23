from os import getcwd
import datetime
from sqlalchemy import create_engine, Integer, DateTime, Column, SmallInteger, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists


db_url = f'sqlite:///{getcwd()}/db.sqlite'
engine = create_engine(db_url)

Base = declarative_base()
session = Session(bind=engine)
# Vladivostok time delta
time_delta = datetime.timedelta(hours=10, minutes=0)


class Entry(Base):
    __tablename__ = 'last_entry'
    id = Column(SmallInteger, primary_key=True)

    @staticmethod
    def current_time():
        time = datetime.datetime.now(datetime.timezone.utc) + time_delta
        # cut out microseconds
        return time.replace(microsecond=0)

    time = Column(DateTime(), default=current_time())

    # Update entry time on schedule update
    def update_time(self):
        self.time = self.current_time()
        session.commit()


if not database_exists(db_url):
    Base.metadata.create_all(engine)
    default_entry = Entry(id=1)
    session.add(default_entry)
    session.commit()
