################################################################################

'''
File : findstation.py
Author: Ching-Yu Chen

Description:
findstation module helps user to find the nearest bike stations.

Copyright (c) 2017 Ching-Yu Chen
'''

################################################################################

import citybikes
from geopy.distance import vincenty

################################################################################

def in_coordinates(lat, lon):

    '''
    Return the nearest station according to the lat and lon.
    '''

    # check arguments
    try:
        client = citybikes.Client()
        net, dist = next(iter(client.networks.near(lat, lon)))
        sts = net.stations.near(lat, lon)
    except:
        raise ImportError("Error accessing citybikes information")
        messenger.send_text(user, "Sorry the citybikes network currently"
            "is not operating. Can't access the bike station information. :(")
    
    if sts is None or len(sts) == 0:
        return None
    else:
        stations = []
        for i in range(0, min(3, len(sts))):
            stations.append(sts[i])
       
        return stations
        
################################################################################

if __name__ == "__main__":

    print(str(in_coordinates(40, 70)))

