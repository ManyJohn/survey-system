from flask import * 
from server import app
from csv_function import Survey, QuestionReaderCSV, QuestionWriterCSV, Question

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
        choices = []
        # Append all choices to list
        for i in range(no_choices):
            choices.append(request.form["choice" + str(i)])
        # Instantiate Question object and pass it to the writer
        QuestionWriterCSV.write(Question(question, choices))

    # Read questions from reader and pass the list of question objects to the 
    #   Jinja2 template
    question_list = QuestionReaderCSV.read()
    return render_template("questions.html", questions=question_list)

@app.route("/surveys")
def surveys():
    # Ensure cookies contain correct credentials
    username = request.cookies.get("username")
    password = request.cookies.get("password")
    if not (username in users and users[username] == password):
        return redirect(url_for("login"))

    return render_template("surveys.html")

@app.route("/error")
def error():
    print ("<h1>404!!!!!!!!!!!!!!!!!!!!!!</h1>")
    return "<h1>403</h1>"


@app.route("/courses", methods=["GET", "POST"])
def choose_course():
    #if not  check_in() : return redirect(url_for("login"))
    if request.method=="POST":
        if request.form['bt']=="submit":
            choice=request.form["choice"]
            print(choice)
            return  redirect(url_for("create_survey",course_name=choice))
    return render_template("course_list.html",dash_board=url_for("index"),course=Course.output_course())


@app.route("/create_survey/<course_name>",methods=["GET", "POST"])
def create_survey(course_name):
    #print(course_name)
    #if not  check_in() : return redirect(url_for("login"))
    
    if request.method=="POST":
        if request.form["bt"]=="submit":
            question_selected=request.form.getlist("question")
            print (question_selected)
            newSurvey=Survey(file_name=course_name,question_list=question_selected)
            newSurvey.make_survey()
    return  render_template("create_survey.html",course=course_name,question_list=Question.output_qurstion())

@app.route("/view_question_pool")
def view_question_pool():
    #if not  check_in() : return redirect(url_for("login"))
    return  render_template("view_question_pool.html",all_question=Question.output_qurstion(),add_question_link=url_for("add_question"))

# launch the integrated development web server
# and run the app on http://localhost:8085
#if __name__=="__main__":
#   app.run(debug=True,port=8085)
