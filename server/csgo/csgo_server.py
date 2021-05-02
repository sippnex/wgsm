import subprocess
import libtmux
import re


class CsgoServer:

    def process_server_output(self, config, server_name: str, output: list):
        # TODO: process server output
        print(output)

    def validate_installation(self, config):
        completed_process = subprocess.run(
            [config['SteamCMD']['InstallDir'] + '/steamcmd.sh',
            '+force_install_dir',
            config['Gameservers']['InstallDir'] + '/cs16_ds',
            '+runscript',
            config['WGSM']['InstallDir'] + '/server/csgo/steamcmd_validate.txt'],
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
            config['Gameservers']['InstallDir'] + '/cs16_ds',
            '+runscript',
            config['WGSM']['InstallDir'] + '/server/csgo/steamcmd_validate.txt'],
            capture_output=True)
        for line in completed_process.stdout.decode('utf8').split('\n'):
            if re.search('ERROR! Failed to install app \'.*\' \(Invalid platform\)', line):
                print('Installation of csgo failed: Invalid platform')
                return False
        return True

    def start(self, config, tmux_session: libtmux.Session):
        tmux_session.attached_pane.send_keys(config['Gameservers']['InstallDir'] + '/csgo_ds/srcds_run')

    def status(self, config, tmux_session: libtmux.Session):
        return 'running'
