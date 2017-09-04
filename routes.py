# create a Flask application instance
from flask import Flask, redirect, render_template, request, url_for, make_response
from server import app
from csv_function import Survey,Question,Course
# define a route through the app.route decorator
users={'admin':'admin'}
session={}
@app.route("/", methods=["GET", "POST"])
def login():
    """for the first iteration"""
    return redirect(url_for("index"))
    """for the first iteration"""
    if request.method == "POST":
        if request.form['bt']=="submit":
            user_name_got= request.form['user_name']
            pass_word_got= request.form['password']
            resp = make_response(redirect(url_for("index")))
            resp.set_cookie('userID',user_name_got)
            resp.set_cookie('userPass',pass_word_got)
            print ("I just got",request.cookies.get('userID'))
            return resp
            
    return render_template("login.html")

@app.route("/checking")
def check_in():
    name=request.cookies.get('userID')
    password=request.cookies.get('userPass')
    if  users.get(name)is not None and users[name]== password:
        return True
    else : 
        return False



@app.route("/dash_board", methods=["GET", "POST"])
def index():
    #if not  check_in() : return redirect(url_for("login"))
    if request.method == "POST":
        if request.form['bt']=="course":
            return redirect(url_for("choose_course"))
    return render_template("index.html",add_question_link=url_for("add_question"),view_question_link=url_for("view_question_pool"))


@app.route("/add_question", methods=["GET", "POST"])
def add_question(): 
    #if not  check_in() : return redirect(url_for("login"))
    if request.method == "POST":
        if request.form['bt']=="submit":
            newQuestion=Question()
            question_get=request.form['question']
            option_get=request.form['option']
            newQuestion.take_in_qustion(question_get,option_get)
    return render_template("add_question.html")


@app.route("/error")
def error():
    print ("<h1>404!!!!!!!!!!!!!!!!!!!!!!</h1>")
    return "<h1>403</h1>"


@app.route("/courses", methods=["GET", "POST"])
def choose_course():
    #if not  check_in() : return redirect(url_for("login"))
    course_list=Course()
    if request.method=="POST":
        if request.form['bt']=="submit":
            choice=request.form["choice"]
            print(choice)
            return  redirect(url_for("create_survey",course_name=choice))
    return render_template("course_list.html",dash_board=url_for("index"),course=course_list.output_course())


@app.route("/create_survey/<course_name>",methods=["GET", "POST"])
def create_survey(course_name):
    #print(course_name)
    #if not  check_in() : return redirect(url_for("login"))
    all_question=Question()
    if request.method=="POST":
        if request.form["bt"]=="submit":
            question_selected=request.form.getlist("question")
            print (question_selected)
            newSurvey=Survey()
            newSurvey.make_survey(file_name=course_name,question_list=question_selected)
    return  render_template("create_survey.html",course=course_name,question_list=all_question.output_qurstion())

@app.route("/view_question_pool")
def view_question_pool():
    #if not  check_in() : return redirect(url_for("login"))
    question_list = Question()
    return  render_template("view_question_pool.html",all_question=question_list.output_qurstion(),add_question_link=url_for("add_question"))

# launch the integrated development web server
# and run the app on http://localhost:8085
#if __name__=="__main__":
#   app.run(debug=True,port=8085)
