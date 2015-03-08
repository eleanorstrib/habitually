# this file performs all of the calculations on the habit data after
# a user enters their demo profile or signs in with Facebook

from __future__ import division

import model_ind as m
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, scoped_session
from sklearn import svm
import numpy as np
from array import array
import sklearn
from sklearn.linear_model import LinearRegression

est = LinearRegression(fit_intercept=False)


engine = create_engine("sqlite:///habit.db")
Session = sessionmaker(bind=engine)

session = Session()


print ("*** " * 30)

print "CLASSIFIER TEST"

# variables that will be passed in
gender=2
age_range=3
region=3
income=4
education=4
# create a numpy array out of the user variables
user = [gender, age_range, region, income, education]
user = np.asarray(user)
print "numpy array for user: ", user

############## TIME DATA ##############
# set up query for demo data from table and class
# note that queries are split up because previous calculations
# for work and sleep removed 0 values
time_demo_exercise = session.query(m.Time.sex, m.Time.age_range, m.Time.region, m.Time.income, m.Time.education).all()
time_demo_sleep = session.query(m.Time.sex, m.Time.age_range, m.Time.region,
	m.Time.income, m.Time.education).filter(m.Time.sleep_habit_timemin > 0).all()
time_demo_work = session.query(m.Time.sex, m.Time.age_range, m.Time.region,
	m.Time.income, m.Time.education).filter(m.Time.work_habit_timemin > 0).all()

class TimeML:
	def __init__(self, timedemos, timedata):
		self.demos = timedemos
		self.time = timedata

# get all of the needed data from the db
time_exercise = session.query(m.Time.exercise_habit_timemin).all()
time_sleep = session.query(m.Time.sleep_habit_timemin).filter(m.Time.sleep_habit_timemin > 0).all()
time_work = session.query(m.Time.work_habit_timemin).filter(m.Time.work_habit_timemin > 0).all()

# create instances of the class
exercise_data = TimeML(time_demo_exercise, time_exercise)
sleep_data = TimeML(time_demo_sleep, time_sleep)
work_data = TimeML(time_demo_work, time_work)

## exercise data ##
# assign variables to lists and convert lists of
# tuples to numpy arrays -- feed in demo data and habit data from db
y = exercise_data.time
y = np.asarray([y[i][0] for i in range(0, len(y))])
X = np.asarray(exercise_data.demos)



print "********** Exercise **********"
print "shape X", X.shape
print "shape y", y.shape
print "est.fit(X, y)", est.fit(X,y)
print "est.coef_", est.coef_
guess = est.predict(user)
print "estimated hours of exercise", guess/60, "versus an average of 0.02 hours"



## sleep data ##
# assign variables to lists and convert lists of
# tuples to numpy arrays -- feed in demo data and habit data from db
y = sleep_data.time
y = np.asarray([y[i][0] for i in range(0, len(y))])
X = np.asarray(sleep_data.demos)



print "********** Sleep **********"
print "shape X", X.shape
print "shape y", y.shape
print "est.fit(X, y)", est.fit(X,y)
print "est.coef_", est.coef_
guess = est.predict(user)
print "estimated hours of sleep ", guess/60, "versus an average of 8.8 hours"


## work data ##
# assign variables to lists and convert lists of
# tuples to numpy arrays -- feed in demo data and habit data from db
y = work_data.time
y = np.asarray([y[i][0] for i in range(0, len(y))])
X = np.asarray(work_data.demos)



print "********** Work **********"
print "shape X", X.shape
print "shape y", y.shape
print "est.fit(X, y)", est.fit(X,y)
print "est.coef_", est.coef_
guess = est.predict(user)
print "estimated hours of work", guess/60, "versus an average of 7.2"


############## MONEY DATA ##############
# set up query for demo data from table and class
money_demos = session.query(m.Money.sex, m.Money.age_range, m.Money.region, m.Money.income, m.Money.education).all()

class MoneyML:
	def __init__(self, moneydemos, moneydata):
		self.demos = moneydemos
		self.time = moneydata

# get all of the needed data from the db
money_clothing = session.query(m.Money.spending_habit_clothes_dollars).all()
money_eatout = session.query(m.Money.spending_habit_eatout_dollars).all()

# create instances of the class feeding in our data
clothes_data = MoneyML(money_demos, money_clothing)
eatout_data = MoneyML(money_demos, money_eatout)


## clothes data ##
# assign variables to lists and convert lists of
# tuples to numpy arrays -- feed in demo data and habit data from db
y = clothes_data.time
y = np.asarray([y[i][0] for i in range(0, len(y))])
X = np.asarray(clothes_data.demos)



print "********** Clothing **********"
print "shape X", X.shape
print "shape y", y.shape
print "est.fit(X, y)", est.fit(X,y)
print "est.coef_", est.coef_
guess = est.predict(user)
print "estimated dollars spent on clothing $", guess, "versus an average of $0.94"

## eat out data ##
# assign variables to lists and convert lists of
# tuples to numpy arrays -- feed in demo data and habit data from db
y = eatout_data.time
y = np.asarray([y[i][0] for i in range(0, len(y))])
X = np.asarray(eatout_data.demos)



print "********** Eating Out **********"
print "shape X", X.shape
print "shape y", y.shape
print "est.fit(X, y)", est.fit(X,y)
print "est.coef_", est.coef_
guess = est.predict(user)
print "estimated dollars spent eating out $", guess, "versus an average of $9.37"














