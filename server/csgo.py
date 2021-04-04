import libtmux

def install():
    print('installing csgo server...')

def start(tmux_session: libtmux.Session):
    print('starting csgo server...')
    tmux_session.attached_pane.send_keys('~/github/wgsm/csgo_ds/srcds_run')
