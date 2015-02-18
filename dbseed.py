import dbmodel as m
import csv


def load_mapping(session):
	"""
	This function will seed our db with the primary keys from our data sets into a MappingIDs table.
	This table will be used as a lookup when we are categorizing habits.
	Reference the MappingID function in dbmodel for more info.
	"""
	# this section loads data from the ATUS file, which has a consumer unit ID and a person ID
	with open('./data/atusresp_2013/atusresp_2013.dat','rb') as atus_file:
		reader = csv.reader(atus_file, delimiter = ',')
		for row in atus_file:
			primary_source_id = row[0] # this is the TUCASEID field
			secondary_source_id = row[1] #this is the TULINENO field
			mapping = m.MappingID(primary_source_id=primary_source_id, secondary_source_id=secondary_source_id)
			session.add(mapping)
		atus_file.close()
	# this section loads data from the CEX file, which has a CU id, but no ref person (RP) ID, so using RP age as secondary
	with open('./data/cex_interview_2013/fmli134.csv', 'rb') as cex_file:
		reader = csv.reader(cex_file, delimiter=',')
		for row in reader:
			primary_source_id = row[0] # this is NEWID field
			secondary_source_id = row[3] # this is the AGE_REF field
			mapping = m.MappingID(primary_source_id=primary_source_id, secondary_source_id=secondary_source_id)
			session.add(mapping)
		cex_file.close()
	session.commit()

# def load_archetype(session):
# 	"""
# 	This function loads the Archetypes table.  This requires some logic, since this table aggregates data from the raw files.
# 	It also updates the mapping table with the Archetype ID that matches the primary and secondary ID
# 	"""
# 	with open('./data/atusrost_2013/atusrost_2013.dat','rb') as atus_file:
# 	#get an age range based on the age
# 	if age < 20:
# 		age_range = 1
# 	if age >= 20 and age < 30:
# 		age_range = 2
# 	if age >= 30 and age < 40:
# 		age_range = 3
# 	if age >= 40 and age < 50:
# 		age_range = 4
# 	if age >= 50 and age < 60:
# 		age_range = 5
# 	if age >=60 and age < 70:
# 		age_range ==6
# 	if age >= 70:
# 		age_range == 7

# # 	age = Column(Integer)
# # 	age_range = Column(Integer, nullable = True)
# # 	sex = Column(Integer)
# # 	occupation = Column(Integer)
# # 	state = Column(Integer)
# # 	education = Column(Integer)
# # 	income = Column(Integer)

def main(session):
    # You'll call each of the load_* functions with the session as an argument
    load_mapping(session)

if __name__ == "__main__":
    go = m.session
    main(go)