from flask import * 
from server import app
from survey_system import *

# Credentials for Iteration 1
users={'admin':'admin'}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # If the submitted credentials are correct, redirect to dashboard
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            resp = make_response(redirect(url_for("dashboard")))
            resp.set_cookie('username', username)
            resp.set_cookie('password', password)
            return resp
        else:
            return render_template("login.html", incorrect_creds=True)
    return render_template("login.html", incorrect_creds=False)

@app.route("/dashboard")
def dashboard():
    # Ensure cookies contain correct credentials
    username = request.cookies.get("username")
    password = request.cookies.get("password")
    if not (username in users and users[username] == password):
        return redirect(url_for("login"))

    return render_template("dashboard.html", questions_link=
            url_for("questions"), surveys_link=url_for("surveys"))

@app.route("/questions", methods=["GET", "POST"])
def questions():
    # Ensure cookies contain correct credentials
    username = request.cookies.get("username")
    password = request.cookies.get("password")
    if not (username in users and users[username] == password):
        return redirect(url_for("login"))

    if request.method == "POST":
        question = request.form["question"]
        no_choices = int(request.form["no_choices"])
        choices = [request.form["choice" + str(i)] for i in range(no_choices)]
        # Instantiate Question object and pass it to the writer
        CSVQuestionRW.write(Question(question, choices))

    # Read questions from reader and pass the list of Question objects to the 
    #   Jinja2 template
    question_list = CSVQuestionRW.read_all()
    return render_template("questions.html", questions=question_list)

@app.route("/surveys", methods=["GET", "POST"])
def surveys():
    # Ensure cookies contain correct credentials
    username = request.cookies.get("username")
    password = request.cookies.get("password")
    if not (username in users and users[username] == password):
        return redirect(url_for("login"))

    if request.method == "POST":
        course_offering = request.form["course"]
        question_ids = request.form.getlist("question_id")
        # Instantiate Survey object and pass it to the writer
        CSVSurveyRW.write(Survey(course_offering, question_ids))


    # Read surveys, questions, and unsurveyed course offerings from the readers 
    #   and pass the lists to the Jinja2 template
    survey_list = CSVSurveyRW.read_all()
    course_offering_list = CSVCourseOfferingsRW.read_unsurveyed()
    questions_list = CSVQuestionRW.read_all()
    return render_template("surveys.html", surveys=survey_list, 
            questions=questions_list, courses=course_offering_list)

@app.route("/fill_survey/<survey_name>", methods=["GET", "POST"])
def fill_survey(survey_name):
    survey_name = survey_name.replace("-", " ")
    if request.method == "POST":
        results = request.form.to_dict()
        CSVSurveyResponseRW.write(SurveyResponse(survey_name, results))        

    survey = CSVSurveyRW.read(survey_name)
    question_list = [CSVQuestionRW.read(q) for q in survey.question_ids]
    return render_template("fill_survey.html", survey_name=survey_name,
            questions=question_list)

