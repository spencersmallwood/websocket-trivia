from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import random
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

# Question data (you can use a database for this)
questions = [
    {
        'question': 'What is the capital of France?',
        'choices': ['Paris', 'Berlin', 'Madrid', 'Rome'],
        'correct_answer': 'Paris',
    },
    {
        'question': 'Which planet is known as the Red Planet?',
        'choices': ['Earth', 'Mars', 'Jupiter', 'Venus'],
        'correct_answer': 'Mars',
    },
    # Add more questions here
]

current_question = questions[0]
responses = {choice: 0 for choice in questions[0]['choices']}  # Store response counts
rounds = 0
round_duration = 30  # Seconds per round

@socketio.on('connect')
def handle_connect():
    global current_question, rounds, responses
    rounds = 0
    responses = {choice: 0 for choice in questions[0]['choices']}
    current_question = questions[rounds]
    emit('question', {'question': current_question, 'round_duration': int(round_duration)})

# @socketio.on('connect')
# def handle_connect():
#     global current_question, rounds, responses
#     rounds = 0
#     responses = {choice: 0 for choice in questions[0]['choices']}
#     emit('question', {'question': questions[rounds], 'round_duration': int(round_duration)})  # Ensure round_duration is an integer

@socketio.on('answer')
def handle_answer(data):
    global current_question, rounds, responses

    if current_question:
        selected_answer = data['answer']
        if selected_answer == current_question['correct_answer']:
            response = 'correct'
        else:
            response = 'incorrect'
        responses[selected_answer] += 1

        # Send the response
        emit('answer', {'response': response}, broadcast=True, namespace='/')

if __name__ == '__main__':
    socketio.run(app, debug=True)
