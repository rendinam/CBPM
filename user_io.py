#
# user_io.py
#
#-*- python -*-
#
#

def prompt_and_run_command(command_set):
    
    for idx, command in enumerate(command_set):
        print('{0:2d} {1:<15}'.format(idx, command.name))

    menu_option = -1
    while menu_option not in range(len(command_set)):
        menu_option = int(input('\nEnter command: '))

    command_set[menu_option].run()
