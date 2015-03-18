habitually
===============

habitually is an app that uses your demographic profile to predict your habits.  It was built in my last four weeks of the Software Engineering Fellowship at [Hackbright Academy](http://www.hackbrightacademy.com) in Winter 2015.

Based on tens of thousands of datapoints from two government surveys and data entered by users, habitually predicts time spent working, sleeping and exercising and discretionary spending on clothing and eating out based on five demographic variables: gender, age range, region (US only), education, and income.

The app has a heavy-duty backend which includes machine learning and statistical analysis libraries for Python piping into a Flask server and fronted with a clean, fast user experience made possible with AngularJS, JavaScript, Bootstrap, HTML and CSS.

![image](https://github.com/eleanorstrib/habitually/blob/master/static/img/stack.png)

The App
----------
On the homepage, a SQLAlchemy query in the Python back end pulls summary stats from the full dataset and they are added, via Flask, JSON, JavaScipt and AngularJS, to the image carousel.  The front end also uses the Bootstrap library.

![image](https://github.com/eleanorstrib/habitually/blob/master/static/img/homepage.png)
When the user clicks on "get started", a page is shown with two options for providing demographic data on which to base the predictions.

![image](https://github.com/eleanorstrib/habitually/blob/master/static/img/demopage.png)
###### Facebook login (FB_login.js)
This option uses the Facebook SDK to ask the user for permission to get some of their demographic data from the social networking site, which is returned as a JSON object.  JavaScript code then pulls this object apart and converts the values into variables that can be used in the Python script to generate predictions.  This is sometimes straightforward, but in some cases required examination of several variables to make an educated guess about what the right value actually is.  For example, because Facebook does not collect income information, income is extrapolated from government data on salary and wage increases and education data.

###### Form (getstarted.html, habitually_ngmain.js)
The form is built in and validated with AngularJS, and passes the variables needed to generate the predictions to the backend on submit.

When the user clicks either "Analyze me!" button, the query variables are added to the Flask session and passed to a Python file (predictions.py) that uses numpy and scikit-learn libraries with SQLAlchemy queries to get the data needed, try to fit the data for people with the same profile to a linear regression model, then predict how much time or money the user spends on each activity.

![image](https://github.com/eleanorstrib/habitually/blob/master/static/img/predictionspage.png)
In the final step, the predications are passed back to the front end via JSON and Flask, and the user sees the predictions in the front end and is able to input actual values then write them to the database as a new record, complete with their demographic variables from the Flask session.

This is an overview of the flow and how each part of the stack plays into it.
![image](https://github.com/eleanorstrib/habitually/blob/master/static/img/flow.jpg)

The Data
----------
The base data for habitually comes from two large-scale studies by the Department of Labor's Bureau of Labor Statistics: the [American Time Use Study](http://www.bls.gov/tus/home.htm) and the [Consumer Expenditure Survey](http://www.bls.gov/cex/pumdhome.htm).  Here's how it all came together in four weeks, in four steps.


STEP 1: Understanding and Cleaning the Data
The first challenge was to sort through both studies, not only to find the demo and habit variables that were relevant, but to locate them in the dozens of files available for download.   It took about four days to look through codebooks, identify the right variables to use, find them in the relevant file, figure out how to summarize and collapse the demographic variables (which unfortunately were not always the same even though the same organization runs both surveys) into groups that were big enough to analyze, link multiple survey files together on simplified demo variables, and write the code to create and seed the SQL database.
![image](https://github.com/eleanorstrib/habitually/blob/master/static/img/rawdata.png)

STEP 2: Verifying the data
The next step was to make sure the data in the SQL database looked right.  It took about a day and a half to verify that the demo variables had been collapsed correctly and that every record in the database had habit data associated with it.  When it was clear, after testing with a couple of dozen SQLite3 queries that the data looked clean, it was time to use the machine learning algorithm to get predictions.
![image](https://github.com/eleanorstrib/habitually/blob/master/static/img/sqlite.png)

STEP 3: Selecting and running machine learning algorithms
Using the scikit-learn library for Python, the next step was to select a model and run the data through it.  A [linear regression model](http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html) was used for this first iteration of the predictions.  The very first iterations of this revealed that the spending data was likely being skewed by zero values that probably should have been Nulls or blanks, as well as some pretty extreme outliers. 
The data was analyzed for this project using all five demographic variables (gender, age range, region (US only), income and education) as an array of independent variables.  In a future iteration, I will look at how combinations of a subset of these variables influence the predictions, and may adjust the data gathering and prediction calculations depending on the results.
![image](https://github.com/eleanorstrib/habitually/blob/master/static/img/machinelearning.png)

STEP 4: Piping output to the front end
The final step was to pipe the results of the Python script that derives the predictions to the front end.  This was done using Flask and JSON, for the result seen in the screenshot.  Although there are thousands of records used to derive each predictions (there are about 16K total), more data might yield more accurate predictions.  To build the data set, users can add their actual habit data to the database.
![image](https://github.com/eleanorstrib/habitually/blob/master/static/img/predictionspage.png)