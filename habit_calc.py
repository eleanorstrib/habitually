# this file performs all of the calculations on the habit data after
# a user enters their demo profile or signs in with Facebook

# # probability function takes self, item categpry

from __future__ import division

import model_ind as m
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, scoped_session
from sklearn import svm
import numpy as np
import codedict as cd
from array import array
from sklearn.linear_model import LinearRegression
est = LinearRegression(fit_intercept=False)


engine = create_engine("sqlite:///habit.db", echo=True)
Session = sessionmaker(bind=engine)

session = Session()


print ("*** " * 30)

print "CLASSIFIER TEST"

class TimeML:
	def __init__(self, timequery, timelist):
		self.d = timequery
		self.l = timelist



time_query = session.query(m.Time).all()
time_list = [[time_query[x].exercise_habit_timemin, time_query[x].work_habit_timemin, time_query[x].work_habit_timemin] for x in range (0, len(time_query))]



t = TimeML(time_query, time_list)

# assign variables to my lists and convert to numpy arrays
time_habits = t.l
time_habits= np.asarray(time_habits)
time_targets =[[30, 480, 480]]
time_targets = np.asarray(time_targets)


#attempt at linear regression 
est.fit(time_habits, time_targets)
est.coef_

print est.coef_

print time_habits.shape
print time_targets.shape


#  attempt at using the classifier
classifier = svm.SVC()

fitting = classifier.fit(time_habits, time_targets)

print fitting



# age = 3
# region = 3
# income = 9
# education = 12
# gender = 2


# money = session.query(m.Money).filter(m.Money.sex == gender, m.Money.age_range == age, m.Time.region == region)
# money_result = money.all()

# time = session.query(m.Time).filter(m.Time.sex == gender, m.Time.age_range == age, m.Time.education== education, m.Time.region == region)
# time_result = time.all()




# time_list_e = []
# time_list_w = []
# time_list_s = []
# for item in range (0, len(time_result)):
# 	exercise = time_result[item].exercise_habit_timemin
# 	work = time_result[item].work_habit_timemin
# 	sleep = time_result[item].sleep_habit_timemin

# 	time_list_e.append(exercise)
# 	if work !=0:
# 		time_list_w.append(work)
# 	time_list_s.append(sleep)
# print "Exercise", (sum(time_list_e)/len(time_list_e)), ((sum(time_list_e)/len(time_list_e))/60)
# print "Work", (sum(time_list_w)/len(time_list_w)), ((sum(time_list_w)/len(time_list_w))/60)
# print "Sleep", (sum(time_list_s)/len(time_list_s)), (sum(time_list_s)/len(time_list_s)/60)

# money_list_c = []
# money_list_e = []
# for item in range (0, len(money_result)):
# 	clothes = money_result[item].spending_habit_clothes_dollars
#  	eatout = money_result[item].spending_habit_eatout_dollars
#  	money_list_c.append(clothes)
#  	money_list_e.append(eatout)
# print "Clothes", (sum(money_list_c)/len(money_list_c))
# print "eat out", (sum(money_list_e)/len(money_list_e))



# time_result = time.all()
# print time_result


# temp_list = []
# for item in range (0, len(time_result)):
# 	sex = time_result[item].sex
# 	age_range = time_result[item].age_range
# 	income = time_result[item].income
# 	education = time_result[item].education
# 	region = time_result[item].region
# 	exercise = time_result[item].exercise_habit_timemin
# 	work = time_result[item].work_habit_timemin
# 	sleep = time_result[item].sleep_habit_timemin
# 	temp_list.append([sex, age_range, income, education, region, exercise, work, sleep])
# print temp_list


# money = session.query(m.Money).filter(m.Money.sex == gender, m.Money.age_range == age, m.Money.education== education)
# money_result = money.all()

# print money_result


# print ("*** " * 30)



# #exercise, work, sleep in minutes per day
# target =[[30], [480], [480]]

# classifier = svm.SVC()



# X = temp_list
# print X
# Y = numpy.ravel(target)
# print Y

# for z in range (0, len(X)):
# 	cls_output = classifier.fit(X[z][:], Y[:])

# print cls_output

# p_output = classifier.predict(X[-3])

# print p_output



# print ("*** " * 30)

# print "PROBABILITY TIME"

# all_records = int(session.query(m.Time).count())


# no_male = session.query(m.Time).filter(m.Time.sex == 1).count()
# no_female = session.query(m.Time).filter(m.Time.sex == 2).count()

# regno1 = session.query(m.Time).filter(m.Time.region == 1).count()
# regno2 = session.query(m.Time).filter(m.Time.region == 2).count()
# regno3 = session.query(m.Time).filter(m.Time.region == 3).count()
# regno4 = session.query(m.Time).filter(m.Time.region == 4).count()

# edno0 = session.query(m.Time).filter(m.Time.education == 0).count()
# edno10 = session.query(m.Time).filter(m.Time.education == 10).count()
# edno11 = session.query(m.Time).filter(m.Time.education == 11).count()
# edno12 = session.query(m.Time).filter(m.Time.education == 12).count()
# edno13 = session.query(m.Time).filter(m.Time.education == 13).count()
# edno14 = session.query(m.Time).filter(m.Time.education == 14).count()
# edno15 = session.query(m.Time).filter(m.Time.education == 15).count()
# edno16 = session.query(m.Time).filter(m.Time.education == 16).count()
# edno17 = session.query(m.Time).filter(m.Time.education == 17).count()

# prob_male = no_male/all_records
# prob_female = no_female/all_records

# prob_reg1 = regno1/all_records
# prob_reg2 = regno2/all_records
# prob_reg3 = regno3/all_records
# prob_reg4 = regno4/all_records

# prob_ed0 = edno0/all_records
# prob_ed10 = edno10/all_records
# prob_ed11= edno11/all_records
# prob_ed12 = edno12/all_records
# prob_ed13 = edno13/all_records
# prob_ed14 = edno14/all_records
# prob_ed15 = edno15/all_records
# prob_ed15 = edno15/all_records
# prob_ed16 = edno16/all_records
# prob_ed17 = edno17/all_records

# print ("male", prob_male)
# print ("female", prob_female)
# print ("prob regions : ", prob_reg1, prob_reg2, prob_reg3, prob_reg4)
# print("prob edu: ", prob_ed0, prob_ed10, prob_ed11, prob_ed12, prob_ed13, prob_ed14, prob_ed15, prob_ed16, prob_ed17)
# fem_4 = regno4/no_female

# print "prob female and region 4", fem_4







