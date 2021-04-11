import subprocess
import libtmux

class CsgoServer:

    def process_server_output(self, server_name: str, output: list):
        # TODO: process server output
        print(output)


    def validate_installation(self):
        completed_process = subprocess.run(['/Users/juliansobotka/Projects/github/wgsm/steamcmd/steamcmd.sh', '+runscript', '/Users/juliansobotka/Projects/github/wgsm/server/csgo/steamcmd_validate.txt'], capture_output=True)
        print(completed_process.stdout)
        for line in completed_process.stdout.decode('utf8').split('\n'):
            print(line)
        return True


    def install(self):
        self.validate_installation()


    def start(self, tmux_session: libtmux.Session):
        tmux_session.attached_pane.send_keys('/Users/juliansobotka/Projects/github/wgsm/csgo_ds/srcds_run')


    def status(self, tmux_session: libtmux.Session):
        return 'running'
