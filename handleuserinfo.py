################################################################################

'''
File : handleuserinfo.py
Author: Ching-Yu Chen

Description:
handleuserinfo module is for edit, get and initialize the data base of the
users' info.

Copyright (c) 2017 Ching-Yu Chen
'''

################################################################################

import sqlite3

################################################################################

# file name of the userinfo
filename = 'usersinfo.sqlite3'

################################################################################

def run():

    '''
    Initialize the sqlfile. 
    '''

    conn = sqlite3.connect(filename)
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS Favs (id TEXT, fav1lati REAL,'
        ' fav1lon REAL, fav2lati REAL, fav2lon REAL, fav3lati REAL, fav3lon REAL)')
    conn.commit()
    conn.close()

#-------------------------------------------------------------------------------

def get(user, option=None):

    '''
    Return the user info according to the option.
    '''

    if user is None:
        raise ValueError("user can't be none")
        return None 

    conn = sqlite3.connect(filename)
    cur = conn.cursor()

    if option is None:
        cur.execute('SELECT * FROM Favs WHERE id = ?', (user,))
        locations = cur.fetchone()
        conn.close()
        return locations 
    else:
        location = [None, None]
        latS = option + 'lati'
        lonS = option + 'lon'
        sqllat = 'SELECT {lat} FROM Favs WHERE id = ?'.format(lat=latS, lon=lonS)
        sqllon = 'SELECT {lon} FROM Favs WHERE id = ?'.format(lat=latS, lon=lonS)

        cur.execute(sqllat, (user,))
        col = cur.fetchone() 
        if col is not None:
            location[0] = col[0]

        cur.execute(sqllon, (user,))
        col = cur.fetchone()
        if col is not None:
            location[1] = col[0]

        conn.close
        return location
        
#---------------------------------------------------------------------------------

def edit(user, option, lat, lon):
    
    '''
    Edit the user info to lat, lon in the option columns
    '''

    conn = sqlite3.connect(filename)
    cur = conn.cursor()

    latS = option + 'lati'
    lonS = option + 'lon'

    sqllat = 'SELECT {lat} FROM Favs WHERE id = ?'.format(lat=latS, lon=lonS)
    sqllon = 'SELECT {lon} FROM Favs WHERE id = ?'.format(lat=latS, lon=lonS)
    cur.execute(sqllat, (user,))
    collat = cur.fetchone()
    cur.execute(sqllon, (user,))
    collon = cur.fetchone()
    

    if collat is None or collon is None:
        cur.execute('INSERT INTO Favs (id, {lat}, {lon}) VALUES ( ?, ?, ?)'.format(lat=latS, lon=lonS), (user, lat, lon))
        conn.commit()
    else:
        cur.execute('UPDATE Favs SET {lat} = ? WHERE id = ?'.format(lat=latS), (lat, user))
        cur.execute('UPDATE Favs SET {lon} = ? WHERE id = ?'.format(lon=lonS), (lon, user))
        conn.commit()

    cur.execute('SELECT * FROM Favs')
    for row in cur :
        print(row)

    conn.close()
    return ["END", None]

#-------------------------------------------------------------------------

if __name__ == "__main__":

    '''
    For testing
    '''

    user = input("Enter the user")
    run()
    print(str(get(user)))
    edit(user, 'fav2', 40, 75)
    print(str(get(user)))
