# the code in this file runs when we have the user data
from __future__ import division

import model_ind as m
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine("sqlite:///habit.db", echo=True)
Session = sessionmaker(bind=engine)

session = Session()

##### variables for over/under ######
exercise_target = 30
work_target = 456
sleep_target = 480

##### queries for all data from each table #####
time_query = session.query(m.Time)
time_all = time_query.all()

money_query = session.query(m.Money)
money_all = money_query.all()


##### demographic variables from form/FB ######
sex = 2
age_range = 2
education = 6
income = 3
region = 4



profile_count = time_query.filter(m.Time.sex == sex, m.Time.age_range == age_range, m.Time.education == education).count()
profile_list = time_query.filter(m.Time.sex == sex, m.Time.age_range == age_range, m.Time.education == education).all()


# ##### check probability of this profile in exercise #####
# ex_over_profile = session.query(m.Time.exercise_habit_timemin).filter(m.Time.sex == sex, m.Time.age_range == age_range, m.Time.education >= education, m.Time.region == region, m.Time.exercise_habit_timemin >= sleep_target)
# ex_under_profile = session.query(m.Time.exercise_habit_timemin).filter(m.Time.sex == sex, m.Time.age_range == age_range, m.Time.education >= education,  m.Time.region == region, m.Time.exercise_habit_timemin <= sleep_target)
# ex_over_profile_count = ex_over_profile.count()
# ex_over_profile_average = ex_under_profile.count()
# ex_under_profile_count = ex_under_profile.count()
# ex_under_profile_all = ex_under_profile.all()  #FIXME - sending back tuples
# ex_profile_count =  time_query.filter(m.Time.sex == sex, m.Time.age_range == age_range, m.Time.education >= education, m.Time.income == income).count()

# print "over ", ex_over_profile_count
# print "under ", ex_under_profile_count
# print "all ", ex_profile_count
# print "detail", ex_under_profile_all


##### check probability of this profile in work #####
wk_over_profile = session.query(m.Time.work_habit_timemin).filter(m.Time.sex == sex, m.Time.age_range == age_range, m.Time.education >= education, m.Time.region == region, m.Time.work_habit_timemin > work_target)
wk_under_profile = session.query(m.Time.work_habit_timemin).filter(m.Time.sex == sex, m.Time.age_range == age_range, m.Time.education >= education, m.Time.region == region, m.Time.work_habit_timemin < work_target)
wk_over_profile_count = wk_over_profile.count()
wk_under_profile_count = wk_under_profile.count()
wk_over_profile_all = wk_over_profile.all()
wk_under_profile_all = wk_over_profile.all()  #FIXME - sending back tuples

test = time_query.filter(m.Time.sex == sex, m.Time.age_range == age_range, m.Time.education == education, m.Time.work_habit_timemin > work_target).all()
test_list = [test[x].work_habit_timemin for x in range(0,len(test))]

time_list = [[time_query[x].exercise_habit_timemin, time_query[x].work_habit_timemin, time_query[x].work_habit_timemin] for x in range (0, 3)]

print time_list
# ##### check probability of this profile in sleep #####

# sl_over_profile = session.query(m.Time.sleep_habit_timemin).filter(m.Time.sex == sex, m.Time.age_range == age_range, m.Time.education >= education, m.Time.region == region, m.Time.sleep_habit_timemin > sleep_target)
# sl_under_profile = session.query(m.Time.sleep_habit_timemin).filter(m.Time.sex == sex, m.Time.age_range == age_range, m.Time.education >= education, m.Time.region == region, m.Time.sleep_habit_timemin < sleep_target)
# sl_over_profile_count = sl_over_profile.count()
# sl_under_profile_count = sl_under_profile.count()
# # sl_over_profile_all = sl_over_profile.all()
# # sl_under_profile_all = sl_over_profile.all()  #FIXME - sending back tuples

# # test = time_query.filter(m.Time.sex == sex, m.Time.age_range == age_range, m.Time.education == education, m.Time.sleep_habit_timemin > sleep_target).all()
# # test_list = [test[x].work_habit_timemin for x in range(0,len(test))]

# # time_list = [[time_query[x].exercise_habit_timemin, time_query[x].work_habit_timemin, time_query[x].work_habit_timemin] for x in range (0, 100)]

# print "profile count", sl_over_profile_count
# print "data", sl_under_profile_count
# print "over count", test
# print "test list", test_list

# print sl_over_profile_all

# sl_test = session.query(m.Time.sleep_habit_timemin).filter(sex == sex, age_range== age_range, education == education, region == region, income == income, m.Time.sleep_habit_timemin > sleep_target).all()

# print sl_test

# ##### query matching records based on demos ######
# time_vars = session.query(m.Time).filter(m.Time.sex == sex, m.Time.age_range == age_range, m.Time.education == education, m.Time.income == income, m.Time.region == region)
# time_count = time_vars.count()
# time_all = time_vars.all()

# # print time_all
# # print time_count

# ##### query for all records for exercise ####
# time_exercise_over30 = session.query(m.Time).filter(m.Time.exercise_habit_timemin > 30).all()
# time_count_all = session.query(m.Time).filter(m.Time.exercise_habit_timemin > 30).count()


# ##### gender probabilties #####
# ex_over30_fem = []

# for x in range(0, len(time_exercise_over30)):
# 	if time_exercise_over30[x].sex == 2:
# 		ex_over30_fem.append(time_exercise_over30[x].exercise_habit_timemin)

# prob_ex_over30_fem = float(len(ex_over30_fem)/time_count_all)
# prob_ex_over30_mal = float(1-prob_ex_over30_fem)

# ##### age probabilties #####
# ex_over30_age_1 =[]
# ex_over30_age_2 =[]
# ex_over30_age_3 =[]
# ex_over30_age_4 =[]
# ex_over30_age_5 =[]
# ex_over30_age_6 =[]
# ex_over30_age_7 =[]


# for x in range(0, time_count_all):
# 	if time_exercise_over30[x].age_range == 1:
# 		ex_over30_age_1.append(time_exercise_over30[x].exercise_habit_timemin)
# 	if time_exercise_over30[x].age_range == 2:
# 		ex_over30_age_2.append(time_exercise_over30[x].exercise_habit_timemin)
# 	if time_exercise_over30[x].age_range == 3:
# 		ex_over30_age_3.append(time_exercise_over30[x].exercise_habit_timemin)
# 	if time_exercise_over30[x].age_range == 4:
# 		ex_over30_age_4.append(time_exercise_over30[x].exercise_habit_timemin)
# 	if time_exercise_over30[x].age_range == 5:
# 		ex_over30_age_5.append(time_exercise_over30[x].exercise_habit_timemin)
# 	if time_exercise_over30[x].age_range == 6:
# 		ex_over30_age_6.append(time_exercise_over30[x].exercise_habit_timemin)
# 	if time_exercise_over30[x].age_range == 7:
# 		ex_over30_age_6.append(time_exercise_over30[x].exercise_habit_timemin)
# 	else:
# 		print "oops ", type(time_exercise_over30[x].age_range), time_exercise_over30[x].age_range
	

# prob_ex_over30_age1 = len(ex_over30_age_1)/time_count_all
# prob_ex_over30_age2 = len(ex_over30_age_2)/time_count_all
# prob_ex_over30_age3 = len(ex_over30_age_3)/time_count_all
# prob_ex_over30_age4 = len(ex_over30_age_4)/time_count_all
# prob_ex_over30_age5 = len(ex_over30_age_5)/time_count_all
# prob_ex_over30_age6 = len(ex_over30_age_6)/time_count_all
# prob_ex_over30_age7 = len(ex_over30_age_7)/time_count_all

# print ex_over30_age_1
# print ex_over30_age_2
# print ex_over30_age_3
# print ex_over30_age_4
# print ex_over30_age_5
# print ex_over30_age_6
# print ex_over30_age_7

# print prob_ex_over30_age1
# print prob_ex_over30_age2
# print prob_ex_over30_age3
# print prob_ex_over30_age4
# print prob_ex_over30_age5
# print prob_ex_over30_age6
# print prob_ex_over30_age7








