#this file is the full calculation for the habit estimates using linear regression
#standalone that will run in the console with DB access

from __future__ import division

import model_ind as m
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, scoped_session
from sklearn import svm
import numpy as np
from array import array #
import sklearn
from sklearn.linear_model import LinearRegression

est = LinearRegression(fit_intercept=False)

############## TIME DATA ##############
# set up query for demo data from table and class
# note that queries are split up because previous calculations
# for work and sleep removed 0 values

def time_data_calc(user_predict, user_raw, user):
	"""
	This function calculations all predictions on time-related user_predict
	of the user based on their demo profile
	"""
	# unpack the user variable
	sex, age_range, region, income, education = user_raw
	print "first raw", sex, age_range, region, income, education
	# run queries for all data on habits

	#query and new vars for exercise
	time_db_ex = m.session.query(m.Time.sex, m.Time.age_range, m.Time.region, m.Time.income, m.Time.education,
		m.Time.exercise_habit_timemin).all()
	ex_demo = [(time_db_ex[i][0], time_db_ex[i][1], time_db_ex[i][2], time_db_ex[i][3], 
		time_db_ex[i][4]) for i in range(0, len(time_db_ex))]
	ex_data = [(time_db_ex[i][5]) for i in range(0, len(time_db_ex))]


	# note that summary data for work and sleep excluded '0' responses, keeping
	# that consistent here as well

	# query and vars for sleep
	time_db_sl = m.session.query(m.Time.sex, m.Time.age_range, m.Time.region,
		m.Time.income, m.Time.education, m.Time.sleep_habit_timemin).filter(m.Time.sleep_habit_timemin > 0).all()
	sl_demo = [(time_db_sl[i][0], time_db_sl[i][1], time_db_sl[i][2], time_db_sl[i][3], 
		time_db_sl[i][4]) for i in range(0, len(time_db_sl))]
	sl_data = [(time_db_sl[i][5]) for i in range(0, len(time_db_sl))]

	# query and vars for work
	time_db_wk = m.session.query(m.Time.sex, m.Time.age_range, m.Time.region,
		m.Time.income, m.Time.education, m.Time.work_habit_timemin).filter(m.Time.work_habit_timemin > 0).all()
	wk_demo = [(time_db_wk[i][0], time_db_wk[i][1], time_db_wk[i][2], time_db_wk[i][3], 
		time_db_wk[i][4]) for i in range(0, len(time_db_wk))]
	wk_data = [(time_db_wk[i][5]) for i in range(0, len(time_db_wk))]

	class TimeML:
		def __init__(self, timedemos, timedata):
			self.demos = timedemos
			self.time = timedata


	# create instances of the class
	exercise_data = TimeML(ex_demo, ex_data)
	sleep_data = TimeML(sl_demo, sl_data)
	work_data = TimeML(wk_demo, wk_data)

	## exercise data ##
	# assign variables to lists and convert lists of
	# tuples to numpy arrays -- feed in demo data and habit data from db
	y = exercise_data.time
	y = np.asarray(y)
	X = np.asarray(exercise_data.demos)

	print "********** Exercise **********"
	print "shape X", X.shape
	print "shape y", y.shape
	print "est.fit(X, y)", est.fit(X,y)
	print "est.coef_", est.coef_
	predict_exercise = est.predict(user)
	if predict_exercise < 0:
		predict_exercise = 0
	print "estimated hours of exercise", predict_exercise/60, "versus an average of 0.02 hours"


	## sleep data ##
	# assign variables to lists and convert lists of
	# tuples to numpy arrays -- feed in demo data and habit data from db
	y = sleep_data.time
	y = np.asarray(y)
	X = np.asarray(sleep_data.demos)



	print "********** Sleep **********"
	print "shape X", X.shape
	print "shape y", y.shape
	print "est.fit(X, y)", est.fit(X,y)
	print "est.coef_", est.coef_
	predict_sleep = est.predict(user)
	print "estimated hours of sleep ", predict_sleep/60, "versus an average of 8.8 hours"


	## work data ##
	# assign variables to lists and convert lists of
	# tuples to numpy arrays -- feed in demo data and habit data from db
	y = work_data.time
	y = np.asarray(y)
	X = np.asarray(work_data.demos)


	print "********** Work **********"
	print "shape X", X.shape
	print "shape y", y.shape
	print "est.fit(X, y)", est.fit(X,y)
	print "est.coef_", est.coef_
	predict_work = est.predict(user)
	if predict_work < 0:
		predict_work = 0
	print "estimated hours of work", predict_work/60, "versus an average of 7.2"

	user_predict['exercise'] = (predict_exercise/60)
	user_predict['sleep'] = (predict_sleep/60)
	user_predict['work'] = (predict_work/60)
	print "after time function ", user_predict
	return user_predict


############## MONEY DATA ##############


def money_data_calc(user_predict, user_raw, user):
	"""
	This function calculations all predictions on time-related user_predict
	of the user based on their demo profile
	"""
	# unpack the user variable
	sex, age_range, region, income, education = user_raw

	# query and vars for clothing
	money_db_cl = m.session.query(m.Money.sex, m.Money.age_range, m.Money.region,
		m.Money.income, m.Money.education, m.Money.spending_habit_clothes_dollars).filter(m.Money.spending_habit_clothes_dollars > 25).all()
	cl_demo = [(money_db_cl[i][0], money_db_cl[i][1], money_db_cl[i][2], money_db_cl[i][3], 
		money_db_cl[i][4]) for i in range(0, len(money_db_cl))]
	cl_data = [(money_db_cl[i][5]) for i in range(0, len(money_db_cl))]

	# query and vars for eating out
	money_db_eo = m.session.query(m.Money.sex, m.Money.age_range, m.Money.region,
		m.Money.income, m.Money.education, m.Money.spending_habit_eatout_dollars).all()
	eo_demo = [(money_db_eo[i][0], money_db_eo[i][1], money_db_eo[i][2], money_db_eo[i][3], 
		money_db_eo[i][4]) for i in range(0, len(money_db_eo))]
	eo_data = [(money_db_eo[i][5]) for i in range(0, len(money_db_eo))]


	class MoneyML:
		def __init__(self, moneydemos, moneydata):
			self.demos = moneydemos
			self.time = moneydata

	# create instances of the class feeding in our data
	clothes_data = MoneyML(cl_demo, cl_data)
	eatout_data = MoneyML(eo_demo, eo_data)


	## clothes data ##
	# assign variables to lists and convert lists of
	# tuples to numpy arrays -- feed in demo data and habit data from db
	y = clothes_data.time
	y = np.asarray(y)
	X = np.asarray(clothes_data.demos)


	print "********** Clothing **********"
	print "shape X", X.shape
	print "shape y", y.shape
	print "est.fit(X, y)", est.fit(X,y)
	print "est.coef_", est.coef_
	predict_clothing = est.predict(user)
	# constrain the value if the model gives us something outlandish
	if predict_clothing < 0:
		predict_clothing = 0
	if predict_clothing > 20333.33:
		predict_clothing = 20333.33 # current max value from original dataset
	print "estimated dollars spent on clothing $", predict_clothing, "versus an average of $0.94"

	## eat out data ##
	# assign variables to lists and convert lists of
	# tuples to numpy arrays -- feed in demo data and habit data from db
	y = eatout_data.time
	y = np.asarray(y)
	X = np.asarray(eatout_data.demos)



	print "********** Eating Out **********"
	print "shape X", X.shape
	print "shape y", y.shape
	print "est.fit(X, y)", est.fit(X,y)
	print "est.coef_", est.coef_
	predict_eatout = est.predict(user)
		# constrain the value if the model gives us something outlandish
	if predict_eatout < 0:
		predict_eatout = 0
	if predict_eatout > 9750:
		predict_eatout = 9750 # current max value from original dataset

	print "estimated dollars spent eating out $", predict_eatout, "versus an average of $9.37"

	user_predict['clothing'] = predict_clothing
	user_predict['eatout'] = predict_eatout
	
	return user_predict


def main(user_predict, user_raw, user):
	time_data_calc(user_predict, user_raw, user)
	money_data_calc(user_predict, user_raw, user)
	print user_predict
	return user_predict

if __name__=="__main__":
	main(user_predict, user_raw, user)







