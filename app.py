from flask import Flask, jsonify, request, abort
import json
import os

app = Flask(__name__)
TASKS_FILE = 'tasks.json'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flaskuser:FlaskPass123!@flask-mariadb.cc9822ak4zd7.us-east-1.rds.amazonaws.com:3306/your_database_name'

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r') as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = load_tasks()
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    if not request.json or 'task' not in request.json:
        abort(400, description="Missing 'task' field")
    tasks = load_tasks()
    new_task = {
        "id": max([t["id"] for t in tasks], default=0) + 1,
        "task": request.json['task'],
        "done": False
    }
    tasks.append(new_task)
    save_tasks(tasks)
    return jsonify(new_task), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    tasks = load_tasks()
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task is None:
        abort(404, description="Task not found")
    if not request.json:
        abort(400)
    task['task'] = request.json.get('task', task['task'])
    task['done'] = request.json.get('done', task['done'])
    save_tasks(tasks)
    return jsonify(task)

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    tasks = load_tasks()
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task is None:
        abort(404, description="Task not found")
    tasks = [t for t in tasks if t['id'] != task_id]
    save_tasks(tasks)
    return jsonify({"result": True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

