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

def main(session):
    # You'll call each of the load_* functions with the session as an argument
    load_mapping(session)

if __name__ == "__main__":
    go = m.session
    main(go)