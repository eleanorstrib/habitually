import model_ind as m
import csv
from math import log


###############################
# the first functions listed  #
# loop through the ATUS file  # 
# to gather demo and time data#
# for work and exercise habits#
###############################

def demo_data_atus(session):
	"""
	This function adds all of the ATUS demo data to a dictionary.
	"""
	user_dict_atus = {}

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

			# standardizing education codes for both studies by reorganizing ATUS codes to match CEX
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

			user_dict_atus[(idA1, idA2)] = [sex, education, age_range, region, income]

	atus_cps_file.close()
	print "created atus dictionary"
	return user_dict_atus

def load_exercising(session, user_dict_atus):
	"""
	This function loads the exercise table from the ATUS data set.
	"""
	exercise_raw = {}

	with open('./data/atussum_2013/atussum_2013.dat','rb') as atus_sum_file:
		reader = csv.reader(atus_sum_file, delimiter=',')

		#get the key demo information from the file
		for row in reader:
			if reader.line_num == 1:
				continue
			# get age and convert to range
			idA1 = row[0] #TUCASEID will use with demos to match to a record in the user_dict
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
			if (idA1, sex, education, age_range) not in exercise_raw:
				exercise_raw[idA1, sex, education, age_range] = 0

			NEC = int(row[270]) #exercise/sports not in another category
			exercise_raw[idA1, sex, education, age_range] = exercise_raw[idA1, sex, education, age_range] + NEC

			# now for the raw exercise data -- appending all time spent as the value for demo key and summing it together
			for x in range(236,260): #range is there because we want the values for t130126 to t130159
				exercise_var = int(row[x])
				exercise_raw[idA1, sex, education, age_range] = exercise_raw[idA1, sex, education, age_range] + exercise_var

	atus_sum_file.close()
	print exercise_raw
	print "finished looping through exercise file -- appending data to dict"
	# loop through the raw dict with the user_dict_atus to find which records to append the new value to
	# check the ID first then verify the other variables match 
	for k, v in user_dict_atus.iteritems():
		for kr, vr in exercise_raw.iteritems():
			if k[0] == kr[0]:
				if kr[1] == v[0] and kr[2] == v[1] and kr[3] == v[2]:
					user_dict_atus[k].append(vr)

	return user_dict_atus


def load_working(session, user_dict_atus):
	"""
	This function loads data for time worked at a primary job.
	"""
	work_raw = {}
	with open('./data/atussum_2013/atussum_2013.dat','rb') as atus_sum_file:
		reader = csv.reader(atus_sum_file, delimiter=',')

		#get the key demo information from the file
		for row in reader:
			if reader.line_num == 1:
				continue
			# get age and convert to range
			idA1 = row[0] #primary interview hhld id
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
			work_raw[(idA1, sex, education, age_range)] = 0

			# now for the raw work data -- appending and summing all time spent as the value for demo key
			work_var = int(row[127])
			work_raw[idA1, sex, education, age_range] = work_raw[idA1, sex, education, age_range] + work_var

	atus_sum_file.close()
	print "finished looping through work file -- appending data to dict"
	# loop through the raw dict with the user_dict_atus to find which records to append the new value to
	# check the ID first then verify the other variables match 
	for k, v in user_dict_atus.iteritems():
		for kr, vr in work_raw.iteritems():
			if k[0] == kr[0]:
				if kr[1] == v[0] and kr[2] == v[1] and kr[3] == v[2]:
					user_dict_atus[k].append(vr)

	return user_dict_atus


def remove_no_data_records_atus(session, user_dict_atus_all):
	"""
	This function removes the key/value pairs in the ATUS dictionary where there is no habit data, 
	as these records will slow the analysis if left in, and don't add value
	"""

	#dict where the final data will live
	atus_user_dict = {}

	# loop through the user_dict_atus_file, append records with more than just demos to the final dict
	print "removing incomplete records"
	for k, v in user_dict_atus_all.iteritems():
		if len(v) > 5:
			atus_user_dict[k] = v
	
	# get length of orginal vs new, clean dict
	original_count = len(user_dict_atus_all)
	clean_count = len(atus_user_dict)
	difference = original_count - clean_count

	print atus_user_dict
	print (difference, "records discarded from original ATUS data set")
	print (clean_count, "records retained in clean ATUS data set")
	return atus_user_dict


def commit_to_db_atus(session, atus_user_dict):
	"""
	Unpacks everything from the final ATUS dictionary, associates it with the appropriate db field, adds to Time db.
	"""
	for key, value in atus_user_dict.iteritems():
		hhld_id = key[0]
		person_id = key[1]
		sex = value[0]
		education = value[1]
		age_range = value[2]
		region = value[3]
		income = value[4]
		exercise_habit_timemin = value[5]
		work_habit_timemin = value[6]
		atus_commit = m.Time(hhld_id=hhld_id, person_id=person_id, sex=sex, education=education, age_range=age_range,
			region=region, income=income, exercise_habit_timemin=exercise_habit_timemin, work_habit_timemin=work_habit_timemin)
		session.add(atus_commit)
	session.commit()
	print "ATUS data committed to the database!"



#########################################
# That completes the ATUS data section  #
# Now adding CEX spend data on food/alc #
# and clothing                          #
#########################################


def demo_data_cex(session):
	"""
	This function adds all of the CEX demo data to a dictionary.
	Because the clothing expenditure data also happens to be in it, adding it here too to avoid having to create
	another function.

	"""
	# this dict will hold the data between opening files
	user_dict_cex = {}
	temp = {}

	with open('./data/cex_interview_2013/memi141.csv', 'rb') as cex_mem_file:
		reader_mem = csv.reader(cex_mem_file, delimiter=',')
		for row_mem in reader_mem:
			if reader_mem.line_num == 1:
				continue
				
			idA1 = row_mem[0]
			idA1 = idA1[:6]
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
			idF = idF[:6]
			for key, value in temp.iteritems():
				if key == idF:
					region = row_fml[116] #REGION in source
					temp[key].append(region)
					income = row_fml[366] #INCLASS in source
					temp[key].append(region)
					exp_quar = float(row_fml[259])
					temp[key].append(exp_quar)

	cex_fml_file.close()


	for key, value in temp.iteritems():
		user_dict_cex[(key, value[0])] = [value[1], value[4], value[2], value[5], value[3], value[6]]
	
	print "created cex dictionary with clothing spend data"
	return user_dict_cex


def load_spending_foodandbev(session, user_dict_cex):
	"""
	This function adds food and beverage spending to the cex dictionary.
	"""
	# create a temp dictionary to store some values we will need to find the right records.
	foodbev_temp = {}
	
	print "started food bev function"
	#first I will create a dictionary where the key is the household ID (there is no other demo info in the file)
	#and the value is the quarterly spending on clothes
	with open('./data/expn13/xpa13.csv', 'rb') as cex_xpa:
		reader = csv.reader(cex_xpa, delimiter=',')
		for row in reader:
			if reader.line_num == 1:
				continue
			idB1 = row[1] #NEWID, hhld identifier and interview ids; this data is only gathered at the hhld level
			idB1 = idB1[:6] #remove last digit which denotes which interview the info was gathered in
			try:	
				ooh_foodr = float(row[11]) #JDINEOQV, food bought in restaurants
			except:
				ooh_foodr = 0
			try:
				ooh_foodo = float(row[9]) #JOTHSTQV, food bought in cafes, bakeries, ordered in, etc
			except:
				ooh_foodo = 0
			try:
				ooh_alcohol = float(row[13]) #JALOUTQV alcohol bought in bars/taverns/restaurants, etc.
			except:
				ooh_alcohol = 0
			ooh_all = ooh_foodr + ooh_foodo + ooh_alcohol # sum together all 3 expenditures
			foodbev_temp[idB1] = ooh_all

	cex_xpa.close()

	#comparing to the cex dictionary and appending the value as appropriate
	for k, v in foodbev_temp.iteritems():
		for key, value in user_dict_cex.iteritems():
			if k == key[0]:
				user_dict_cex[key].append(v)
				
	
	print "completed food and bev info appending"

	return user_dict_cex


def remove_no_data_records_cex(session, user_dict_cex_all):
	"""
	This function removes the key/value pairs in the ATUS dictionary where there is no habit data, 
	as these records will slow the analysis if left in, and don't add value
	"""

	#dict where the final data will live
	cex_user_dict = {}

	# loop through the user_dict_atus_file, append records with more than just demos to the final dict
	print "removing incomplete records"
	for k, v in user_dict_cex_all.iteritems():
		if len(v) > 5:
			cex_user_dict[k] = v
	
	# get length of orginal vs new, clean dict
	original_count = len(user_dict_cex_all)
	clean_count = len(cex_user_dict)
	difference = original_count - clean_count

	print cex_user_dict
	print (difference, " records discarded from original CEX data set")
	print (clean_count, "records retained in clean CEX data set")
	return cex_user_dict


def commit_to_db_cex(session, cex_user_dict):
	"""
	Unpacks everything from the final CEX dictionary, associates it with the appropriate db field, adds to Money db.
	"""
	for key, value in cex_user_dict.iteritems():
		hhld_id = key[0]
		person_id = key[1]
		sex = value[0]
		education = value[1]
		age_range = value[2]
		region = value[3]
		income = value[4]
		spending_habit_clothes_dollars = value[5]
		spending_habit_eatout_dollars = value[6]
		cex_commit = m.Money(hhld_id=hhld_id, person_id=person_id, sex=sex, education=education,
			age_range=age_range, region=region, income=income, 
			spending_habit_clothes_dollars=spending_habit_clothes_dollars, 
			spending_habit_eatout_dollars=spending_habit_eatout_dollars)
		session.add(cex_commit)
	session.commit()
	print "CEX data committed to the database!"


def main(session):
	#atus files
	user_dict_atus = demo_data_atus(session)
	load_exercising(session, user_dict_atus)
	user_dict_atus_all = load_working(session, user_dict_atus)
	atus_user_dict = remove_no_data_records_atus(session, user_dict_atus_all)
	print "ATUS data dictionary created (atus_user_dict)"
	commit_to_db_atus(session, atus_user_dict)

	# cex files
	user_dict_cex = demo_data_cex(session)
	user_dict_cex_all = load_spending_foodandbev(session, user_dict_cex)
	cex_user_dict = remove_no_data_records_cex(session, user_dict_cex_all)
	commit_to_db_cex(session, cex_user_dict)


if __name__ == "__main__":
    go = m.session
    main(go)

