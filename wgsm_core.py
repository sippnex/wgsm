import libtmux
import threading
import time
import re

from server.csgo.csgo_server import CsgoServer


class ObserverThread(threading.Thread):
    def __init__(self, server: libtmux.Server):
        threading.Thread.__init__(self)
        self.tmux_server = server

    def run(self):
        while True:
            wgsm_sessions = [s for s in self.tmux_server.sessions if re.search('^wgsm(#.*)*', s.get('session_name'))]
            for wgsm_session in wgsm_sessions:
                output = wgsm_session.attached_pane.capture_pane()
                attributes = re.split('#', wgsm_session.get('session_name'))
                game = attributes[1]
                server_name = attributes[2]
                game_servers[game].process_server_output(server_name, output.copy())
            time.sleep(2)


def unknown_game(game):
    print(f'unknown game \'{game}\'')


def server_already_installing(game):
    print(f'game-server \'{game}\' already installing')


def server_not_found(server_name):
    print(f'server with name \'{server_name}\' not found')


def server_already_exists(server_name):
    print(f'server with name \'{server_name}\' already exists')


def game_exists(game):
    return game == 'csgo'


def get_servers():
    return [s for s in tmux_server.sessions if re.search('^wgsm#server(#.*)*', s.get('session_name'))]


def validate_installation(game):
    if not game_exists(game):
        unknown_game(game)
        return
    game_servers[game].validate_installation()


def install(game):
    if not game_exists(game):
        unknown_game(game)
        return
    print(f'installing game-server \'{game}\'')
    game_servers[game].install()


def create_server(game, server_name):
    if not game_exists(game):
        unknown_game(game)
        return
    server_sessions = [s for s in tmux_server.sessions if re.search('^wgsm#.*#' + server_name, s.get('session_name'))]
    if len(server_sessions) > 0:
        server_already_exists(server_name)
        return
    print(f'creating server \'{server_name}\'')
    tmux_server.new_session(session_name='wgsm#' + game + '#' + server_name)


def start_server(game, server_name):
    if not game_exists(game):
        unknown_game(game)
        return
    server_sessions = [s for s in tmux_server.sessions if re.search('^wgsm#' + game + '#' + server_name, s.get('session_name'))]
    if len(server_sessions) == 0:
        server_not_found(server_name)
        return
    if game_servers[game].validate_installation() == False:
        install_server(game)
    print(f'starting server \'{server_name}\'')
    server_session = server_sessions[0]
    game_servers[game].start(server_session)

def start_observing():
    observer_thread = ObserverThread(tmux_server)
    observer_thread.start()

tmux_server = libtmux.Server()

game_servers = {
    'csgo': CsgoServer()
}