#FBBikeBot 
## About
FBBikeBot is a facebook messenger bot provides the user real-time information of the 
word-wide bike-share system. Users can get nearest bike-share station information
by sending current location or address.
                 
## Installation
`pip3 install git+https://github.com/chingyuchen/FBBikeBot`
                 
## Example

### Use current / favorite locations
To find the bike stations, you can choose the option of sending your current location or favorite location, then FBBikeBot
will find the nearest three bike-share stations for you. 

<a href="url"><img src="https://github.com/chingyuchen/FBBikeBot/blob/master/photo_017-09-18_05-33-19.jpg" height="249" width="213"></a>
<a href="url"><img src="https://github.com/chingyuchen/FBBikeBot/blob/master/photo_017-09-18_05-33-19.jpg" height="321" width="213"></a>
                    
### Use address
If you want to find the station by address, type `/addr` then FBBikeBot will request the address from you and search the nearest
stations.

### Edit favorite locations 
To edit your favorite locations, type `/editfav`. FBBikeBot will ask which one you would
like to edit and request the address. After finding the corresponding address and 
confirmed by you, the FBBikeBot will save your new location.

### Check the favorite locations
By typing command `/favs`, FBBikeBot will show your list of favorite locations.

### Help 
If you need the command instruction, type `/help` then FBBikeBot will show you the list of commands manual.
<a href="url"><img src="https://github.com/chingyuchen/CYCFBBot/blob/master/photo_2017-09-02_14-04-08.jpg" height="123" width="213"></a>

              
## Usage
Simply talk to FBBikeBot on facebook!

## Add commands
FBBikeBot is an example of [CYCFBBot](https://github.com/chingyuchen/FBBikeBot)
Developers can use the add programs functions of fbbot module in fbbikebot.py to add more commands.
