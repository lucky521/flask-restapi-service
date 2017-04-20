#!flask/bin/python
# import third-party component
import flask
from flask import Flask,json
from flask import jsonify
from flask import abort
from flask import request
import flask_login
from OpenSSL import SSL
import threading
import os

# import local component
import file_db

app = Flask(__name__)
app.secret_key = 'I am Lucky'


# root page
@app.route('/')
def index():
    return "Hello, Flask"

@app.route('/root')
@flask_login.login_required
def root_fun():
    return "Hello, this is root"

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


# delete one item




# post binary to server
@app.route('/image/restapi/post', methods=['POST'])
def add_image():
    # store binary to db  
    print request.files['image'] # image_key is key of file
    image_file = request.files['image']
    image_id = file_db.put_file(image_file)    

    return image_id


# get binary from server
@app.route('/image/restapi/get/<image_id>', methods=['GET'])
def get_image(image_id): 
    # get binary from db
    
    return flask.send_from_directory("./db", "lena.jpeg")



# User login
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(name):
    user = User()
    user.id = name
    return user

@login_manager.request_loader
def request_loader(request):
    user = User()
    user.id = request.form['name']
    user.is_authenticated = True
    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '''
            <form action='login' method='POST'>
            <input type='text' name='name' id='name' placeholder='name'></input>
            <input type='password' name='pw' id='pw' placeholder='password'></input>
            <input type='submit' name='submit'></input>
            </form>
               '''
    name = request.form['name']
    pw = request.form['pw']
    if name == 'lucky' and pw == 'lulu':
         user = User() 
         user.id = name
         flask_login.login_user(user)
         return "Welcome!"
    else:
        return "Who are you?!"


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'You are Unauthorized!'




def run_https_server():
    context = ('./certificates/alice.crt', './certificates/alice.key')
    app.run(debug=True,
            host="0.0.0.0",
            port=443,
            ssl_context=context)

def run_http_server():
    app.run(debug=True,
            host="0.0.0.0",
            port=80)

if __name__ == '__main__':
    #print "https process..."
    #run_https_server()

    print "http process..."
    run_http_server()
    
