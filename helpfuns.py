
import sys 
sys.path.insert(0, '/home/chingyuc/CYCFBbot')
import messenger

################################################################################

def check_start(data):
    return True

def state_start(user, msg_content=None, args=None):

    messenger.send_text(user, \
            '/default : search current or favorite locations.\n'
            '/addr : search address.\n'
            '/fav : list of favs.\n'
            '/editFav : edit fav.\n'
            '/start : greeting!\n'
            '/help : instructions')

    return ["END", None]


################################################################################
state_funs = {"START":state_start}
check_funs = {"START":check_start}
