from flask import Flask, render_template, redirect, request, flash, session
from flask_session import Session

from surveys import satisfaction_survey

app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'oh-so-secret'

Session(app)


@app.route('/')
def root():
    session["responses"] = []

    return render_template("base.html", survey=satisfaction_survey)


@app.route('/questions/<question_num>')
def question(question_num):

    if len(session["responses"]) != int(question_num):
        flash("You are trying to access an invalid question!")
        return redirect(f"/questions/{len(session['responses'])}")

    return render_template("question.html", survey=satisfaction_survey, question_number=question_num, question=satisfaction_survey.questions[int(question_num)])


@app.route('/questions/<question_num>', methods=["POST"])
def answer(question_num):
    session["responses"].append(request.form["answer"])
    if len(session["responses"]) == len(satisfaction_survey.questions):
        return redirect("/complete")
    else:
        return redirect(f"/questions/{int(question_num) + 1}")


@app.route('/complete')
def complete():
    return render_template("complete.html", responses=session["responses"])
