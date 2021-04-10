from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from re import search

import wgsm_core

app_version = '0.1.0'

app = Flask(__name__)
socketio = SocketIO(app)


def emit_server_list_refresh():
    servers = wgsm_core.get_servers()
    servers_as_json = list(
        map(lambda server: {'serverName': search('^wgsm#.*#(.*)', server.get('session_name')).group(1), 'type': 'csgo', 'status': 'running'},
            servers))
    emit('server list refresh', servers_as_json)


@app.route('/')
def page_index():
    return render_template('index.html', app_version=app_version)


@app.route('/list')
def page_server_list():
    return render_template('server_list.html', app_version=app_version)


@app.route('/create')
def page_server_create():
    return render_template('server_create.html', app_version=app_version)


@socketio.on('trigger server list refresh')
def trigger_server_list_refresh():
    emit_server_list_refresh()


@socketio.on('action server create')
def action_server_create(json):
    wgsm_core.create_server('csgo', json['serverName'])
    emit_server_list_refresh()


@socketio.on('action server start')
def action_server_start(json):
    wgsm_core.start_server('csgo', json['serverName'])
    emit_server_list_refresh()


if __name__ == '__main__':
    socketio.run(app)
