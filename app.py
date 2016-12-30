#!flask/bin/python
from flask import Flask,json
from flask import jsonify
from flask import abort
from flask import request

app = Flask(__name__)


# root page
@app.route('/')
def index():
    return "Hello, Flask"


# get json from server
@app.route('/restapi/get/task/<int:uid>', methods=['GET'])
def get_task(uid):
    json_file = open("./db/tasks.json", "r")
    internal_task = json.load(json_file)
    result = filter(lambda t: t['uid'] == uid, internal_task)
    if len(result) == 0:
        return jsonify({'ERROR': str(uid) + ' not exist'})
    return jsonify({'Task': result})


# post json to server
@app.route('/restapi/post/task', methods=['POST'])
def add_task():
    if not request.json or not 'uid' in request.json:
        abort(400)
    json_file = open("./db/tasks.json", "r")
    internal_task = json.load(json_file)
    json_file.close()
    internal_task.append(request.json)
    json_file = open("tasks.json", "w")
    json.dump(internal_task, json_file)
    json_file.close()
    return jsonify({'New task': request.json}), 201




if __name__ == '__main__':
    app.run(debug=True,
            host="0.0.0.0",
            port=5521)
