import dbmodel as m
import csv
from math import log


def load_mapping(session):
	"""
	This function will seed our db with the primary keys from our data sets into a MappingIDs table.
	This table will be used as a lookup when we are categorizing habits.
	Reference the MappingID function in dbmodel for more info.
	"""
	# this section loads data from the ATUS file, which has a consumer unit ID and a person ID
	with open('./data/atuscps_2013/atuscps_2013.dat','rb') as atus_file:
		reader = csv.reader(atus_file, delimiter=',')
		for row in reader:
			primary_source_id = row[0] # this is the TUCASEID field
			secondary_source_id = row[1] #this is the TULINENO field
			subject_id = primary_source_id + '|' + secondary_source_id
			mapping = m.MappingID(subject_id=subject_id)
			session.add(mapping)
		atus_file.close()
	# this section loads data from the CEX file, which has a CU id, but no ref person (RP) ID, so using RP age as secondary
	with open('./data/cex_interview_2013/memi141.csv', 'rb') as cex_file:
		reader = csv.reader(cex_file, delimiter=',')
		for row in reader:
			primary_source_id = row[0] # this is NEWID field
			secondary_source_id = row[49] # this is the MEMBNO field
			subject_id = primary_source_id + "|" + secondary_source_id
			mapping = m.MappingID(subject_id = subject_id)
			session.add(mapping)
		cex_file.close()
	session.commit()

def create_user_dict(session):
	"""
	This function loads the Archetypes table.  This requires some logic, since this table aggregates data from the raw files.
	It also updates the mapping table with the Archetype ID that matches the primary and secondary ID
	"""
	#first we need to pull the two data sources together in a dictionary
	#doing this to make sure the right ages from one data source get added to the right users from the other
	
	user_dict = {}

	# this ATUS file gets the demo data
	with open('./data/atuscps_2013/atuscps_2013.dat','rb') as atus_cps_file:
		reader = csv.reader(atus_cps_file, delimiter=',')
		for row in reader:
			if reader.line_num == 1:
				continue
			idA1 = row[0]
			idA2 = row[1]
			sex = row[136]
			occupation = row[41]
			state = row[6]
			education = row[68]
			income = row[8]
			age = row[187]

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

	# demo data from CEX file
	with open('./data/cex_interview_2013/memi141.csv', 'rb') as cex_mem_file:
		reader = csv.reader(cex_mem_file, delimiter=',')
		for row in reader:
			if reader.line_num == 1:
				continue
			idA1 = row[0]
			idA2 = row[49]
			sex = row[64]
			occupation = row[50]
			education = row[22]
			age = row[1]

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
			except:
				print "didn't work", row[0], row[1]
		cex_mem_file.close()
			
	with open('./data/cex_interview_2013/fmli141.csv', 'rb') as cex_fml_file:
		reader = csv.reader(cex_fml_file, delimiter=',')
		for row in reader:
			if reader.line_num == 1:
				continue
			idB1 = row[0]
			if idB1 == idA1:
				income = int(row[366])
				state = int(row[367])
			else:
				continue
			user_dict[(idA1 + '|' + idA2)] = (sex, occupation, state, education, income, age_range)
		cex_fml_file.close()

	return user_dict

def group_archetype_keys(session, user_dict):
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

def load_archetype_table(session, archetype_dict):
	"""
	This function loops through the archetype dictionary created in the group_archetype_keys function, 
	where the archetypes were deduped, and adds the fields to the Archetypes table.
			
	"""
	#grab all of the values from each key and put them into the Archetypes table
	for key in archetype_dict:
		sex = key[0]
		occupation = key[1]
		state = key[2]
		education = key[3]
		income = key[4]
	  	age_range = key[5]
	  	hash_tuple = (sex, occupation, state, education, income, age_range)
	  	hash_id = hash(hash_tuple)
	  	archetype_load = m.Archetype(sex=sex, occupation=occupation, state=state,
	  		education=education, income=income, age_range=age_range, hash_id=hash_id)
		session.add(archetype_load)
	session.commit()


def main(session):
	# load the mapping table with out the archetype keys
    load_mapping(session)
    
    user_dict=create_user_dict(session)
    archetype_dict=group_archetype_keys(session, user_dict)
    load_archetype_table(session, archetype_dict)

if __name__ == "__main__":
    go = m.session
    main(go)
    # main()