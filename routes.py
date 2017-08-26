# create a Flask application instance
from flask import Flask, redirect, render_template, request, url_for
from server import app
from csv_function import *
# define a route through the app.route decorator
session={}
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if request.form['bt']=="course":
            return redirect(url_for("choose_course"))
    return render_template("index.html",add_question_link=url_for("add_question"),view_question_link=url_for("view_question_pool"))


@app.route("/add_question", methods=["GET", "POST"])
def add_question(): 
    if request.method == "POST":
        if request.form['bt']=="submit":
            question_get=request.form['question']
            option_get=request.form['option']
            take_in_qustion(question_get,option_get)
    return render_template("add_question.html")


@app.route("/error")
def error():
    print ("<h1>404!!!!!!!!!!!!!!!!!!!!!!</h1>")
    return "<h1>403</h1>"


@app.route("/courses", methods=["GET", "POST"])
def choose_course():
    course_list=output_course()
    if request.method=="POST":
        if request.form['bt']=="submit":
            choice=request.form["choice"]
            print(choice)
            return  redirect(url_for("create_survey",course_name=choice))
    return render_template("course_list.html",course=course_list)


@app.route("/create_survey/<course_name>",methods=["GET", "POST"])
def create_survey(course_name):
    #print(course_name)
    all_question=output_qurstion()
    if request.method=="POST":
        if request.form["bt"]=="submit":
            question_selected=request.form.getlist("question")
            print (question_selected)
            make_survey(file_name=course_name,question_list=question_selected)
    return  render_template("create_survey.html",course=course_name,question_list=all_question)

@app.route("/view_question_pool")
def view_question_pool():
    question_list = output_qurstion()
    return  render_template("view_question_pool.html",all_question=question_list,add_question_link=url_for("add_question"))

# launch the integrated development web server
# and run the app on http://localhost:8085
#if __name__=="__main__":
#   app.run(debug=True,port=8085)
