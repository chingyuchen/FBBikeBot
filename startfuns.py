
import sys 
sys.path.insert(0, '/home/chingyuc/CYCFBbot')
import messenger
################################################################################

def check_start(data):
    return True

def state_start(user, msg_content=None, args=None):

    '''
    The start state function. Send greeting to the user and return enum 
    of the end state function. args provide the user name.
    '''

    name = messenger.get_user_info(user)["first_name"]

    messenger.send_text(user, 'Hi, {first_name}! \nFBBikeBot helps you to'\
            ' find the nearest bike station. \nPlease type /help for commands'\
            ' instruction.'.format(first_name=name))

    return ["END", None]
################################################################################
state_funs = {"START":state_start}
check_funs = {"START":check_start}
