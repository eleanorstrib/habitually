
from __future__ import division
from flask import Flask, render_template, jsonify, send_file, make_response
from flask import session as usersess
from flask.ext.sqlalchemy import SQLAlchemy
import calculations as calc
import model_ind as m
import jinja2
import os
import json

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

@app.route('/')
def index():
	"""
	This function loads the first page and all of the survey data for graphing.
	"""
	# habits = calc.main(habits_dict)
	# usersess['habits'] = {}
	# usersess['habits'] = habits
	print usersess  # FIXME remove
	# define all of the variables needed on the page
	# avg_work_hours_all = usersess['habits']['work']['avg_work_hours_all']
	# print avg_work_hours_all
	
	return render_template('index.html')

@app.route("/allhabits.json")
def habits_data():
	"""Return JSON info about habits."""
	habits = calc.main(habits_dict)
	return jsonify(habits)


if __name__ == "__main__":
	app.run(debug=True)