################################################################################

'''
File : addrfuns.py
Author: Ching-Yu Chen

Description:
addrfuns includes the check and state functions of the "/addr" command program. 
addr program use users input address to search the nearest bike stations.

Copyright (c) 2017 Ching-Yu Chen
'''

################################################################################

import defaultfuns
import findstation
import geocoder
import handleuserinfo 
import sys 
sys.path.insert(0, '/home/chingyuc/CYCFBbot')
import fbbot
import msganalyzer
import messenger
from geopy.distance import vincenty

################################################################################

# google geocoder key
geokey = ""
try:
    with open('geocoder_key', 'r') as f:
        geokey = f.read().strip()
        f.close()
    assert(len(key) != 0)
except:
    print("error in accessing geocoder key")

# Token of the bot.
TOKEN = ""
with open('Token', 'r') as f:
    TOKEN = f.read().strip()
    f.close()

################################################################################

def check_start(data):

    '''
    The check function of the start state. Check if command in data is valid.
    Return true.
    '''

    return True

#-------------------------------------------------------------------------------

def state_start(user, msg_content=None, args=None):

    '''
    Start state function. Send messege to user to request the address. Return 
    the next state.
    '''

    messenger.send_text(user, "Please enter the address.")

    return ["ADDRESS", None]

#-------------------------------------------------------------------------------

def check_address(data):

    '''
    Address state check function. If input command in data is valid return true.
    Otherwise, return false.
    '''

    [chat_id, msg_type, msg_content] = msganalyzer.glance_msg(data)
       
    if msg_type is 'sent_msg' and 'text' in msg_content:
        return True
    return False

#-------------------------------------------------------------------------------

def state_address(user, msg_content=None, args=None):

    '''
    Address state function. From the address in msg_content that user send, search
    the corresponding address. Send quick reply message to user and ask if the 
    corresponding address is correct. Return the next state and the location of
    the address.
    '''

    addr = msg_content['text']
    try:
        g = geocoder.google(addr, key=geokey)
        location = {'lat':g.latlng[0], 'long':g.latlng[1]}
        result = geocoder.google([g.latlng[0], g.latlng[1]],
                method='reverse', key=geokey)
        corres_addr = result.address
    except:
        messenger.send_text(user, "Sorry there's problem using"\
                " geocoder to search.")
        raise ImportError("problem using geocoder")
        return ["END", None] 
        
    quick_replies = [
        {
            "content_type":"text",
            "title":"Correct",
            "payload":"correct"
        },
        {
            "content_type":"text",
            "title":"WrongAddress",
            "payload":"incorrect"
        }
    ] 

    text = corres_addr + "\nIs the address correct?"
    messenger.send_quickreply(user, text, quick_replies)
    
    return ["SEARCH", location]

#-------------------------------------------------------------------------------

def check_search(data):
     
    '''
    Check function of the search state. If command in data is valid return true,
    otherwise, return false.
    '''

    [chat_id, msg_type, msg_content] = msganalyzer.glance_msg(data)

    if msg_type is 'sent_msg' and 'text' in msg_content:
        if msg_content['text'] == 'Correct' or \
                msg_content['text'] == 'WrongAddress':
            return True
    return False

#-------------------------------------------------------------------------------

def state_search(user, msg_content, args):

    '''
    Form the msg_content that user replies, if the address is correct search the
    nearest bike stations of the location in args. Otherwise, request the address
    again. Return the next state.
    '''

    location = args

    reply = msg_content['quick_reply']['payload']
    if reply == "incorrect":
        messenger.send_text(user, "Please enter the address again.")
        return ["ADDRESS", None]

    else:
        sta = findstation.in_coordinates(location['lat'], location['long'])
        if sta is None:
            messenger.sent_text(user, "Sorry no station is found")
        else:
            posi1 = (location['lat'], location['long'])
            order = ["[1st]\n", "[2nd]\n", "[3rd]\n"]
            for i in reversed(range(len(sta))):
                name = sta[i][0]['name']
                free = sta[i][0]['free_bikes']
                slots = sta[i][0]['empty_slots']
                posi2 = (sta[i][0]['latitude'], sta[i][0]['longitude'])
                distval = vincenty(posi1, posi2).meters
                dis = "{:1.1f}".format(distval)
                emojf = u"\U0001F6B2"*min(7, free)
                emojs = u"\U0001F17F"*min(10, slots)

                text = "{staorder}{sta}"\
                    "\n{bikes} bikes, {park} slots.\
                    \n{imgbikes}\
                    \n{imgslots}\
                    \n{dist} meters away."\
                    .format(staorder=order[i], sta=name, bikes=free, park=slots, imgbikes=emojf,\
                    imgslots=emojs, dist=dis)

                   
                buttons = [{"type":"postback", "title":"View in map", "payload":"viewmap" + str(i)}]
                if i is 0:
                    done = {"type":"postback", "title":"Done!", "payload":"done"}
                    buttons.append(done)
                messenger.send_buttons(user, text, buttons)

    return ["MAP", sta]

################################################################################

# state functions of the address program
state_funs = {"START":state_start, "ADDRESS":state_address, 
        "SEARCH":state_search, "MAP": defaultfuns.state_map}

# check functions of the address program
check_funs = {"START":check_start, "ADDRESS":check_address, 
        "SEARCH":check_search, "MAP": defaultfuns.check_map}

################################################################################
