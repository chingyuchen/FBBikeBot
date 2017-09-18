################################################################################

'''
File : startfuns.py
Author: Ching-Yu Chen

Description:
startfuns includes the check and state functions of the "/start" command program. 
The start program greets to the user.

Copyright (c) 2017 Ching-Yu Chen
'''

################################################################################

import sys 
sys.path.insert(0, '/home/chingyuc/CYCFBbot')
import messenger

################################################################################

def check_start(data):

    '''
    Check function of the start state. Check if command in data is valid.
    Return true.
    '''

    return True

#-------------------------------------------------------------------------------

def state_start(user, msg_content=None, args=None):

    '''
    The start state function. Send greeting to the user and return the end state.
    '''

    name = messenger.get_user_info(user)["first_name"]

    messenger.send_text(user, 'Hi, {first_name}! \nFBBikeBot helps you to'\
            ' find the nearest bike station. \nPlease type /help for commands'\
            ' instruction.'.format(first_name=name))

    return ["END", None]

################################################################################

# map of state functions
state_funs = {"START":state_start}

# map of check functions
check_funs = {"START":check_start}
