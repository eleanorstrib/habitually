# the code in this file gets data about the entire population
from __future__ import division

import model_ind as m
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, scoped_session
import numpy

engine = create_engine("sqlite:///habit.db", echo=True)
Session = sessionmaker(bind=engine)

session = Session()

##### variables for target ######
exercise_target = 30
work_target = 456
sleep_target = 480

##### queries for all data from each table #####
time_query = session.query(m.Time)
time_all = time_query.all()

money_query = session.query(m.Money)
money_all = money_query.all()

# dictionary that will hold results from all queries
habits_dict = {}

def calc_work_stats():
	"""
	This function calculates all of the summary stats for respondents US wide with primary jobs
	using data from the ATUS study.  Removed zero values
	"""
	habits_dict['work'] = {}
	#### work overall -- whole population #####
	overall_work_minutes= session.query(m.Time.work_habit_timemin).all()
	overall_work_minutes = [overall_work_minutes[i][0] for i in range(0, len(overall_work_minutes))]
	overall_work_minutes = filter(lambda a: a !=0, overall_work_minutes) # remove zero values
	#summary work stats #
	habits_dict['work']['med_work_hours_all'] = numpy.median(overall_work_minutes)/60
	habits_dict['work']['avg_work_hours_all'] = (sum(overall_work_minutes)/len(overall_work_minutes))/60
	habits_dict['work']['min_work_hours_all']= min(overall_work_minutes)/60
	habits_dict['work']['max_work_hours_all'] = max(overall_work_minutes)/60
 
	return habits_dict

def calc_sleep_stats():
	"""
	This function calculates all of the summary stats for respondents US wide with primary jobs
	using data from the ATUS study.  Removed zero values.
	"""
	habits_dict['sleep'] = {}
	#### sleep overall -- whole population #####
	overall_sleep_minutes= session.query(m.Time.sleep_habit_timemin).all()
	overall_sleep_minutes = [overall_sleep_minutes[i][0] for i in range(0, len(overall_sleep_minutes))]
	overall_sleep_minutes = filter(lambda a: a !=0, overall_sleep_minutes) # remove zero values
	#summary sleep stats #
	habits_dict['sleep']['med_sleep_hours_all'] = numpy.median(overall_sleep_minutes)/60
	habits_dict['sleep']['avg_sleep_hours_all'] = (sum(overall_sleep_minutes)/len(overall_sleep_minutes))/60
	habits_dict['sleep']['min_sleep_hours_all'] = min(overall_sleep_minutes)/60
	habits_dict['sleep']['max_sleep_hours_all'] = max(overall_sleep_minutes)/60

	return habits_dict


def calc_exercise_stats():
	"""
	This function calculates all of the summary stats for respondents US wide 
	using data from the ATUS study.  Zero values NOT removed.
	"""
	habits_dict['exercise'] = {}
	#### exercise overall -- whole population #####
	overall_ex_minutes= session.query(m.Time.exercise_habit_timemin).all()
	overall_ex_minutes = [overall_ex_minutes[i][0] for i in range(0, len(overall_ex_minutes))]
	#summary exercise stats #
	habits_dict['exercise']['med_ex_hours_all'] = numpy.median(overall_ex_minutes)/60
	habits_dict['exercise']['avg_ex_hours_all'] = (sum(overall_ex_minutes)/len(overall_ex_minutes))/60
	habits_dict['exercise']['min_ex_hours_all'] = min(overall_ex_minutes)/60
	habits_dict['exercise']['max_ex_hours_all'] = max(overall_ex_minutes)/60

	return habits_dict


def calc_clothes_spend_stats():
	"""
	This function calculates all of the summary stats for respondents US wide 
	as a quarterly number using data from the CEX study on all clothing for the hhld.
	Zero values NOT removed.
	"""
	habits_dict['clothing'] = {}
	#### clothes spending overall -- whole population #####
	overall_clothes_spending= session.query(m.Money.spending_habit_clothes_dollars).all()
	overall_clothes_spending = [overall_clothes_spending[i][0] for i in range(0, len(overall_clothes_spending))]
	#summary clothing stats #
	habits_dict['clothing']['med_clothes_spending_all'] = numpy.median(overall_clothes_spending)
	habits_dict['clothing']['avg_clothes_spending_all'] = (sum(overall_clothes_spending)/len(overall_clothes_spending))/60
	habits_dict['clothing']['min_clothes_spending_all'] = min(overall_clothes_spending)
	habits_dict['clothing']['max_clothes_spending_all'] = max(overall_clothes_spending)

	return habits_dict
 

def calc_eatout_spend_stats():
	"""
	This function calculates all of the summary stats for respondents US wide 
	as a quarterly number using data from the CEX study on all food and alcohol 
	purchased outside of a grocery store for the hhld.
	Zero values NOT removed.
	"""
	habits_dict['eatout'] = {}
	#### Eat out spending averages -- whole population #####
	overall_eatout_spending= session.query(m.Money.spending_habit_eatout_dollars).all()
	overall_eatout_spending = [overall_eatout_spending[i][0] for i in range(0, len(overall_eatout_spending))]
	#summary clothing stats #
	habits_dict['eatout']['med_eatout_spending_all'] = numpy.median(overall_eatout_spending)
	habits_dict['eatout']['avg_eatout_spending_all'] = (sum(overall_eatout_spending)/len(overall_eatout_spending))/60
	habits_dict['eatout']['min_eatout_spending_all'] = min(overall_eatout_spending)
	habits_dict['eatout']['max_eatout_spending_all'] = max(overall_eatout_spending)

	return habits_dict


def get_habits_dict():
	calc_work_stats()
	calc_sleep_stats()
	calc_exercise_stats()
	calc_clothes_spend_stats()
	calc_eatout_spend_stats()
	return habits_dict
