from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref


#db set-up, connection requiring explicit inclusion of adds and commits
engine = create_engine("sqlite:///habitually.db", echo=True)
session = scoped_session(sessionmaker (bind=engine,
										autocommit=False,
										autoflush=False))

#establishing base to model tables on
Base = declarative_base()
Base.query = session.query_property()


class Archetype(Base):
	__tablename__ = "Archetypes"
	id = Column(Integer, primary_key = True)
	sex = Column(String)
	education = Column(String)
	age_range = Column(String)
	region = Column(String)
	income = Column(String)
  	value_id = Column(String, nullable = False)

	def __repr__(self):
		return "<id=%d age_range=%d sex=%d occupation=%d state=%s education=%d income=%d>"

class MappingID(Base):
	__tablename__ = "MappingIDs"
	id = Column(Integer, primary_key=True)
	subject_id = Column(String, nullable=False)
	value_id = Column(String, nullable=False)

	def __repr__(self):
		return "<id=%d primary_source_id=%d secondary_source_id=%d>"

class Sleeping(Base):
	__tablename__ = "Sleeping_habit"
	id = Column(Integer, primary_key = True)
	sex = Column(String)
	education = Column(String)
	age_range = Column(String)
	min_minutes = Column(Integer)
	max_minutes = Column(Integer)
	avg_minutes = Column(Integer)
	value_id_h = Column(String, nullable=False)

	def __repr__(self):
		return "<id=%d sex=%s education=%s age_range=%s min_minutes=%d max_minutes=%d avg_minutes=%d>"


class Exercising(Base):
	__tablename__ = "Exercising_habit"
	id = Column(Integer, primary_key = True)
	sex = Column(String)
	education = Column(String)
	age_range = Column(String)
	min_minutes = Column(Integer)
	max_minutes = Column(Integer)
	avg_minutes = Column(Integer)
	value_id_h = Column(String, nullable=False)

	def __repr__(self):
		return "<id=%d sex=%s education=%s age_range=%s min_minutes=%d max_minutes=%d avg_minutes=%d>"


class Working(Base):
	__tablename__ = "Working_habit"
	id = Column(Integer, primary_key = True)
	sex = Column(String)
	education = Column(String)
	age_range = Column(String)
	min_minutes = Column(Integer)
	max_minutes = Column(Integer)
	avg_minutes = Column(Integer)
	value_id_h = Column(String, nullable=False)

	def __repr__(self):
		return "<id=%d sex=%s education=%s age_range=%s min_minutes=%d max_minutes=%d avg_minutes=%d>"


class Spending_Clothes(Base):
	__tablename__ = "Spending_habit_clothing"
	id = Column(Integer, primary_key = True)
	sex = Column(String)
	education = Column(String)
	age_range = Column(String)
	region = Column(String)
	income= Column(String)
	min_spending = Column(Integer)
	max_spending = Column(Integer)
	avg_spending = Column(Integer)
	value_id = Column(String, nullable=False)

	def __repr__(self):
		return "<id=%d sex=%s education=%s age_range=%s min_minutes=%d max_minutes=%d avg_minutes=%d>"

