from flask import Flask, jsonify, request, abort
import pymysql

app = Flask(__name__)

# DB connection config
db_config = {
    'host': 'flask-mariadb.cc9822ak4zd7.us-east-1.rds.amazonaws.com',
    'user': 'flaskuser',
    'password': 'FlaskPass123!',
    'db': 'task_db',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db_connection():
    return pymysql.connect(**db_config)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()
    conn.close()
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    if not request.json or 'task' not in request.json:
        abort(400, description="Missing 'task' field")
    task_text = request.json['task']
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO tasks (task, done) VALUES (%s, %s)", (task_text, False))
        conn.commit()
        task_id = cursor.lastrowid
    conn.close()
    return jsonify({'id': task_id, 'task': task_text, 'done': False}), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    if not request.json:
        abort(400)
    task_text = request.json.get('task')
    done = request.json.get('done')

    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("UPDATE tasks SET task = %s, done = %s WHERE id = %s", (task_text, done, task_id))
        conn.commit()
    conn.close()
    return jsonify({'id': task_id, 'task': task_text, 'done': done})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        conn.commit()
    conn.close()
    return jsonify({"result": True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

