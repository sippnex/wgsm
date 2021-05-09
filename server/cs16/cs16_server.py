import subprocess
import libtmux
import re


class Cs16Server:

    def process_server_output(self, config, server_name: str, output: list):
        # TODO: process server output
        print(output)

    def validate(self, config):
        completed_process = subprocess.run(
            [config['SteamCMD']['InstallDir'] + '/steamcmd.sh',
            '+force_install_dir',
            config['Gameservers']['InstallDir'] + '/cs16',
            '+runscript',
            config['WGSM']['InstallDir'] + '/server/cs16/steamcmd_validate.txt'],
            capture_output=True)
        for line in completed_process.stdout.decode('utf8').split('\n'):
            if re.search('^ERROR! Failed to install app \'.*\' \(Invalid platform\)', line):
                print('Validation of csgo failed: Invalid platform')
                return False
        return True

    def install(self, config):
        completed_process = subprocess.run(
            [config['SteamCMD']['InstallDir'] + '/steamcmd.sh',
            '+force_install_dir',
            config['Gameservers']['InstallDir'] + '/cs16',
            '+runscript',
            config['WGSM']['InstallDir'] + '/server/csgo/steamcmd_validate.txt'],
            capture_output=True)
        for line in completed_process.stdout.decode('utf8').split('\n'):
            if re.search('ERROR! Failed to install app \'.*\' \(Invalid platform\)', line):
                print('Installation of cs16 failed: Invalid platform')
                return False
        return True

    def start(self, config, tmux_session: libtmux.Session):
        tmux_session.attached_pane.send_keys(config['Gameservers']['InstallDir'] + '/cs16/hlds')

    def status(self, config, tmux_session: libtmux.Session):
        return 'running'
