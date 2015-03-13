
from __future__ import division
from flask import Flask, render_template, jsonify, send_file, make_response, request, redirect
from flask import session as usersess
from flask.ext.sqlalchemy import SQLAlchemy
import calculations as calc
import predict
import model_ind as m
import jinja2
import os
import json
import requests
import ast

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, scoped_session
import numpy as np



app = Flask(__name__)
app.secret_key='\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'
habits_dict = {}
user_predict = {}


@app.route('/')
def index():
	"""
	This function loads the first page and all of the survey data for graphing.
	"""
	return render_template('index.html')

@app.route('/allhabits.json')
def habits_data():
	"""
	Return JSON info on summary habit data.
	"""
	habits = calc.main(habits_dict)
	usersess['habits'] = habits
	print usersess  # FIXME remove
	return jsonify(habits)

@app.route('/userData.json', methods = ['POST'])
def user_data():
	"""
	Pull in JSON info about the user's demos.
	"""
	data = request.data # this is a string
	print data
	print type(data)

	usersess['user_data'] = data
	print usersess
	return redirect("/#/predictions")


@app.route('/userDataJS.json', methods = ['POST'])
def user_data_js():
	"""
	Pull in JSON info about the user's demos.
	"""
	data = request.form.to_dict(flat=True)
	print type(data)
	print data
	# data = json.loads(data)
	# print data
	# print type(data)
	usersess['user_data'] = data
	print usersess
	return "loading your predictions!"


@app.route('/predictions.json')
def user_predictions():
	"""
	Sends json data from ML algorithm to front end.
	"""
	user_dict = usersess['user_data']
	print "first version"
	print type(user_dict)
	if not isinstance(user_dict, dict):
		user_dict = ast.literal_eval(usersess['user_data'])
		user_dict = json.loads(user_dict)
	else:
		user_dict = {key:int(value) for key, value in user_dict.iteritems()}
	print "second version"
	print type(user_dict)
	print "*******"
	print user_dict
	print type(user_dict)
	
	sex = user_dict['queryGender']
	age_range = user_dict['queryAge']
	region = user_dict['queryRegion']
	income = user_dict['queryIncome']
	education = user_dict['queryEducation']
	
	user_raw = [sex, age_range, region, income, education]
	user = np.asarray(user_raw)
	print user_raw
	print user
	
	predictions = predict.main(user_predict, user_raw, user)
	print predictions

	return jsonify(predictions)

@app.route('/actualData.json', methods = ['POST'])
def send_actual_data():
	"""
	This function writes user data to the database for use in future predictions.
	"""
	#transform the actual data from the user via the form to a dict
	actual_data = request.data
	actual_data = ast.literal_eval(actual_data)
	
	#define the actual variables
	work_actual = actual_data['work']
	sleep_actual = actual_data['sleep']
	exercise_actual = actual_data['exercise']
	clothes_actual = actual_data['clothes']
	eatout_actual = actual_data['eatout']
	print type(work_actual)
	print type(sleep_actual)
	print type(exercise_actual)
	print type(clothes_actual)
	print type(eatout_actual)
	
	#transform the demo data from the session to form to a dict
	user_demo = ast.literal_eval(usersess['user_data'])
	user_demo = json.loads(user_demo)

	# define the demo variables
	age = user_demo['queryAge']
	sex = user_demo['queryGender']
	region = user_demo['queryRegion']
	income = user_demo['queryIncome']
	education = user_demo['queryEducation']
	print type(age)
	print type(sex)
	print type(region)
	print type(income)
	print type(education)

	# create query to add data to the Time table, add to session
	time_insert = m.Time(hhld_id='site', person_id='0', sex=sex, age_range=age, region=region, 
		education=education, income=income, work_habit_timemin=work_actual, sleep_habit_timemin=sleep_actual,
		exercise_habit_timemin=exercise_actual)
	print time_insert
	m.session.add(time_insert)

	# create query to add data to the Money table, add to session
	money_insert = m.Money(hhld_id='site', person_id='0', sex=sex, age_range=age, region=region,
		education=education, income=income, spending_habit_clothes_dollars=clothes_actual, 
		spending_habit_eatout_dollars=eatout_actual)
	print money_insert
	
	m.session.add(money_insert)
	
	m.session.commit()
	print "***** ADDITION TO THE DATABASE *****"
	print "New record has been committed!"
	print "ID for Money record:", money_insert.id, "ID for Time record:", time_insert.id
	print "*****" * 5
	return redirect("/#/thankyou")

if __name__ == "__main__":
	app.run(debug=True)