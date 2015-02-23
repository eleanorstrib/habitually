from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref


#db set-up, connection requiring explicit inclusion of adds and commits
engine = create_engine("sqlite:///habit.db", echo=True)
session = scoped_session(sessionmaker (bind=engine,
										autocommit=False,
										autoflush=False))

#establishing base to model tables on
Base = declarative_base()
Base.query = session.query_property()

class Time(Base):
	__tablename__ = "Time_habits"
	id = Column(Integer, primary_key = True)
	hhld_id = Column(Integer)
	person_id = Column(Integer)
	sex = Column(String)
	education = Column(String)
	age_range = Column(String)
	region = Column(String)
	income = Column(String)
	exercise_habit_timemin = Column(Integer)
	work_habit_timemin = Column(Integer)

	def __repr__(self):
		return "<id=%d sex=%s education=%s age_range=%s region=%s income=%s exercise_habit_timemin=%d work_habit_timemin=%d>"

class Money(Base):
	__tablename__ = "Money_habits"
	id = Column(Integer, primary_key = True)
	hhld_id = Column(Integer)
	person_id = Column(Integer)
	sex = Column(String)
	education = Column(String)
	age_range = Column(String)
	region = Column(String)
	income = Column(String)
	spending_habit_clothes_dollars = Column(Integer)
	spending_habit_eatout_dollars = Column(Integer)

	def __repr__(self):
		return "<id=%d sex=%s education=%s age_range=%s region=%s income=%s spending_habit_clothes_dollars=%d spending_habit_eat_out_dollars=%d>"




