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

    text = "Where would you like to search?"
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
                imgslots=emojs, dist=dis, target=loca)

               
            buttons = [{"type":"postback", "title":"View in map", "payload":"viewmap" + str(i)}]
            if i is 0:
                done = {"type":"postback", "title":"Done!", "payload":"done"}
                buttons.append(done)
            messenger.send_buttons(user, text, buttons)


    return ["MAP", sta]


#-------------------------------------------------------------------------------

def check_map(data):
    
    [chat_id, msg_type, msg_content] = msganalyzer.glance_msg(data)
        
    if msg_type is 'postback':
        if msg_content['title'] == 'View in map' or \
                msg_content['title'] == 'Done!':
            return True
        else:
            return False
    else:
        return False


#-------------------------------------------------------------------------------

def state_map(user, msg_content, args):

    if msg_content['title'] == 'Done!':
        return ["END", None]

    sta = args
    payload = msg_content['payload']
    index = int(payload[len(payload) - 1:])
    messenger.send_location(user, sta[index][0]['latitude'], sta[index][0]['longitude'])

    buttons = [{"type":"postback", "title":"Done!", "payload":"done"}]
    text = "Done?"
    messenger.send_buttons(user, text, buttons)

    return ["MAP", sta]

################################################################################

state_funs = {"START":state_start, "LOCATION":state_location, "MAP":state_map}
check_funs = {"START":check_start, "LOCATION":check_location, "MAP":check_map}

################################################################################

if __name__ == "__main__":

    '''
    for testing
    '''
    
    fbbot.remove_pgm_state("/default", "RESPOND")
    fbbot.remove_pgm_state("/default", "QUICKRESPOND")
    fbbot.set_pgm_state("/default", "START", check_start, state_start)
    fbbot.add_pgm_state("/default", "LOCATION", check_location, state_location)
    fbbot.add_pgm_state("/default", "MAP", check_map, state_map)

    print("default pgm states = " +  str(fbbot.get_pgmstates("/default")))

    fbbot.run()

