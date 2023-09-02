from flask import Flask, render_template, redirect, url_for, session, request
from functools import wraps
import json
from util import jinja_to_dict
import supabase as db


app = Flask(__name__)
app.secret_key = 'bla'
# app.jinja_env.globals.update(__builtins__.__dict__)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if 'user' not in session:
            return redirect(url_for('auth'))
        return f(*args, **kws)
    return decorated_function


@app.route("/")
@login_required
def home():
    return render_template('home.html')


@app.route("/auth", methods=['GET', 'POST'])
def auth():
    args = request.args.to_dict()
    referrer = args['referrer'] if 'referrer' in args else None
    is_signup = True if 'signup' in args else False
    if request.method == 'POST':
        # if sign in
        if request.form['session']:
            data = json.loads(request.form['session'])
            session['user'] = data['user']
            session['access_token'] = data['session']['access_token']
            return redirect(url_for('home'))
        # if sign up
        else:
            signup_user = request.form['userEmailSignup']
            referrer = request.form['referrer']
            print(db.process_referrer(referrer, signup_user))
            return redirect(url_for('confirm_email'))
    return render_template('auth.html', referrer=referrer, is_signup=is_signup)


@app.route("/confirm_email")
def confirm_email():
    return render_template('confirm_email.html')


@app.route("/clear_session")
def clear_session():
    session['user'] = None
    session.modified = True
    return ''


@app.route("/play")
@login_required
def play():
    videos = db.get_active_videos()
    return render_template('play.html', videos=videos)


@app.route("/refer")
def refer():
    auth_link = f'{request.host_url[:-1]}{url_for("auth")}'
    user_email = session['user']['email']
    referral_link = f'{auth_link}?signup&referrer={user_email}'
    return render_template('refer.html', referral_link=referral_link)

@app.route("/lottery")
def lottery():
    tickets = db.get_user_tickets(session['user']['id'])
    return render_template('lottery.html', tickets=tickets)


# Components

@app.route("/purchase_ticket", methods=['GET', 'POST'])
def purchase_ticket():
    ticket = {
        'num_1': request.form.get('ticket_num_1'),
        'num_2': request.form.get('ticket_num_2'),
        'num_3': request.form.get('ticket_num_3'),
        'num_4': request.form.get('ticket_num_4'),
        'num_5': request.form.get('ticket_num_5'),
        'num_powerball': request.form.get('ticket_num_powerball')
    }
    db.purchase_ticket(session['user']['id'], ticket)
    tickets = db.get_user_tickets(session['user']['id'])
    return render_template('components/tickets_tbody.html', tickets=tickets)


@app.route("/next_question")
def next_question():
    response = request.args.to_dict()
    video = jinja_to_dict(request.args['video'])
    if 'answer' in response and response['answer'] == response['selected_answer']:
        db.process_answer(session['user']['id'],
                          response['question_id'], video['id'])
    quiz_score = db.get_quiz_score(session['user']['id'], video['id'])
    total_score = db.get_user_score(session['user']['id'])
    question = session['questions'].pop(0) if session['questions'] else None
    session.modified = True
    return render_template('components/next_question.html', question=question, quiz_score=quiz_score, total_score=total_score, video=video)


@app.route("/quiz_modal")
def quiz_modal():
    video = jinja_to_dict(request.args['video'])
    questions = db.get_questions(video['id'], video['active_sequence'])
    quiz_score = db.get_quiz_score(session['user']['id'], video['id'])
    session['questions'] = questions
    return render_template('components/quiz_modal.html', video=video, quiz_score=quiz_score)


@app.route("/video_modal")
def video_modal():
    video = jinja_to_dict(request.args['video'])
    return render_template('components/video_modal.html', video=video)


@app.route("/get_user_score")
def get_user_score():
    score = db.get_user_score(session['user']['id'])
    return render_template('components/user_score.html', score=score)
    


@app.route("/debug")
def debug():
    return render_template('debug.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
