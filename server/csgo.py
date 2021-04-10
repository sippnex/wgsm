import libtmux
from re import search


def process_output(output: list):
    output.reverse()
    for line in output:
        if search('^ERROR!.*', line):
            print('---------csgo---------')
            print('Error detected during csgo installation')
            print('---------csgo---------')


def install(tmux_session: libtmux.Session):
    print('installing csgo server...')
    tmux_session.attached_pane.send_keys(
        '~/Documents/Projekte/github/wgsm/steamcmd/steamcmd.sh +runscript ~/Documents/Projekte/github/wgsm/server/steamcmd_install_cs16.txt')


def start(tmux_session: libtmux.Session):
    print('starting csgo server...')
    tmux_session.attached_pane.send_keys('~/Documents/Projekte/github/wgsm/csgo_ds/srcds_run')
