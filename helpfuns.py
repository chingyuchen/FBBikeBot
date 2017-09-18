################################################################################

'''
File : helpfuns.py
Author: Ching-Yu Chen

Description:
helpfuns includes the check and state functions of the "/helps" command program. 
The help program send user command instructions.

Copyright (c) 2017 Ching-Yu Chen
'''

################################################################################

import sys 
sys.path.insert(0, '/home/chingyuc/CYCFBbot')
import messenger

################################################################################

def check_start(data):

    '''
    The check function of the start state. Check if command in data is valid.
    Return ture.
    '''

    return True

#------------------------------------------------------------------------------

def state_start(user, msg_content=None, args=None):

    '''
    Start state function. Send user the list of command instructions. Return
    end state.
    '''

    messenger.send_text(user, \
            '/default : search current or favorite locations.\n'
            '/addr : search address.\n'
            '/fav : list of favs.\n'
            '/editFav : edit fav.\n'
            '/start : greeting!\n'
            '/help : instructions')

    return ["END", None]

################################################################################

# map of state functions
state_funs = {"START":state_start}

# map of check functions
check_funs = {"START":check_start}
