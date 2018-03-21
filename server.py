from flask import Flask, render_template, request, redirect, url_for
import csv, os, time
from data_manager import *

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def list_questions():
    questions = read_questions()
    
    return render_template('questions.html', questions=questions)


@app.route('/question/<id>')
def display_question(id):
    answer = read_answers_by_question_id(id)
    return render_template("answers.html", answer=answer)


@app.route('/add-question')
@app.route('/add-question', methods=['POST'])
def question_form():
    if request.method == 'POST':
        current_questions = read_questions()
        new_row = dict()
        new_row.update({
            'title'         : request.form.get('title'),
            'message'       : request.form.get('message'),
            'id'            : len(current_questions),
            'submisson_time': format(time.time(), '.0f'),
            'view_number'   : 0,
            'vote_number'   : 0,
            'image'         : ''
        })
        write_questions(new_row)
        return redirect(url_for('list_questions'))
    
    return render_template('add-question.html', h1='Create question')


@app.route('/question/<int:question_id>/new-answer')
@app.route('/question/<int:question_id>/new-answer', methods=['POST'])
def answer_form(question_id):
    if request.method == 'POST':
        current_answers = read_answers()
        new_row = dict()
        new_row.update({
            'id'            : len(current_answers),
            'submisson_time': format(time.time(), '.0f'),
            'vote_number'   : 0,
            'question_id'   : question_id,
            'message'       : request.form.get('message'),
            'image'         : ''
        })
        write_answers(new_row)
        return redirect('/question/{}'.format(question_id))
    
    return render_template('new-answer.html', h1='Create answer')


if __name__ == '__main__':
    app.secret_key = "topsecret"
    answers = read_answers()
    app.run(debug=True, host='0.0.0.0', port=5000)
