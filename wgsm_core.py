import libtmux
from re import search

from server import csgo

tmux_server = libtmux.Server()

def unknown_game(game):
    print(f'unknown game \'{game}\'')

def serer_not_found(server_name):
    print(f'server with name \'{server_name}\' not found')

def server_already_exists(server_name):
    print(f'server with name \'{server_name}\' already exists')

def game_exists(game):
    return game == 'csgo'

def get_servers():
    return [s for s in tmux_server.sessions if search('^wgsm-.*', s.get('session_name'))]

def create_server(server_name, game):
    if not game_exists(game):
        unknown_game(game)
        return
    if tmux_server.has_session('wgsm-' + server_name):
        server_already_exists(server_name)
        return
    print(f'creating server \'{server_name}\'')
    tmux_session = tmux_server.new_session(session_name='wgsm-' + server_name)
    start_server(server_name, game)

def start_server(server_name, game):
    if not game_exists(game):
        unknown_game(game)
        return
    print(f'starting server \'{server_name}\'')
    tmux_session = None
    if not tmux_server.has_session('wgsm-' + server_name):
        serer_not_found(server_name)
        return
    tmux_session = tmux_server.find_where({'session_name': 'wgsm-' + server_name})
    if game == 'csgo':
        csgo.start(tmux_session)

#print(session.attached_pane.capture_pane())