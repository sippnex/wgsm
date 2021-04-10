import libtmux
import threading
import time
import re

from server import csgo


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
                session_type = attributes[1]
                game = attributes[2]
                if session_type == 'install':
                    csgo.process_install_output(output.copy())
                elif session_type == 'server':
                    server_name = attributes[3]
                    csgo.process_server_output(server_name, output.copy())
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


def install_server(game):
    if not game_exists(game):
        unknown_game(game)
        return
    install_sessions = [s for s in tmux_server.sessions if re.search('^wgsm#install#' + game, s.get('session_name'))]
    if len(install_sessions) > 0:
        server_already_installing(game)
        return
    print(f'installing game-server \'{game}\'')
    install_session = tmux_server.new_session(session_name='wgsm#install#' + game)
    if game == 'csgo':
        csgo.install(install_session)


def create_server(game, server_name):
    if not game_exists(game):
        unknown_game(game)
        return
    server_sessions = [s for s in tmux_server.sessions if re.search('^wgsm#server#.*#' + server_name, s.get('session_name'))]
    if len(server_sessions) > 0:
        server_already_exists(server_name)
        return
    print(f'creating server \'{server_name}\'')
    tmux_server.new_session(session_name='wgsm#server#' + game + '#' + server_name)


def start_server(game, server_name):
    if not game_exists(game):
        unknown_game(game)
        return
    server_sessions = [s for s in tmux_server.sessions if re.search('^wgsm#server#' + game + '#' + server_name, s.get('session_name'))]
    if len(server_sessions) == 0:
        server_not_found(server_name)
        return
    print(f'starting server \'{server_name}\'')
    server_session = server_sessions[0]
    if game == 'csgo':
        csgo.start(server_session)

tmux_server = libtmux.Server()
observer_thread = ObserverThread(tmux_server)
observer_thread.start()