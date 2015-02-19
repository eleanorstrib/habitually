# import dbmodel as m
import csv
from math import log


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
			age = row[187]
			if reader_cps.line_num == 1:
				continue
			try:
				age = int(age)
				if age < 20:
					age_range = '1'
				elif age >= 20 and age < 30:
					age_range = '2'
				elif age >= 30 and age < 40:
					age_range = '3'
				elif age >= 40 and age < 50:
					age_range = '4'
				elif age >= 50 and age < 60:
					age_range = '5'
				elif age >=60 and age < 70:
					age_range = '6'
				else:
					age_range = '7'
			except:
				print "didn't work", row[0], row[1]
			user_dict[(idA1 + '|' + idA2)] = (sex, occupation, state, education, income, age_range)
	atus_cps_file.close()

	print user_dict
	
	return user_dict

def group_keys(user_dict):
	"""
	This function groups the keys in the dict with the same demo characteristics.
	"""
	

	#this dictionary will flip the key value pairs, deduping the values to create the archetypes 
	#and grouping the ids

	archetype_dict = {}

	for key, value in user_dict.iteritems():
		if value not in archetype_dict:
			archetype_dict[value] = [key]
		else:
			archetype_dict[value].append(key)
	print archetype_dict
	return archetype_dict

# def load_spending:
# 	with open('./data')

def main():
    # You'll call each of the load_* functions with the session as an argument
    # load_mapping(session)
    # create_user_dict()
    first_dict=create_user_dict()
    group_keys(first_dict)
if __name__ == "__main__":
    # go = m.session
    # main(go)
    main()