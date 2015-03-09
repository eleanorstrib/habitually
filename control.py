
from __future__ import division
from flask import Flask, render_template, jsonify, send_file, make_response, request
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
import numpy

# engine = create_engine("sqlite:///habit.db", echo=True)
# Session = sessionmaker(bind=engine)

app = Flask(__name__)
app.secret_key='\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'
habits_dict = {}
user_predict = {}

@app.route('/')
def index():
	"""
	This function loads the first page and all of the survey data for graphing.
	"""
	print usersess  # FIXME remove
	return render_template('index.html')

@app.route('/allhabits.json')
def habits_data():
	"""
	Return JSON info on summary habit data.
	"""
	habits = calc.main(habits_dict)
	return jsonify(habits)

@app.route('/userData.json', methods = ['POST'])
def user_data():
	"""
	Pull in JSON info about the user's demos.
	"""
	data = request.data # this is a string
	data = ast.literal_eval(data)
	user_data = json.loads(data) #converted to dict
	name = user_data['firstName']
	age_range = user_data['queryAge']
	gender = user_data['queryGender']
	region = user_data['queryRegion']
	education = user_data['queryEducation']
	income = user_data['queryIncome']

	print name, age_range, gender, region, education, income
	print type(age_range)

	return data

@app.route('/predictions.json')
def user_predictions():
	"""
	Sends json data from ML algorithm to front end.
	"""
	predictions = predict.main(user_predict)
	print predictions
	return jsonify(predictions)

if __name__ == "__main__":
	app.run(debug=True)