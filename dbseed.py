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
	with open('./data/atuscps_2013/atuscps_2013.dat','rb') as atus_cps_file:
		reader = csv.reader(atus_cps_file, delimiter=',')
		for row in reader:
			if reader.line_num == 1:
				continue
			idA1 = row[0]
			idA2 = row[1]
			sex = str(row[136])
			occupation = str(row[41])
			region = str(row[4])
			education = str(row[68])

			# standardizing income for both studies by recategorizing ATUS codes to match CEX
			income_raw = str(row[8])
			if income_raw == '1':
				income = '1'
			if income_raw == '2' or income_raw == '3':
				income = '2'
			if income_raw == '4' or income_raw == '5':
				income = '3'
			if income_raw == '6':
				income = '4'
			if income_raw == '7' or income_raw == '8':
				income = '5'
			if income_raw == '9' or income_raw == '10':
				income = '6'
			if income_raw == '11':
				income = '7'
			if income_raw == '12' or income_raw == '13':
				income = '8'
			if income_raw == '14' or income_raw == '15' or income_raw == '16':
				income = '9'

			#putting "raw" age into ranges for analysis
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
			user_dict[(idA1 + '|' + idA2)] = (sex, occupation, region, education, income, age_range)
			user_dict_archid[(idA1 + '|' + idA2)]= sex+occupation+region+education+income+age_range
		atus_cps_file.close()

	# demo data from CEX file
	# cex_temp = {}
	# with open('./data/cex_interview_2013/memi141.csv', 'rb') as cex_mem_file:
	# 	reader = csv.reader(cex_mem_file, delimiter=',')
	# 	for row in reader:
	# 		if reader.line_num == 1:
	# 			continue
	# 		idA1 = row[0]
	# 		idA2 = row[49]
	# 		sex = str(row[64])
	# 		occupation = str(row[50])
	# 		education = str(row[22])
	# 		print idA1
	# 		cex_temp[idA1]['idA2'] = idA2
	# 		cex_temp[idA1]['sex'] = sex
	# 		cex_temp[idA1]['occupation'] = occupation
	# 		cex_temp[idA1]['education'] = education
	# 		age = row[1]

	# 		try:
	# 			age = int(age)
	# 			if age < 20:
	# 				cex_temp[idA1]['age_range'] = '1'
	# 			elif age >= 20 and age < 30:
	# 				cex_temp[idA1]['age_range'] = '2'
	# 			elif age >= 30 and age < 40:
	# 				cex_temp[idA1]['age_range'] = '3'
	# 			elif age >= 40 and age < 50:
	# 				cex_temp[idA1]['age_range'] = '4'
	# 			elif age >= 50 and age < 60:
	# 				cex_temp[idA1]['age_range'] = '5'
	# 			elif age >=60 and age < 70:
	# 				cex_temp[idA1]['age_range'] = '6'
	# 			else:
	# 				cex_temp[idA1]['age_range'] = '7'
	# 		except:
	# 			print "didn't work", row[0], row[1]

	# 	cex_mem_file.close()
			
	# with open('./data/cex_interview_2013/fmli141.csv', 'rb') as cex_fml_file:
	# 	reader = csv.reader(cex_fml_file, delimiter=',')
	# 	for row in reader:
	# 		if reader.line_num == 1:
	# 			continue
	# 		idB1 = row[0]
	# 		if cex_temp[idA1]==idB1:
	# 			cex_temp[idA1]['income'] = str(row[366]) #INCLASS in source
	# 			cex_temp[idA1]['region'] = str(row[116]) #REGION in source
	# 		user_dict[(cex_temp[idA1] + '|' + cex_temp[idA1][idA2])] = (cex_temp[idA1]['sex'], 
	# 			cex_temp[idA1]['occupation'], cex_temp[idA1]['region'], cex_temp[idA1]['education'],
	# 			cex_temp[idA1]['income'], cex_temp[idA1]['age_range'])
	# 		user_dict_archid[(cex_temp[idA1] + '|' + cex_temp[idA1][idA2])] = (cex_temp[idA1]['sex']+ 
	# 			cex_temp[idA1]['occupation'] + cex_temp[idA1][region] + cex_temp[idA1][education] + 
	# 			cex_temp[idA1]['income'] + cex_temp[idA1]['age_range'])
	# 	cex_fml_file.close()

	# user_dict = user_dict.extend(cex_temp)

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
    print user_dict_archid
    archetype_dict=group_archetype_keys(session, user_dict)
    load_archetype_table(session, archetype_dict)
    print user_dict_archid
    load_mapping(session, user_dict_archid)
    # add_arch_ids(session, user_dict)

if __name__ == "__main__":
    go = m.session
    main(go)
    # main()



