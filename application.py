import database
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask_httpauth import HTTPBasicAuth


app = Flask(__name__, static_url_path='')
auth = HTTPBasicAuth()
CONNECTION = database.connect()


@auth.get_password
def get_password(username):
    for credential in database.get_user_credentials(CONNECTION):
        if credential[0] == username:
            return credential[1]
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)
    # return 403 instead of 401 to prevent browsers from displaying
    # the default auth dialog


@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(405)
def not_allowed(error):
    return make_response(jsonify({'error': 'Method not allowed'}), 405)


def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'],
                                      _external=True)
        else:
            new_task[field] = task[field]
    return new_task


@app.route('/tasks', methods=['GET'])
@auth.login_required
def get_tasks():
    return jsonify({'tasks': list(map(make_public_task,
                                      database.get_tasks(CONNECTION)))})


@app.route('/tasks/<int:task_id>', methods=['GET'])
@auth.login_required
def get_task(task_id):
    task = database.get_task(CONNECTION, task_id)
    if len(task) == 0:
        abort(404)
    return jsonify({'task': make_public_task(task[0])})


@app.route('/tasks', methods=['POST'])
@auth.login_required
def create_task():
    if not request.json or 'title' not in request.json:
        abort(400)
    task = {
        'id': max([int(task.get('id')) for task in
                   database.get_tasks(CONNECTION)]) + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'status': request.json.get('status', 'False')
    }
    database.create_task(CONNECTION, task)
    return jsonify({'task': make_public_task(task)}), 201


@app.route('/tasks/<int:task_id>', methods=['PUT'])
@auth.login_required
def update_task(task_id):
    task = database.get_task(CONNECTION, task_id)
    print(task)
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and not isinstance(request.json['title'], str):
        abort(400)
    if 'description' in request.json and \
            not isinstance(request.json['description'], str):
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description',
                                              task[0]['description'])
    task[0]['status'] = request.json.get('status', task[0]['status'])
    database.update_task(CONNECTION, task[0])
    return jsonify({'task': make_public_task(task[0])})


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
@auth.login_required
def delete_task(task_id):
    task = database.get_task(CONNECTION, task_id)
    if len(task) == 0:
        abort(404)
    database.delete_task(CONNECTION, task_id)
    return jsonify({'result': True})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')