from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample in-memory database
tasks = [
    {
        'id': 1,
        'title': 'Learn Flask',
        'description': 'Study Flask to create web applications',
        'done': False
    },
    {
        'id': 2,
        'title': 'Learn REST',
        'description': 'Understand RESTful APIs',
        'done': False
    }
]

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify({'task': task})

@app.route('/tasks', methods=['POST'])
def create_task():
    if not request.json or 'title' not in request.json:
        return jsonify({'error': 'The title is missing'}), 400

    task = {
        'id': len(tasks) + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404

    if 'title' in request.json:
        task['title'] = request.json['title']
    if 'description' in request.json:
        task['description'] = request.json['description']
    if 'done' in request.json:
        task['done'] = request.json['done']

    return jsonify({'task': task})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True)
