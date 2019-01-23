from flask import Flask, request, render_template
from Class_for_courses import Course
from Request import Request
import json

app = Flask(__name__)
newRequest = Request()
# @app.route('/')
# def index():
# 	return 'This is the homepage'

@app.route('/courses', methods=['GET'])
def courses():
	CS125 = Course("CS125")
	CS225 = Course("CS225")
	courses = [CS125.course_name, CS225.course_name]
	return json.dumps(courses)

@app.route('/newcourse/', methods=['GET', 'POST'])
def newcourse():
	return request.data

@app.route('/')
def my_form():
    return render_template('year.html')

@app.route('/', methods=['POST'])
def the_year():
	newRequest.set_year(request.form['year'])
	newRequest.set_semester(request.form['semester'])
	newRequest.set_major(request.form['subject'])
	newRequest.get_courses()
	s = ""
	for i in newRequest.course_list:
		s = s + i + "\n"
	return s

@app.route('/inputs/', methods=['POST'])
def my_form_post():
	subject = request.form['text']
	newRequest = Request()
	newRequest.major = subject
	newRequest.get_courses()
	return newRequest.course_list
	# return render_template('courses.html')
    # processed_text = text.upper()
    # return processed_text

if __name__ == "__main__":
	app.run(debug = True)