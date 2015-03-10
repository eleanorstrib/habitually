
from __future__ import division
from flask import Flask, render_template, jsonify, send_file, make_response, request, g
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

# engine = create_engine("sqlite:///habit.db", echo=True)
# Session = sessionmaker(bind=engine)

app = Flask(__name__)
app.secret_key='\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'
habits_dict = {}
user_predict = {}

# @app.before_request  # Every time we get a request, first do this stuff.
# def before_request():
# 	pass

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
	usersess['user_data'] = data
	print usersess
	return "loading your predictions!"


@app.route('/predictions.json')
def user_predictions():
	"""
	Sends json data from ML algorithm to front end.
	"""
	user_dict = usersess['user_data']
	user_dict = ast.literal_eval(usersess['user_data'])
	user_dict = json.loads(user_dict)
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
	return "hi"

if __name__ == "__main__":
	app.run(debug=True)