# import dbmodel as m
import csv
from math import log


# def load_mapping(session):
# 	"""
# 	This function will seed our db with the primary keys from our data sets into a MappingIDs table.
# 	This table will be used as a lookup when we are categorizing habits.
# 	Reference the MappingID function in dbmodel for more info.
# 	"""
# 	# this section loads data from the ATUS file, which has a consumer unit ID and a person ID
# 	with open('./data/atusresp_2013/atusresp_2013.dat','rb') as atus_file:
# 		reader = csv.reader(atus_file, delimiter = ',')
# 		for row in atus_file:
# 			primary_source_id = row[0] # this is the TUCASEID field
# 			secondary_source_id = row[1] #this is the TULINENO field
# 			mapping = m.MappingID(primary_source_id=primary_source_id, secondary_source_id=secondary_source_id)
# 			session.add(mapping)
# 		atus_file.close()
# 	# this section loads data from the CEX file, which has a CU id, but no ref person (RP) ID, so using RP age as secondary
# 	with open('./data/cex_interview_2013/fmli134.csv', 'rb') as cex_file:
# 		reader = csv.reader(cex_file, delimiter=',')
# 		for row in reader:
# 			primary_source_id = row[0] # this is NEWID field
# 			secondary_source_id = row[3] # this is the AGE_REF field
# 			mapping = m.MappingID(primary_source_id=primary_source_id, secondary_source_id=secondary_source_id)
# 			session.add(mapping)
# 		cex_file.close()
# 	session.commit()

def create_user_dict():
	"""
	This function loads the Archetypes table.  This requires some logic, since this table aggregates data from the raw files.
	It also updates the mapping table with the Archetype ID that matches the primary and secondary ID
	"""
	#first we need to pull the two data sources together in a dictionary
	#doing this to make sure the right ages from one data source get added to the right users from the other
	
	user_dict = {}
	print "user dict created"

	# this first ATUS file gets most of the demo data
	with open('./data/atuscps_2013/atuscps_2013.dat','rb') as atus_cps_file:
		reader_cps = csv.reader(atus_cps_file, )
		for row in reader_cps:
			idA1 = row[0]
			idA2 = row[1]
			sex = row[136]
			occupation = row[41]
			state = row[6]
			education = row[68]
			income = row[8]
			user_dict[(idA1, idA2)] = [sex, occupation, state, education, income]
	atus_cps_file.close()

	#this second ATUS file will get us age, and we need to convert that into an age range for the archetype
	#the value is then added at index 0 of the list that makes up the value of the user's key

	#*********** ^ this is what doesn't work! ^*******************************
	with open('./data/atusrost_2013/atusrost_2013.dat','rb') as atus_rost_file:
		reader_rost = csv.reader(atus_rost_file, delimiter = ',')
		firstline = True
		for row in reader_rost:
			if firstline:
				firstline = False
				continue
			idB1 = row[0]
			idB2 = row[1]
			age = row[2]
			if reader_cps.line_num == 1:
				continue
			try:
				age = int(age)
				if age < 20:
					age_range = 1
				elif age >= 20 and age < 30:
					age_range = 2
				elif age >= 30 and age < 40:
					age_range = 3
				elif age >= 40 and age < 50:
					age_range = 4
				elif age >= 50 and age < 60:
					age_range = 5
				elif age >=60 and age < 70:
					age_range = 6
				else:
					age_range = 7
				print age, age_range
			except:
				print "didn't work", row[0], row[1]

			if (idB1, idB2) in user_dict:
				user_dict[(idB1, idB2)].append(age_range)
	atus_rost_file.close()
	print user_dict
	return user_dict

# def group_keys(session):
# 	"""
# 	This function groups the keys in the dict with the same demo characteristics.
# 	"""
# 	create_user_dict(session)

# 	#this dictionary will flip the key value pairs, deduping the values to create the archetypes 
# 	#and grouping the ids

# 	archetype_dict = {}

# 	#FIXME could be shortened by using "get"
# 	for key, value in user_dict:
# 		if archetype_dict[value] not in archetype_dict:
# 			archetype_dict[value] = [key]
# 		else:
# 			archetype_dict[value].append(key)





def main():
    # You'll call each of the load_* functions with the session as an argument
    # load_mapping(session)
    create_user_dict()
if __name__ == "__main__":
    # go = m.session
    # main(go)
    main()