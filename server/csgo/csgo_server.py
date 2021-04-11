import subprocess
import libtmux
import re


class CsgoServer:

    def process_server_output(self, server_name: str, output: list):
        # TODO: process server output
        print(output)

    def validate_installation(self):
        completed_process = subprocess.run(
            ['/Users/juliansobotka/Documents/Projekte/github/wgsm/steamcmd/steamcmd.sh', '+runscript',
             '/Users/juliansobotka/Documents/Projekte/github/wgsm/server/csgo/steamcmd_validate.txt'],
            capture_output=True)
        for line in completed_process.stdout.decode('utf8').split('\n'):
            if re.search('^ERROR! Failed to install app \'.*\' \(Invalid platform\)', line):
                print('Validation of csgo failed: Invalid platform')
                return False
        return True

    def install(self):
        completed_process = subprocess.run(
            ['/Users/juliansobotka/Documents/Projekte/github/wgsm/steamcmd/steamcmd.sh', '+runscript',
             '/Users/juliansobotka/Documents/Projekte/github/wgsm/server/csgo/steamcmd_validate.txt'],
            capture_output=True)
        for line in completed_process.stdout.decode('utf8').split('\n'):
            if re.search('ERROR! Failed to install app \'.*\' \(Invalid platform\)', line):
                print('Installation of csgo failed: Invalid platform')
                return False
        return True

    def start(self, tmux_session: libtmux.Session):
        tmux_session.attached_pane.send_keys('/Users/juliansobotka/Documents/Projekte/github/wgsm/csgo_ds/srcds_run')

    def status(self, tmux_session: libtmux.Session):
        return 'running'
