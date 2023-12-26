from calendar import weekday
from os import name
from turtle import st
from click import option
from flask import Blueprint, redirect, render_template, request, session, g, url_for
from flask_login import current_user
from sqlalchemy import desc
from sqlalchemy.sql.expression import func

from app.extenstions import db
from app.utils import date_converter
from app.utils.weather_api_handler import WeatherApiHandler
from app.forms import QuestionForm
from app.models import Questions, User, user_questions

main = Blueprint('main', __name__)

def get_new_question_for_user(user_id):
    subq = db.session.query(user_questions.c.question_id).filter(user_questions.c.user_id == user_id).subquery()
    new_question = Questions.query.filter(~Questions.id.in_(subq)).order_by(db.func.random()).first()
    return new_question

def record_answer(user_id, question_id):
    new_entry = user_questions.insert().values(user_id=user_id, question_id=question_id)
    db.session.execute(new_entry)
    db.session.commit()

@main.before_request
def before_request():
    if not current_user.is_authenticated:
        return

    if request.endpoint != 'main.quiz' and request.endpoint != 'main.score':
        session['question_number'] = 1
        session['score_in_current_quiz'] = 0

    # unmark all asked questions in this session
    # correctly answered questions are already marked in database
    if request.endpoint != 'main.quiz':
        clear_asked_questions()
        session['questions_left'] = count_quesions_left(get_current_user())

def clear_asked_questions():
    for question in Questions.query:
        session[str(question.id)] = 0

@main.route('/', methods=['GET', 'POST'])
def index():
    weekday_name = date_converter.get_weekday_name()
    today_date = date_converter.get_today_date()

    if request.method == 'POST':
        city_name = request.form['city_name']

        if city_name == '':
            return render_template(
                'home.html',
                today_date = today_date,
                day_of_the_week = weekday_name
            )

        weather_api_handler = WeatherApiHandler()

        if not weather_api_handler.is_ok(city_name):
            return render_template(
                'home.html',
                today_date = today_date,
                day_of_the_week = weekday_name,
                error_message = 'Nieprawidłowa nazwa miasta. Używaj tylko litery alfabetu łacińskiego'
        )

        weather_forecast = weather_api_handler.get_weather_forecast(city_name)
        current_temperature = weather_api_handler.get_current_temperature(city_name)

        return render_template(
            'home.html', 
            current_temperature = current_temperature,
            today_weather = weather_forecast[0],
            tomorrow_weather = weather_forecast[1],
            day_after_weather = weather_forecast[2],
            today_date = today_date,
            day_of_the_week = weekday_name
        )

    return render_template(
                'home.html',
                today_date = today_date,
                day_of_the_week = weekday_name
            )

@main.route('/record_table')
def record_table():
    users = User.query.with_entities(User.nickname, User.main_score).order_by(desc(User.main_score)).all()

    return render_template('record_table.html', usernames_scores=users)

@main.route('/score')
def score():
    score = session['score_in_current_quiz']
    session['score_in_current_quiz'] = 0

    is_any_questions_left = count_quesions_left(get_current_user()) != 0

    return render_template('score.html', current_score = score, is_any_questions_left=is_any_questions_left)



@main.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    user = get_current_user()

    if 'score_in_current_quiz' not in session:
        session['score_in_current_quiz'] = 0
    
    if 'questions_left' not in session:
        session['questios_left'] = count_quesions_left(user)

    question_number = session.get('question_number', 1)

    quiz_questions_to_answer = 5
    if question_number > quiz_questions_to_answer:
        session['question_number'] = 1
        return redirect(url_for('main.score'))

    if session['questions_left'] == 0:
        clear_asked_questions()

    question = None
    if 'current_question_id' in session:
        question = Questions.query.filter_by(id=session['current_question_id']).first()
    else:
        question = get_new_question_for_user(user.id)

        if not question:
            return redirect(url_for('main.score'))

        while str(question.id) in session and session[str(question.id)] == 1:
            question = get_new_question_for_user(user.id)

        # mark question as asked for this quiz
        session[str(question.id)] = 1
        session['questions_left'] -= 1
        session['current_question_id'] = question.id    

    form = QuestionForm()
    
    if request.method == 'POST':
        option = request.form['options']
        if option == question.answer:
            session['score_in_current_quiz'] += 1
            user.main_score += 1
            db.session.commit()

            record_answer(user.id, question.id)
        
        session['question_number'] = question_number + 1
        session.pop('current_question_id')
        session.modified = True

        return redirect(url_for('main.quiz'))

    form.options.choices = [
        question.first_option, 
        question.second_option, 
        question.third_option, 
        question.fourth_option
    ]

    return render_template(
        'quiz.html', 
        form = form, 
        question = question.question,
        score = user.main_score,
        question_number = question_number,
        sum_question = quiz_questions_to_answer
    )

def get_current_user():
    return User.query.filter_by(id=session['user_id']).first()

def count_quesions_left(user):
    return Questions.query.count() - user.main_score

@main.route('/create_question', methods=['GET', 'POST'])
def create_question():
    if request.method == 'POST':
        question = request.form['question']

        options = []
        options.append(request.form['option1'])
        options.append(request.form['option2'])
        options.append(request.form['option3'])
        options.append(request.form['option4'])

        correct_option = options[int(request.form['correct_option_index'])]

        quiz_question = Questions(
            question = question,
            first_option = options[0],
            second_option = options[1],
            third_option = options[2],
            fourth_option = options[3],
            answer = correct_option
        )

        db.session.add(quiz_question)
        db.session.commit()

    return render_template('create_question.html')