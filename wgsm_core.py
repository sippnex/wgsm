import libtmux
import threading
import time
import re
import configparser
import os.path
import subprocess

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
                game_servers[game].process_server_output(config, server_name, output.copy())
            time.sleep(2)


def get_config():
    return config


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
    return [s for s in tmux_server.sessions if re.search('^wgsm(#.*)*', s.get('session_name'))]


def init_wgsm():
    # TODO: check steamcmd installation
    if not os.path.isfile(config['SteamCMD']['InstallDir'] + '/steamcmd.sh'):
        print('steamcmd is not installed')
        install_steamcmd()


def install_steamcmd():
    # curl -sqL "https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz" | tar zxvf -
    print('install steamcmd')
    if not os.path.exists(config['SteamCMD']['InstallDir']):
        os.makedirs(config['SteamCMD']['InstallDir'])
    cmd = 'curl -sqL "' + config['SteamCMD']['DownloadURL'] + '" | tar zxvf - -C ' + config['SteamCMD']['InstallDir']
    ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    output = ps.communicate()[0]
    print(output)


def install_game(game):
    if not game_exists(game):
        unknown_game(game)
        return
    if validate_game(game):
        print(f'game-server \'{game}\' already installed')
        return
    print(f'installing game-server \'{game}\'')
    return game_servers[game].install(config)


def validate_game(game):
    if not game_exists(game):
        unknown_game(game)
        return
    return game_servers[game].validate_installation(config)


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
    server_sessions = [s for s in tmux_server.sessions if
                       re.search('^wgsm#' + game + '#' + server_name, s.get('session_name'))]
    if len(server_sessions) == 0:
        server_not_found(server_name)
        return
    if not game_servers[game].validate_installation(config):
        success = install(game)
        if not success:
            print(f'installation of game \'{game}\' failed')
            return
    print(f'starting server \'{server_name}\'')
    server_session = server_sessions[0]
    game_servers[game].start(config, server_session)


def start_observing():
    observer_thread = ObserverThread(tmux_server)
    observer_thread.start()


config = configparser.ConfigParser()
config.read('wgsm.ini')
tmux_server = libtmux.Server()

game_servers = {
    'csgo': CsgoServer()
}
