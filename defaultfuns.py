################################################################################
import sys 
sys.path.insert(0, '/home/chingyuc/CYCFBbot')
import fbbot
import msganalyzer
import messenger
import handleuserinfo 
from geopy.distance import vincenty
import findstation

################################################################################

# Token of the bot.
TOKEN = ""
with open('Token', 'r') as f:
    TOKEN = f.read().strip()
    f.close()


#-------------------------------------------------------------------------------

sqlfile = "usersinfo.sqlite3"  
with open('usersinfo.sqlite3', 'a+') as f:

    try:
        assert(f != None)
        handleuserinfo.run() 
            
    except:
        print("no user info file")

f.close()


################################################################################
#Deault

def check_start(data):
    return True

def state_start(user, msg_content=None, args=None):
        
    '''
    The start state function. Return enum of the next state function and args. 
    '''

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
        },
        {
            "content_type":"text",
            "title":"Fav3",
            "payload":"fav3"
        },
        {
            "content_type":"location"
        }
    ]

    text = "Where would you like to go?"
    messenger.send_quickreply(user, text, quick_replies)
    return ["LOCATION", None]

#-------------------------------------------------------------------------------

def check_location(data):

    '''
    Return true if the respond message for the request state function from 
    the user is valid. Otherwise, return false.
    '''
    [chat_id, msg_type, msg_content] = msganalyzer.glance_msg(data)
        
    if msg_type is 'sent_msg': 
        if 'text' in msg_content:
            if msg_content['text'] == 'Fav1' or \
                msg_content['text'] == 'Fav2' or\
                msg_content['text'] == 'Fav3':
                return True
            else:
                return False
        elif 'attachments' in msg_content and \
                msg_content['attachments'][0]['type'] == 'location':
            return True
        else:
            return False
    else:
        return False 

#-------------------------------------------------------------------------------

def state_location(user, msg_content=None, args=None):

    location = {}
    loca = ""

    if 'text' in msg_content:
        option = msg_content['quick_reply']['payload']
        info = handleuserinfo.get(user, option)
        if info[0] is None or info[1] is None:
            messenger.send_text(user, 'The favorite location is'
                ' not set yet. Please use /editFav to set')
            return ["END", None]
        else: 
            loca = msg_content['text']
            location['lat'] = info[0]
            location['long'] = info[1]

    else:
        location = msg_content['attachments'][0]['payload']['coordinates']
        loca = "current"


    sta = findstation.in_coordinates(location['lat'], location['long'])
    if sta is None:
        messenger.sent_text(user, "Sorry no station is found")
    else:
        messenger.send_location(user, sta[0][0]['latitude'], sta[0][0]['longitude'])
        posi1 = (location['lat'], location['long'])
        for stai in sta:
            name = stai[0]['name']
            free = stai[0]['free_bikes']
            slots = stai[0]['empty_slots']
            posi2 = (stai[0]['latitude'], stai[0]['longitude'])
            distval = vincenty(posi1, posi2).meters
            dis = "{:1.1f}".format(distval)
            emojf = u"\U0001F6B2"*min(10, free)
            emojs = u"\U0001F17F"*min(10, slots)
            messenger.send_text(user, "Station {sta}"\
                "\n{bikes} free bikes, {park} empty slots.\
                \n{imgbikes}\
                \n{imgslots}\
                \n{dist} meters away."\
                .format(sta=name, bikes=free, park=slots, imgbikes=emojf,\
                imgslots=emojs, dist=dis, target=loca))
                
    return ["END", None]



################################################################################

state_funs = {"START":state_start, "LOCATION":state_location}
check_funs = {"START":check_start, "LOCATION":check_location}

#print(str(fbbot.get_pgmcmds()))
#print("default pgm states = " +  str(fbbot.get_pgmstates("/default")))

fbbot.remove_pgm_state("/default", "RESPOND")
fbbot.remove_pgm_state("/default", "QUICKRESPOND")
fbbot.set_pgm_state("/default", "START", check_start, state_start)
fbbot.add_pgm_state("/default", "LOCATION", check_location, state_location)
print("default pgm states = " +  str(fbbot.get_pgmstates("/default")))

fbbot.run()
