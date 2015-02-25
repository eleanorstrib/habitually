"""
This file contains all of the coding dictionaries to interpret data from two studies conducted
by the Department of Labor.

1 - The American Time Use Survey (ATUS) -  http://www.bls.gov/tus/
2 - The Consumer Expenditure Survey (CEX) - http://www.bls.gov/cex/home.htm

As the CEX study has more general categories and the data needed to be comparable, the coding
for both studies on demographics has been normalized to the CEX groupings.  To facilitate faster
analysis, the raw ages reported in both studies have been coded by age group, as shown below.

"""
sex_codes = {
	'1' : "male",
	'2' : "female",
}

age_range_codes = {
	'1' : ["Under 20"],
	'2' : ["20-29", "twenties"],
	'3' : ["30-39", "thirties"], 
	'4' : ["40-49", "forties"],
	'5' : ["50-59", "fifties"],
	'6' : ["60-69", "sixties"],
	'7' : ["70+", "seventies"],
}


education_codes = {
	0 : "Never attended school",
	10 : "First through 8th grade",
	11 : "Ninth through 12th grade (did not graduate)",
	12 : "High school graduate",
	13 : "Some college (did not graduate)",
	14 : "Associate's/vocational degree",
	15 : "Bachelor's degree",
	16 : "Master's or Doctoral degree",
	17 : "No data reported"
}

region_codes = {
	1: { 'Northeast':
			[("Connecticut", "CT"), ("Maine", "ME"), ("Massachusetts", "MA"),
			("New Hampshire", "NH"), ("New Jersey", "NJ"), ("New York", "NY"), 
			("Pennsylvania", "PA"), ("Rhode Island"), ("Vermont", "VT")],
		},
	2: {'Midwest':
			[("Illinois", "IL"), ("Indiana", "IN"), ("Iowa", "IA"), ("Kansas", "KS"), ("Michigan", "MI"),
			("Minnesota", "MN"), ("Missouri", "MO"), ("Nebraska", "NB"), ("North Dakota", "ND"), 
			("Ohio", "OH"), ("South Dakota", "SD"), ("Wisconsin", "WI")],
		},
	3 : {'South': 
			[("Alabama", "AL"), ("Arkansas", "AK"), ("Delaware", "DE"), ("District of Columbia", "DC"), 
			("Florida", "FL"), ("Georgia", "GA"), ("Kentucky", "KY"), ("Louisiana", "LA"), ("Maryland", "MD"),
			("Mississippi", "MI"), ("North Carolina", "NC"), ("Oklahoma", "OK"), ("South Carolina", "SC"),
			("Tennessee", "TN"), ("Texas", "TX"), ("Virginia", "VA"), ("West Virginia", "WV")],
	},
	4 : {'West':
		[("Alaska", "AK"), ("Arizona", "AZ"), ("California", "CA"), ("Colorado", "CO"), ("Hawaii", "HI"),
		("Idaho", "ID"), ("Montana", "MT"), ("Nevada", "NV"), ("New Mexico", "NM"), ("Oregon", "OR"),
		("Utah", "UT"), ("Washington", "WA"), ("Wyoming", "WI")],
	},

}

income_codes = {
 	1 : "Less than $5,000",
 	2 : "$5,000 to $9,999",
 	3 : "$10,000 to $14,999",
 	4 : "$15,000 to $19,999",
 	5 : "$20,000 to $29,999",
 	6 : "$30,000 to $39,999",
 	7 : "$40,000 to $49,999",
 	8 : "$50,000 to $69,999",
 	9 : "$70,000 and over",
}