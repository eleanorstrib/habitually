import dbmodel as m
import csv
from math import log

def create_user_dict(session):
	"""
	This function loads the Archetypes table.  This requires some logic, since this table aggregates data from the raw files.
	It also updates the mapping table with the Archetype ID that matches the primary and secondary ID
	"""
	#first we need to pull the two data sources together in a dictionary
	#doing this to make sure the right ages from one data source get added to the right users from the other
	
	user_dict = {}
	user_dict_archid = {}

	# this ATUS file gets the demo data
	# with open('./data/atuscps_2013/atuscps_2013.dat','rb') as atus_cps_file:
	# 	reader = csv.reader(atus_cps_file, delimiter=',')
	# 	for row in reader:
	# 		if reader.line_num == 1:
	# 			continue
	# 		idA1 = row[0]
	# 		idA2 = row[1]
	# 		sex = str(row[136])
	# 		occupation = str(row[41])
	# 		region = str(row[4])
	# 		education = str(row[68])
	# 		income = str(row[8])
	# 		age = row[187]

	# 		try:
	# 			age = int(age)
	# 			if age < 20:
	# 				age_range = '1'
	# 			elif age >= 20 and age < 30:
	# 				age_range = '2'
	# 			elif age >= 30 and age < 40:
	# 				age_range = '3'
	# 			elif age >= 40 and age < 50:
	# 				age_range = '4'
	# 			elif age >= 50 and age < 60:
	# 				age_range = '5'
	# 			elif age >=60 and age < 70:
	# 				age_range = '6'
	# 			else:
	# 				age_range = '7'
	# 		except:
	# 			print "didn't work", row[0], row[1]
	# 		user_dict[(idA1 + '|' + idA2)] = (sex, occupation, region, education, income, age_range)
	# 		user_dict_archid[(idA1 + '|' + idA2)]= sex+occupation+region+education+income+age_range
	# 	atus_cps_file.close()

	# demo data from CEX file
	with open('./data/cex_interview_2013/memi141.csv', 'rb') as cex_mem_file:
		reader = csv.reader(cex_mem_file, delimiter=',')
		for row in reader:
			if reader.line_num == 1:
				continue
			idA1 = row[0]
			idA2 = row[49]
			sex = str(row[64])
			occupation = str(row[50])
			education = str(row[22])
			age = row[1]

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
		cex_mem_file.close()
			
	with open('./data/cex_interview_2013/fmli141.csv', 'rb') as cex_fml_file:
		reader = csv.reader(cex_fml_file, delimiter=',')
		for row in reader:
			if reader.line_num == 1:
				continue
			idB1 = row[0]
			if idB1 == idA1:
				income = str(row[366]) #INCLASS in source
				region = str(row[116]) #REGION in source
			else:
				continue
			user_dict[(idA1 + '|' + idA2)] = (sex, occupation, region, education, income, age_range)
			user_dict_archid[(idA1 + '|' + idA2)]= sex+occupation+region+education+income+age_range
		cex_fml_file.close()

	return_this = [user_dict, user_dict_archid]
	return return_this

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
		region = key[2]
		education = key[3]
		income = key[4]
	  	age_range = key[5]
	  	value_id = sex+occupation+region+education+income+age_range
	 
	  	archetype_load = m.Archetype(sex=sex, occupation=occupation, region=region,
	  		education=education, income=income, age_range=age_range, value_id=value_id)
		session.add(archetype_load)
	session.commit()

def load_mapping(session, user_dict_archid):
	"""
	This function takes the subject ids and value IDs from the user dict we created with 
	archetype ids and adds them to the MappingID table.
	"""
	# this section loads data from the ATUS file, which has a consumer unit ID and a person ID
	# with open('./data/atuscps_2013/atuscps_2013.dat','rb') as atus_file:
	# 	reader = csv.reader(atus_file, delimiter=',')
	# 	for row in reader:
	# 		if reader.line_num == 1:
	# 			continue
	# 		primary_source_id = row[0] # this is the TUCASEID field
	# 		secondary_source_id = row[1] #this is the TULINENO field
	# 		subject_id = primary_source_id + '|' + secondary_source_id
	# 		value_id = user_dict_archid[subject_id]
	# 		mapping = m.MappingID(subject_id=subject_id, value_id=value_id)
	# 		session.add(mapping)
	# 	atus_file.close()
	# this section loads data from the CEX file, which has a CU id, but no ref person (RP) ID, so using RP age as secondary
	# with open('./data/cex_interview_2013/memi141.csv', 'rb') as cex_file:
	# 	reader = csv.reader(cex_file, delimiter=',')

	# 	for row in reader:
	# 		if reader.line_num == 1:
	# 			continue
	# 		primary_source_id = row[0] # this is NEWID field
	# 		secondary_source_id = row[49] # this is the MEMBNO field
	# 		subject_id = primary_source_id + '|' + secondary_source_id
	# 		value_id = user_dict_archid[subject_id]
	# 		mapping = m.MappingID(subject_id=subject_id, value_id=value_id)
	# 		session.add(mapping)
	# 	cex_file.close()
	for key, value in user_dict_archid.iteritems():
		subject_id = key
		value_id = value
		mapping = m.MappingID(subject_id=subject_id, value_id=value_id)
		session.add(mapping)
	session.commit()



def main(session):
	# load the mapping table with out the archetype keys
    
    user_dict=create_user_dict(session)[0]
    user_dict_archid=create_user_dict(session)[1]
    archetype_dict=group_archetype_keys(session, user_dict)
    load_archetype_table(session, archetype_dict)
    load_mapping(session, user_dict_archid)
    # add_arch_ids(session, user_dict)

if __name__ == "__main__":
    go = m.session
    main(go)
    # main()



## code from an approach I've since abandoned...will likely delete
# def add_arch_ids(session, user_dict_archid):
# 	"""
# 	This function adds the archetype IDs to the mapping table so we can cross reference them
# 	"""

# 	#query the database for the value_id and id(primary key) from the Archetypes table
# 	database_values = session.query(m.Archetype.value_id, m.Archetype.id).all()
# 	print database_values
	
# 	#create a new dict to store the combined value string as the key and the primary id from the table as the value.
# 	value_dict_db = {}
# 	for row in database_values:
# 		value_id = row[0]
# 		id_prim = row[1]
# 		value_dict_db[value_id]=id_prim
# 	print value_dict_db


# 	#finally, we compare the keys of the first dict to the keys of the second
# 	#when the keys match, we take the value from the first dict, and look at the subject_id
# 	#(value of 2nd dict) and add the value of the first dict(primary key for archetype) 
# 	#to the record of the relevant user in the db
# 	for k_db, v_db in value_dict_db.iteritems():
# 		print "got into first part of dict loop"
# 		for k_user, v_user in user_dict_archid.iteritems():
# 			print "kdb =" + str(k_db)
# 			print "k_user =" + str(k_user)
# 			if k_db == k_user:
# 				print "got into if regionment in dict loop"
# 				archetype_id = value_dict_db[k_db]
# 				subject_id = user_dict_archid[k_user]
# 				add_arch_id = m.MappingID(archetype_id=archetype_id)
# 				print "got past add arch id"
# 				session.add(add_arch_id)
# 	session.commit()

