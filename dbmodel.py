from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import sessionmaker, scoped_session, relationship, backref


#db set-up, connection requiring explicit inclusion of adds and commits
engine = create_engine("sqlite:///habitually.db", echo=True)
session = scoped_session(sessionmaker (bind=engine,
										autocommit=False,
										autoflush=False))

#establishing base to model tables on
Base = declarative_base()
Base.query = session.query_property()

#table definition
class Archetype(Base):
	__tablename__ = "Archetypes"
	id = Column(Integer, primary_key = True)
	#the next two fields in caps are identifiers in the original ATUS dataset
	age = Column(Integer(3))
	age_range = Column(Integer(2), nullable = True)
	sex = Column(Integer(1))
	occupation = Column(Integer(2))
	state = Column(Integer(2))
	education = Column(Integer(2))
	income = Column(Integer(2))

	def __repr__(self):
		return "<id=%d age=%d age_range=%d sex=%d occupation=%d state=%s education=%d income=%d>"

class MappingID(Base):
	__tablename__ = "MappingIDs"
	id = Column(Integer, primary_key = True)
	primary_source_id = (Integer(20), nullable=False)
	secondary_source_id = (Integer(2), nullable=False)
	archetype_id = Column(Integer(ForeignKey('Archetypes.id')))

	def __repr__(self):
		return "<id=%d primary_source_id=%s secondary_source_id=%s archetype_id=%d>"

	archetype = relationship("Archetype",
				backref=backref("Archetypes", order_by=id))


# 	spending = relationship("Spending_habits",
# 				backref=backref("Archetypes", order_by=id))

# class Spending(Base):
# 	__tablename__ = "Spending_habits"
# 	id = Column(Integer, primary_key = True)
# 	name = Column(String(50))
# 	description = Column(String(150))
# 	archetype_id = Column(Integer, ForeignKey('Archetypes.id'))
# 	clothing_purchserv = Column(Integer(16), nullable = True)
# 	food_out_purch = Column(Integer(16), nullable = True)
# 	alcohol_out_purch = Column(Integer(16), nullable = True)
# 	cigarette_purch = Column(Integer(16), nullable = True)
# 	gasoline_purch = Column(Integer(8), nullable = True)

# 	def __repr__(self):
# 		return "<id=%d description=%s archetype_id=%d clothing_purchserv=%d food_out_purch=%d alcohol_out_purch=%d cigarette_purch=%d gasoline_purch=%d>"

# 	archetype = relationship("Archetypes", 
# 				backref=backref("Spending_habits", order_by=id))