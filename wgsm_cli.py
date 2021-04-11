import sys

import wgsm_core


def invalid_arguments():
    print('invalid arguments')
    sys.exit(1)


def command_list(argv):
    servers = wgsm_core.get_servers()
    print(servers)


def command_validate(argv):
    if len(argv) == 3:
        wgsm_core.validate_installation(argv[2])
    else:
        invalid_arguments()


def command_install(argv):
    if len(argv) == 3:
        wgsm_core.install(argv[2])
    else:
        invalid_arguments()


def command_create(argv):
    if len(argv) == 4:
        wgsm_core.create_server(argv[2], arg[3])
    else:
        invalid_arguments()


def command_start(argv):
    if len(argv) == 4:
        wgsm_core.start_server(argv[2], arg[3])
    else:
        invalid_arguments()


if len(sys.argv) < 2:
    invalid_arguments()

if sys.argv[1] == 'list':
    command_list(sys.argv)
elif sys.argv[1] == 'validate':
    command_validate(sys.argv)
elif sys.argv[1] == 'install':
    command_install(sys.argv)
elif sys.argv[1] == 'create':
    command_create(sys.argv)
elif sys.argv[1] == 'start':
    command_start(sys.argv)
else:
    invalid_arguments()
