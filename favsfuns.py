
import geocoder
import sys 
sys.path.insert(0, '/home/chingyuc/CYCFBbot')
import fbbot
import msganalyzer
import messenger
import handleuserinfo 
from geopy.distance import vincenty

################################################################################

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
    return True

def state_start(user, msg_content=None, args=None):

    favs = {"fav1":"", "fav2":"", "fav3":""}
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
            "* fav3 : \n{favs3}\n"\
            "\n".format(favs1=favs["fav1"], favs2=favs["fav2"], favs3=favs["fav3"])
    messenger.send_text(user, text)
    
    return ["END", None]


################################################################################

state_funs = {"START":state_start}
check_funs = {"START":check_start}


