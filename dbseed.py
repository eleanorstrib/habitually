import dbmodel as m
import csv
from math import log
import numpy

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
			region = str(row[4])

			#standardizing education codes for both studies by reorganizing ATUS codes to match CEX
			education_raw = row[68]
			if education_raw == '31' or education_raw == '32' or education_raw == '33' or education_raw == '34':
				education = '10'
			if education_raw == '35' or education_raw == '36' or education_raw == '37' or education_raw == '38':
				education = '11'
			if education_raw == '39':
				education = '12'
			if education_raw =='40':
				education = '13'
			if education_raw == '41' or education_raw == '42':
				education = '14'
			if education_raw == '43':
				eduation = '15'
			if education_raw == '45' or education_raw == '46':
				education = '16'


			# standardizing income for both studies by recategorizing ATUS codes to match CEX
			income_raw = row[8]
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
			user_dict[(idA1 + '|' + idA2)] = (sex, education, age_range, region, income)
			user_dict_archid[(idA1 + '|' + idA2)]= sex+education+age_range+region+income
		atus_cps_file.close()

	temp = {}

# demo data from CEX file
	with open('./data/cex_interview_2013/memi141.csv', 'rb') as cex_mem_file:
		reader_mem = csv.reader(cex_mem_file, delimiter=',')
		for row_mem in reader_mem:
			if reader_mem.line_num == 1:
				continue
				
			idA1 = row_mem[0]
			idA2 = row_mem[49]
			sex = row_mem[64]
			education = row_mem[22]

			age = row_mem[1]

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


			temp[idA1] = [idA2, sex, education, age_range]
	cex_mem_file.close()
	
	with open('./data/cex_interview_2013/fmli141.csv', 'rb') as cex_fml_file:
		reader_fml = csv.reader(cex_fml_file, delimiter=',')

		for row_fml in reader_fml:
			idF = row_fml[0]
			for key, value in temp.iteritems():
				if key == idF:
					region = row_fml[116] #REGION in source
					temp[key].append(region)
					income = row_fml[366] #INCLASS in source
					temp[key].append(region)

	cex_fml_file.close()

	for key, value in temp.iteritems():
		user_dict[(key + "|" + value[0])] = (value[1], value[4], value[2], value[5], value[3])
		user_dict_archid[(key + "|" + value[0])]= value[1] + value[4] + value[2] + value[5]+ value[3]
		
		user_dict[(idA1 + '|' + idA2)] = (sex, education, age_range, region, income)
		user_dict_archid[(idA1 + '|' + idA2)]= sex+education+age_range+region+income
		
		cex_mem_file.close()
		cex_fml_file.close()

	return_this = [user_dict, user_dict_archid]
	print user_dict
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
		region = key[1]
		education = key[2]
		income = key[3]
	  	age_range = key[4]
	  	value_id = sex+education+age_range+region+income
	 
	  	archetype_load = m.Archetype(sex=sex, region=region, education=education, income=income, 
	  		age_range=age_range, value_id=value_id)
		session.add(archetype_load)
	session.commit()


def load_mapping(session, user_dict_archid):
	"""
	This function takes the subject ids and value IDs from the user dict we created with 
	archetype ids and adds them to the MappingID table.
	"""

	for key, value in user_dict_archid.iteritems():
		subject_id = key
		value_id = value
		mapping = m.MappingID(subject_id=subject_id, value_id=value_id)
		session.add(mapping)
	session.commit()


def load_sleeping(session):
	"""
	This function populates the sleeping table
	"""
	sleeping_raw = {}
	sleeping_data = {}
	with open('./data/atussum_2013/atussum_2013.dat','rb') as atus_sum_file:
		reader = csv.reader(atus_sum_file, delimiter=',')
		for row in reader:
			if reader.line_num == 1:
				continue
				# get age and convert to range
			age = row[3] #TEAGE
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
			
			sex = row[4] #TESEX
			
			education_raw = row[5] #PEEDUCA
			if education_raw == '31' or education_raw == '32' or education_raw == '33' or education_raw == '34':
				education = '10'
			if education_raw == '35' or education_raw == '36' or education_raw == '37' or education_raw == '38':
				education = '11'
			if education_raw == '39':
				education = '12'
			if education_raw =='40':
				education = '13'
			if education_raw == '41' or education_raw == '42':
				education = '14'
			if education_raw == '43':
				eduation = '15'
			if education_raw == '45' or education_raw == '46':
				education = '16'

			#create a dictionary with all of the values for each combo of demos available
			if (sex, education, age_range) not in sleeping_data:
				sleeping_raw[(sex, education, age_range)] = []

			time_sleep = int(row[24]) #t010101
			sleeping_raw[(sex, education, age_range)].append(time_sleep)

			for key, value in sleeping_raw.iteritems():
				sleeping_data[key] = [min(value), max(value), ((reduce(lambda x,y: x+y, value))/len(value))]

	atus_sum_file.close()
	print sleeping_data

	for key, value in sleeping_data.iteritems():
		sex = key[0]
		education = key[1]
		age_range = key[2]
		min_minutes = value[0]
		max_minutes = value[1]
		avg_minutes = value[2]
		value_id_h = sex+education+age_range
		sleeping = m.Sleeping(sex=sex, education=education, age_range=age_range, min_minutes=min_minutes, 
			max_minutes=max_minutes, avg_minutes=avg_minutes, value_id_h=value_id_h)
		session.add(sleeping)
		print "right before commit"
	session.commit()
	print "commit sleep ran"

def load_exercising(session):
	"""
	This function loads the exercise table
	"""
	exercise_raw = {}
	exercise_data = {}
	with open('./data/atussum_2013/atussum_2013.dat','rb') as atus_sum_file:
		reader = csv.reader(atus_sum_file, delimiter=',')

		#get the key demo information from the file
		for row in reader:
			if reader.line_num == 1:
				continue
			# get age and convert to range
			age = row[3] #TEAGE
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
			
			sex = row[4] #TESEX
			
			education_raw = row[5] #PEEDUCA
			if education_raw == '31' or education_raw == '32' or education_raw == '33' or education_raw == '34':
				education = '10'
			if education_raw == '35' or education_raw == '36' or education_raw == '37' or education_raw == '38':
				education = '11'
			if education_raw == '39':
				education = '12'
			if education_raw =='40':
				education = '13'
			if education_raw == '41' or education_raw == '42':
				education = '14'
			if education_raw == '43':
				eduation = '15'
			if education_raw == '45' or education_raw == '46':
				education = '16'

			# add the demo values as keys in the 'raw' dictionary
			if (sex, education, age_range) not in exercise_raw:
				exercise_raw[sex, education, age_range] = []

			NEC = int(row[270]) #exercise/sports not in another category
			exercise_raw[sex, education, age_range].append(NEC)

			# now for the raw exercise data -- appending all time spent as the value for key demo key
			for x in range(236,260): #range is there because we want the values for t130126 to t130159
				exercise_var = int(row[x])
				exercise_raw[sex, education, age_range].append(exercise_var)

			for key, value in exercise_raw.iteritems():
				exercise_data[key] = [min(value), max(value), ((reduce(lambda x,y: x+y, value))/len(value))]

	atus_sum_file.close()

	for key, value in exercise_data.iteritems():
		sex = key[0]
		education = key[1]
		age_range = key[2]
		min_minutes = value[0]
		max_minutes = value[1]
		avg_minutes = value[2]
		value_id_h = sex+education+age_range
		exercise = m.Exercising(sex=sex, education=education, age_range=age_range, min_minutes=min_minutes, 
			max_minutes=max_minutes, avg_minutes=avg_minutes, value_id_h=value_id_h)
		session.add(exercise)
	session.commit()
	print "commit exercise ran"


def load_working(session):
	"""
	This function loads the work table
	"""
	work_raw = {}
	work_data = {}
	with open('./data/atussum_2013/atussum_2013.dat','rb') as atus_sum_file:
		reader = csv.reader(atus_sum_file, delimiter=',')

		#get the key demo information from the file
		for row in reader:
			if reader.line_num == 1:
				continue
			# get age and convert to range
			age = row[3] #TEAGE
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
			
			sex = row[4] #TESEX
			
			education_raw = row[5] #PEEDUCA
			if education_raw == '31' or education_raw == '32' or education_raw == '33' or education_raw == '34':
				education = '10'
			if education_raw == '35' or education_raw == '36' or education_raw == '37' or education_raw == '38':
				education = '11'
			if education_raw == '39':
				education = '12'
			if education_raw =='40':
				education = '13'
			if education_raw == '41' or education_raw == '42':
				education = '14'
			if education_raw == '43':
				eduation = '15'
			if education_raw == '45' or education_raw == '46':
				education = '16'

			# add the demo values as keys in the 'raw' dictionary
			if (sex, education, age_range) not in work_raw:
				work_raw[(sex, education, age_range)] = []

			# now for the raw work data -- appending all time spent as the value for key demo key
			work_var = int(row[127])
			work_raw[sex, education, age_range].append(work_var)

			#add these values to the final dict with stats
			for key, value in work_raw.iteritems():
				work_data[key] = [min(value), max(value), ((reduce(lambda x,y: x+y, value))/len(value))]

	atus_sum_file.close()

	for key, value in work_data.iteritems():
		sex = key[0]
		education = key[1]
		age_range = key[2]
		min_minutes = value[0]
		max_minutes = value[1]
		avg_minutes = value[2]
		value_id_h = sex+education+age_range
		work = m.Working(sex=sex, education=education, age_range=age_range, min_minutes=min_minutes, 
			max_minutes=max_minutes, avg_minutes=avg_minutes, value_id_h=value_id_h)
		session.add(work)
	session.commit()
	print "commit work ran"








def main(session):
	# load the mapping table with out the archetype keys
    
    user_dict=create_user_dict(session)[0]
    user_dict_archid=create_user_dict(session)[1]
    print user_dict_archid
    archetype_dict=group_archetype_keys(session, user_dict)
    load_archetype_table(session, archetype_dict)
    print user_dict_archid
    load_mapping(session, user_dict_archid)
    load_sleeping(session)
    load_working(session)
    load_exercising(session)


if __name__ == "__main__":
    go = m.session
    main(go)
    # main()



