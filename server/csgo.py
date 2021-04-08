import libtmux

def install(tmux_session: libtmux.Session):
    print('installing csgo server...')
    tmux_session.attached_pane.send_keys('~/Projects/github/wgsm/steamcmd/steamcmd.sh +runscript ~/Projects/github/wgsm/server/steamcmd_install_cs16.txt')

def start(tmux_session: libtmux.Session):
    print('starting csgo server...')
    tmux_session.attached_pane.send_keys('~/Projects/github/wgsm/csgo_ds/srcds_run')