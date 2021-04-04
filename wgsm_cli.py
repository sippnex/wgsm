import sys

import wgsm_core

def invalid_arguments():
    print('invalid arguments')
    sys.exit(1)

def command_list(argv):
    servers = wgsm_core.get_servers()
    print(servers)

def command_start(argv):
    if len(argv) == 3:
        wgsm_core.start_server(argv[2])
    else:
        invalid_arguments()

if len(sys.argv) < 2:
    invalid_arguments()

if sys.argv[1] == 'list':
    command_list(sys.argv)
elif sys.argv[1] == 'start':
    command_start(sys.argv)
else:
    invalid_arguments()

