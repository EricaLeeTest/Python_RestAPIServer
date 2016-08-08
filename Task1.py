from flask import Flask, jsonify, make_response, request, abort
import logging
import sys

app = Flask(__name__)

tasks = [
    {
        'id': "a",
        'title': u'item1',

    },
    {
        'id': "b",
        'title': u'item2',

    },
    {
        'id': "c",
        'title': u'item3',

    }
]


@app.route('/tasks', methods=['GET'])
def get_task():
    res = jsonify({'tasks': tasks})
    app.logger.info('GET: {0} successfully with structure content of tasks : {1}'.format(res, tasks))
    return res


@app.errorhandler(404)
def not_found(error):
    error_res = make_response(jsonify({'error': 'Not Found'}), 404)
    app.logger.error(error_res)
    return error_res


@app.route('/tasks', methods=['PUT'])
def create_task():
    msg = 'PUT with Headers: {0} \n Form: {1} \n Body: {2} \n'.format(request.headers, request.form, request.data)
    app.logger.info(msg)

    if not request.json:
        error = 'request.json not existed. \n'
        app.logger.error(error)
        abort(404)

    res = request.json
    if not 'title' in res:
        error = 'PUTT: title not in res: {0} \n'.format(res)
        app.logger.error(error)
        abort(404)

    task = {
        'id': request.json['id'],
        'title': request.json['title'],
    }
    tasks.append(task)
    res = jsonify({'result': 'ADD OK'})
    app.logger.info('PUT successfully with structure content of tasks: {0} \n'.format(tasks))

    return res, 201


@app.route('/tasks/<int:task_id>', methods=['POST'])
def update_task(task_id):
    msg = 'POST with Headers: {0} \n Form: {1} \n Body: {2} \n'.format(request.headers, request.form, request.data)
    app.logger.info(msg)

    if task_id > len(tasks)-1:
        error = 'task: {0} does not exsited. \n'.format(task_id)
        app.logger.error(error)
        abort(404)

    if not request.json:
        error = 'request.json not existed. \n'
        app.logger.error(error)
        abort(401)

    res = request.json

    if 'title' in res and type(res['title']) != unicode:
        error = 'title not in res and format is incorrect: {0} \n'.format(res)
        app.logger.error(error)
        abort(402)

    if 'id' in res and type(res['id']) is not unicode:
        error = 'id not in res and format is incorrect: {0} \n'.format(res)
        app.logger.error(error)
        abort(403)

    tasks[task_id]['id'] = request.json.get('id')
    tasks[task_id]['title'] = request.json.get('title')

    res = "{ 'result':'OK'}"
    app.logger.info('POST successfully with structure content of tasks: {0} \n'.format(tasks))

    return res, 201


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    msg = 'DELETE with Headers: {0} \n Form: {1} \n Body: {2} \n'.format(request.headers, request.form, request.data)
    app.logger.info(msg)

    if task_id > len(tasks)-1:
        error = 'task: {0} does not exsited. \n'.format(task_id)
        app.logger.error(error)
        abort(404)

    tasks.remove(tasks[task_id])
    res = jsonify({'result': 'DELETE ok'})
    app.logger.info('DELETE successfully with structure content of tasks: {0} \n'.format(tasks))

    return res, 201


if __name__ == '__main__':
    print "start"
    handler = logging.FileHandler('appServer.log', encoding='UTF-8')
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)
    ip = sys.argv[1]
    port = 3000
    print "IP with port: {0}:{1}".format(ip, port)
    app.run(host=ip, port=port, debug=True)

