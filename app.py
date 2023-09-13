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
    {
        'question': 'Who wrote the play "Romeo and Juliet"?',
        'choices': ['Charles Dickens', 'William Shakespeare', 'Jane Austen', 'Mark Twain'],
        'correct_answer': 'William Shakespeare',
    },
    {
        'question': 'What is the largest planet in our solar system?',
        'choices': ['Earth', 'Mars', 'Saturn', 'Jupiter'],
        'correct_answer': 'Jupiter',
    },
    {
        'question': 'In which year did Christopher Columbus first arrive in the Americas?',
        'choices': ['1492', '1620', '1776', '1812'],
        'correct_answer': '1492',
    },
    {
        'question': 'Who painted the Mona Lisa?',
        'choices': ['Vincent van Gogh', 'Leonardo da Vinci', 'Pablo Picasso', 'Michelangelo'],
        'correct_answer': 'Leonardo da Vinci',
    },
    {
        'question': 'What is the chemical symbol for gold?',
        'choices': ['Au', 'Ag', 'Fe', 'Hg'],
        'correct_answer': 'Au',
    },
    {
        'question': 'Which planet is known as the "Morning Star" or "Evening Star" and is often the brightest object in the night sky?',
        'choices': ['Venus', 'Mercury', 'Mars', 'Jupiter'],
        'correct_answer': 'Venus',
    },
    {
        'question': 'What is the largest mammal in the world?',
        'choices': ['Elephant', 'Giraffe', 'Blue Whale', 'Hippopotamus'],
        'correct_answer': 'Blue Whale',
    },
    {
        'question': 'Which country is known as the Land of the Rising Sun?',
        'choices': ['China', 'South Korea', 'Japan', 'Vietnam'],
        'correct_answer': 'Japan',
    },
]
current_question_index = 0
responses = {choice: 0 for choice in questions[0]['choices']}  # Store response counts
rounds = 1
round_duration = 30  # Seconds per round

@socketio.on('connect')
def handle_connect():
    global current_question_index, rounds, responses
    rounds = 0
    responses = {choice: 0 for choice in questions[0]['choices']}
    send_question(current_question_index)

@socketio.on('answer')
def handle_answer(data):
    global current_question_index, rounds, responses

    if current_question_index < len(questions):
        selected_answer = data['answer']
        correct_answer = questions[current_question_index]['correct_answer']

        if selected_answer == correct_answer:
            response = 'correct'
            current_question_index += 1  # Move to the next question upon a correct answer
        else:
            response = 'incorrect'

        # responses[selected_answer] += 1

        if current_question_index < len(questions):
            send_question(current_question_index)
        else:
            emit('results', responses, namespace='/')

def send_question(question_index):
    question_data = questions[question_index]
    question_data['round_duration'] = int(round_duration)
    emit('question', question_data, namespace='/')

if __name__ == '__main__':
    socketio.run(app, debug=True)
