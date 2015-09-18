from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, scoped_session


#db set-up, connection requiring explicit inclusion of adds and commits
# engine = create_engine("sqlite:///habit.db", echo=True)
engine = create_engine("/home/habitually/habitually/habit.db", echo=True)
session = scoped_session(sessionmaker (bind=engine,
										autocommit=False,
										autoflush=False))

#establishing base to model tables on
Base = declarative_base()
Base.query = session.query_property()

class Time(Base):
	__tablename__ = "Time_habits"
	id = Column(Integer, primary_key = True)
	hhld_id = Column(String)
	person_id = Column(String)
	sex = Column(Integer, nullable=False)
	education = Column(Integer, nullable=False)
	age_range = Column(Integer, nullable=False)
	region = Column(Integer, nullable=False)
	income = Column(Integer, nullable=False)
	exercise_habit_timemin = Column(Integer)
	work_habit_timemin = Column(Integer)
	sleep_habit_timemin = Column(Integer)

	# def __repr__(self):
	# 	return "<sex=%d education=%d age_range=%d region=%d income=%d exercise_habit_timemin=%d work_habit_timemin=%d sleep_habit_timemin=%d>" % (self.id, self.sex, self.education, self.age_range, self.region, self.income, self.exercise_habit_timemin, self.work_habit_timemin, self.sleep_habit_timemin)

class Money(Base):
	__tablename__ = "Money_habits"
	id = Column(Integer, primary_key = True)
	hhld_id = Column(String)
	person_id = Column(String)
	sex = Column(Integer, nullable=False)
	education = Column(Integer, nullable=False)
	age_range = Column(Integer, nullable=False)
	region = Column(Integer, nullable=False)
	income = Column(Integer, nullable=False)
	spending_habit_clothes_dollars = Column(Integer)
	spending_habit_eatout_dollars = Column(Integer)

	# def __repr__(self):
	# 	return "<sex=%d education=%d age_range=%d region=%d income=%d spending_habit_clothes_dollars=%d spending_habit_eat_out_dollars=%d>" % (self.id, self.sex, self.education, self.age_range, self.region, self.income, self.spending_habit_clothes_dollars, self.spending_habit_eatout_dollars)




