from flask import Flask, render_template, redirect, url_for, session
from flask_session import Session  # Correct import for Flask-Session
from datetime import datetime, timedelta


TIMEOUT_DURATION_IN_MINUTES = 8

app = Flask(__name__)
app.secret_key = 'berlinfrogs'  # Replace with your secret key for sessions

app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


@app.route('/')
def home():
    # If session doesn't have start time, set it
    if 'start_time' not in session:
        session['start_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Get the current time and the stored start time
    start_time = datetime.strptime(session['start_time'], '%Y-%m-%d %H:%M:%S')
    current_time = datetime.now()

    # Calculate the elapsed time
    elapsed_time = current_time - start_time
    if elapsed_time > timedelta(minutes=TIMEOUT_DURATION_IN_MINUTES):
        return redirect(url_for('timeout'))

    return render_template('index.html')


@app.route('/timeout')
def timeout():
    return render_template('timeout.html')

@app.route('/reset')
def reset():
    # Reset the timer
    session.pop('start_time', None)  # Remove the start time from the session
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
