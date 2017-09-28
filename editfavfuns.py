################################################################################

'''
File : editfavfuns.py
Author: Ching-Yu Chen

Description:
editfavfuns includes the check and state functions of the "/editfav" command 
program. The editfavs program let users edit their list of favorite locations.

Copyright (c) 2017 Ching-Yu Chen
'''

################################################################################

import geocoder
import handleuserinfo 
import sys 
sys.path.insert(0, '/home/chingyuc/CYCFBbot')
import fbbot
import msganalyzer
import messenger
from geopy.distance import vincenty

################################################################################

# google gecoder key
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
    Check function of the start state. Check if command in data is valid.
    Return true.
    '''

    return True

#------------------------------------------------------------------------------

def state_start(user, msg_content=None, args=None):

    '''
    Start state functions. Send user the list of their favrite location address,
    and ask which one to edit in quick reply. Return next state.
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
            "\nWhich one would you like to edit?".format(\
            favs1=favs["fav1"], favs2=favs["fav2"])
    
    quick_replies = [
        {
            "content_type":"text",
            "title":"Fav1",
            "payload":"fav1"
        },
        {
            "content_type":"text",
            "title":"Fav2",
            "payload":"fav2"
        }
    ]
    
    messenger.send_quickreply(user, text, quick_replies)

    return ["REQUEST", None]

#--------------------------------------------------------------------------

def check_request(data):

    '''
    Check function of the request state. Return true if the command in data
    is valid, otherwise, return false.
    '''
    
    [chat_id, msg_type, msg_content] = msganalyzer.glance_msg(data)
       
       # should also check quick_reply type
    if msg_type is 'sent_msg':  
        if 'text' in msg_content:
            if msg_content['text'] == 'Fav1' or \
                    msg_content['text'] == 'Fav2':
                return True
            else:
                return False
    return False

#--------------------------------------------------------------------------

def state_request(user, msg_content=None, args=None):

    '''
    Requst state function. Requst user to send the address. Return the 
    option in msg_content and the next state.
    '''

    option = msg_content['quick_reply']['payload']
    messenger.send_text(user, "Please enter the address.")

    return ["ADDRESS", option]

#--------------------------------------------------------------------------

def check_address(data):

    '''
    Check function of the address state. Return true if command in data is
    valid. Otherwise return false.
    '''

    [chat_id, msg_type, msg_content] = msganalyzer.glance_msg(data)

    if msg_type is 'sent_msg' and 'text' in msg_content:
        return True
    else:
        return False

#--------------------------------------------------------------------------

def state_address(user, msg_content=None, args=None):

    '''
    State function of the address dtate. Use the addrss in msg_content to 
    find the corresponding address. If corresponding address can't be find
    send user message and raise the error. Otherwise send user the 
    corresponding address and request quick reply if it is correct or not.
    Return the address, location, option in args and the next state.
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

    next_args = {'option':args, 'addr':corres_addr, 'location':location}
    
    return ["EDIT", next_args]

#--------------------------------------------------------------------------

def check_edit(data):
     
    '''
    Check function of edit state. If command in data is valid return true.
    Otherwise, return false.
    '''

    [chat_id, msg_type, msg_content] = msganalyzer.glance_msg(data)

    if msg_type is 'sent_msg' and 'text' in msg_content:
        if msg_content['text'] == 'Correct' or \
                msg_content['text'] == 'WrongAddress':
            return True
    return False


#--------------------------------------------------------------------------

def state_edit(user, msg_content, args):
    
    '''
    Edit state function. if the reply from user in msg_content is correct
    send user message "finished edit" and return end state. Otherwise,
    request the address again and return the next state.
    '''

    reply = msg_content['quick_reply']['payload']
    if reply == "incorrect":
        messenger.send_text(user, "Please enter the address again.")
        return ["ADDRESS", args['option']]
    else:
        handleuserinfo.edit(user, args['option'], 
                args['location']['lat'], args['location']['long'])
        messenger.send_text(user, "Finished Edit!")

    return ["END", None]


################################################################################

# map of the state functions
state_funs = {"START":state_start, "REQUEST":state_request, \
        "ADDRESS":state_address, "EDIT":state_edit}

# map of the check functions
check_funs = {"START":check_start, "REQUEST":check_request, \
        "ADDRESS":check_address, "EDIT":check_edit}

    


