##################################################################################

'''
File : fbbikebot.py
Author: Ching-Yu Chen

Description:
fbbikebot.py is a facebook messenger bot which provides real-time information of 
world-wide bike-share system.

Copyright (c) 2017 Ching-Yu Chen
'''

##################################################################################

import addrfuns
import favsfuns
import editfavfuns
import defaultfuns
import startfuns
import helpfuns
import sys 
sys.path.insert(0, '/home/chingyuc/CYCFBbot')
import fbbot

##################################################################################

def add_funs(pgmcmd, check_funs, state_funs):

    '''
    Add the check_funs and state_funs to the fbbot module corresponding to the
    pgmcmd.
    '''

    for key in state_funs:
        if key == "START":
            fbbot.set_pgm_state(pgmcmd, key, 
                    check_funs[key], state_funs[key])
        else:
            fbbot.add_pgm_state(pgmcmd, key, 
                    check_funs[key], state_funs[key])

##################################################################################

#Set start
pgmcmd = "/start"
check_funs = startfuns.check_funs
state_funs = startfuns.state_funs
add_funs(pgmcmd, check_funs, state_funs)

#Set help 
pgmcmd = "/help"
check_funs = helpfuns.check_funs
state_funs = helpfuns.state_funs
add_funs(pgmcmd, check_funs, state_funs)


# Set default
pgmcmd = "/default"
fbbot.remove_pgm_state(pgmcmd, "RESPOND")
fbbot.remove_pgm_state(pgmcmd, "QUICKRESPOND")
check_funs = defaultfuns.check_funs
state_funs = defaultfuns.state_funs
add_funs(pgmcmd, check_funs, state_funs)

# Add editfav
pgmcmd = "/editfav"
fbbot.add_cmdpgm(pgmcmd)
check_funs = editfavfuns.check_funs
state_funs = editfavfuns.state_funs
add_funs(pgmcmd, check_funs, state_funs)

# Add favs
pgmcmd = "/favs"
fbbot.add_cmdpgm(pgmcmd)
check_funs = favsfuns.check_funs
state_funs = favsfuns.state_funs
add_funs(pgmcmd, check_funs, state_funs)

# Add favs
pgmcmd = "/addr"
fbbot.add_cmdpgm(pgmcmd)
check_funs = addrfuns.check_funs
state_funs = addrfuns.state_funs
add_funs(pgmcmd, check_funs, state_funs)


fbbot.run()
