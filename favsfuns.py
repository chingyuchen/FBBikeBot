################################################################################

'''
File : favsfuns.py
Author: Ching-Yu Chen

Description:
favsfuns includes the check and state functions of the "/favs" command program. 
The favs program send users their list of favorite locations.

Copyright (c) 2017 Ching-Yu Chen
'''

################################################################################

import geocoder
import sys 
sys.path.insert(0, '/home/chingyuc/CYCFBbot')
import fbbot
import msganalyzer
import messenger
import handleuserinfo 
from geopy.distance import vincenty

################################################################################

# google geocode key
geokey = ""
try:
    with open('geocoder_key', 'r') as f:
        geokey = f.read().strip()
        f.close()
    assert(len(key) != 0)
except:
    print("error in accessing geocoder key")

################################################################################

def check_start(data):

    '''
    The check fucntion of the start state. Check if command in data is valid. 
    Return true.
    '''

    return True

#------------------------------------------------------------------------------

def state_start(user, msg_content=None, args=None):

    '''
    Start state function. Send user the address of his/her favorite locations.
    Return end state.
    '''

    favs = {"fav1":"", "fav2":""}
    for key in favs:
        info = handleuserinfo.get(user, key)
        if info[0] is not None and info[1] is not None:
            lat = info[0]
            lon = info[1]
            try:
                result = geocoder.google([lat, lon], method='reverse', 
                        key=geokey)
                addr = result.address
                favs[key] = addr
            except:
                messenger.send_text(user, "Sorry, the google geocoder"
                        "currently is not operating")
                raise ImportError("problem using geocoder")
                return ["END", None]

    text = "Here's the list of your favorite locations,\n"\
            "* fav1 : \n{favs1}\n"\
            "* fav2 : \n{favs2}\n"\
            "\n".format(favs1=favs["fav1"], favs2=favs["fav2"])
    messenger.send_text(user, text)
    
    return ["END", None]


################################################################################

# map of state functions
state_funs = {"START":state_start}

# map of check fuctions
check_funs = {"START":check_start}


