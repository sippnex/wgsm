import functools
import flask
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, disconnect
from re import search
from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user, current_user
from passlib.apache import HtpasswdFile

import wgsm_core

app_version = '0.1.0'

app = Flask(__name__)
app.secret_key = '123456789'
socketio = SocketIO(app, cors_allowed_origins=wgsm_core.get_config()['Webserver']['ProxyUrl'])
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'page_login'

class User(UserMixin):

    def __init__(self, id):
        self.id = id
        
    def __repr__(self):
        return f'<User: {self.id}>'


ht = HtpasswdFile('wgsm.htpasswd')
users = list(map(lambda username: User(username), ht.users()))


def emit_server_list_refresh():
    servers = wgsm_core.get_servers()
    servers_as_json = list(
        map(lambda server: {'serverName': search('^wgsm#.*#(.*)', server.get('session_name')).group(1), 'type': 'csgo', 'status': 'running'},
            servers))
    emit('server list refresh', servers_as_json)


def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)
    return wrapped


@login_manager.user_loader
def load_user(user_id):
    user = [u for u in users if u.id == user_id]
    if len(user) > 0:
        return user[0]
    else:
        return None


@app.route('/login', methods=['GET', 'POST'])
def page_login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = [u for u in users if u.id == username]
        if len(user) > 0 and ht.check_password(user[0].id, password):
            login_user(user[0])
            print('Logged in successfully.')
            next = flask.request.args.get('next')
            return flask.redirect(next or flask.url_for('page_index'))
        else:
            error = 'Invalid credentials'
    return render_template('login.html', app_version=app_version, error=error)


@app.route('/')
@login_required
def page_index():
    return flask.redirect(flask.url_for('page_server_list'))
    # return render_template('index.html', app_version=app_version)


@app.route('/list')
@login_required
def page_server_list():
    return render_template('server_list.html', app_version=app_version)


@app.route('/create')
@login_required
def page_server_create():
    return render_template('server_create.html', app_version=app_version)


@socketio.on('action server create')
@authenticated_only
def action_server_create(json):
    wgsm_core.create_server('csgo', json['serverName'])
    emit_server_list_refresh()


@socketio.on('action server start')
def action_server_start(json):
    wgsm_core.start_server('csgo', json['serverName'])
    emit_server_list_refresh()


@socketio.on('trigger server list refresh')
def trigger_server_list_refresh():
    emit_server_list_refresh()


if __name__ == '__main__':
    wgsm_core.init_wgsm()
    socketio.run(app)