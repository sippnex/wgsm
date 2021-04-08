import libtmux
import threading
import time
from re import search

from server import csgo

class ObserveThread (threading.Thread):
    def __init__(self, tmux_server: libtmux.Server):
      threading.Thread.__init__(self)
      self.tmux_server = tmux_server
    def run(self):
        while (True):
            sessions = [s for s in self.tmux_server.sessions if search('^wgsm#.*#.*', s.get('session_name'))]
            for session in sessions:
                output = session.attached_pane.capture_pane()
                print('----------------------')
                print('new output')
                for line in output:
                    print(line)
                print('----------------------')
            time.sleep(2)


def unknown_game(game):
    print(f'unknown game \'{game}\'')

def server_not_found(server_name):
    print(f'server with name \'{server_name}\' not found')

def server_already_exists(server_name):
    print(f'server with name \'{server_name}\' already exists')

def game_exists(game):
    return game == 'csgo'

def get_servers():
    return [s for s in tmux_server.sessions if search('^wgsm#.*#.*', s.get('session_name'))]
    
def create_server(server_name, game):
    if not game_exists(game):
        unknown_game(game)
        return
    tmux_sessions = [s for s in tmux_server.sessions if search('^wgsm#.*#' + server_name, s.get('session_name'))]
    if len(tmux_sessions) > 0:
        server_already_exists(server_name)
        return
    print(f'creating server \'{server_name}\'')
    tmux_session = tmux_server.new_session(session_name='wgsm#' + game + '#' + server_name)
    if game == 'csgo':
        csgo.install(tmux_session)

def start_server(server_name, game):
    if not game_exists(game):
        unknown_game(game)
        return
    print(f'starting server \'{server_name}\'')
    tmux_sessions = [s for s in tmux_server.sessions if search('^wgsm#.*#' + server_name, s.get('session_name'))]
    if len(tmux_sessions) == 0:
        server_not_found(server_name)
        return
    tmux_session = tmux_sessions[0]
    if game == 'csgo':
        csgo.start(tmux_session)

tmux_server = libtmux.Server()
observe_thread = ObserveThread(tmux_server)
observe_thread.start()

#print(session.attached_pane.capture_pane())