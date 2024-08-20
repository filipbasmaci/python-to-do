import csv
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

CSV_FILE = 'todos.csv'

def load_todos():
    todos = []
    try:
        with open(CSV_FILE, mode='r') as file:
            reader = csv.reader(file)
            todos = [row[0] for row in reader]
    except FileNotFoundError:
        pass
    return todos

def save_todos(todos):
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        for todo in todos:
            writer.writerow([todo])


todos = load_todos()

@app.route('/')
def index():
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    todo = request.form.get('todo')
    if todo:
        todos.append(todo)
        save_todos(todos)
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    if 0 <= todo_id < len(todos):
        todos.pop(todo_id)
        save_todos(todos)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
