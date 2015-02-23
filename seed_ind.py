import dbmodel as m
import csv
from math import log



def demo_data_atus():
	"""
	This function adds all of the ATUS demo data to the tables.
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
			user_dict[(idA1, idA2)] = [sex, education, age_range, region, income]

		atus_cps_file.close()

		return user_dict

def demo_data_cex():
	"""
	This function adds all of the CEX demo data to a dictionary.

	"""
	# this dict will hold the data between opening files
	user_dict = {}
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

	cex_fml_file.close()

	for key, value in temp.iteritems():
		user_dict[(key, value[0])] = (value[1], value[4], value[2], value[5], value[3])

	print user_dict
	return user_dict

def main():
	user_dict = demo_data_atus()
	user_dict_alldemos = demo_data_cex(user_dict)


    


if __name__ == "__main__":
    # go = m.session
    # main(go)
    main()





# def normalize_education(variable):
# 	"""
# 	This function standardizes education codes across the datasets by reorganizing ATUS codes to match CEX
# 	"""
# 	education_raw = row[68]
# 	if education_raw == '31' or education_raw == '32' or education_raw == '33' or education_raw == '34':
# 		education = '10'
# 	if education_raw == '35' or education_raw == '36' or education_raw == '37' or education_raw == '38':
# 		education = '11'
# 	if education_raw == '39':
# 		education = '12'
# 	if education_raw =='40':
# 		education = '13'
# 	if education_raw == '41' or education_raw == '42':
# 		education = '14'
# 	if education_raw == '43':
# 		eduation = '15'
# 	if education_raw == '45' or education_raw == '46':
# 		education = '16'

# 	print education
# 	return education

# def normalize_income(variable):
# 	"""
# 	This function standardizes income codes across the datasets by reorganizing ATUS codes to match CEX
# 	"""
# 	income_raw = row[8]
# 	if income_raw == '1':
# 		income = '1'
# 	if income_raw == '2' or income_raw == '3':
# 		income = '2'
# 	if income_raw == '4' or income_raw == '5':
# 		income = '3'
# 	if income_raw == '6':
# 		income = '4'
# 	if income_raw == '7' or income_raw == '8':
# 		income = '5'
# 	if income_raw == '9' or income_raw == '10':
# 		income = '6'
# 	if income_raw == '11':
# 		income = '7'
# 	if income_raw == '12' or income_raw == '13':
# 		income = '8'
# 	if income_raw == '14' or income_raw == '15' or income_raw == '16':
# 		income = '9'

# 	print income
# 	return income
