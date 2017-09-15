import sqlite3

filename = 'usersinfo.sqlite3'
#-------------------------------------------------------------------------

def run():
    conn = sqlite3.connect(filename)
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS Favs (id TEXT, fav1lati REAL, fav1lon REAL, fav2lati REAL, fav2lon REAL, fav3lati REAL, fav3lon REAL)')

    cur.execute('INSERT INTO Favs (id, fav1lati, fav1lon) VALUES ( ?, ?, ? )', 
        ('1454392541282560', 42.395739, -71.146727))
    conn.commit()
    conn.close()


#-------------------------------------------------------------------------

def get(user, option=None):
    if user is None:
        raise ValueError("user can't be none")
        return None 

    conn = sqlite3.connect(filename)
    cur = conn.cursor()

    if option is None:
        cur.execute('SELECT * FROM Favs WHERE id = ?', (user,))
        locations = cur.fetchone()
        conn.close
        return locations 
    else:
        location = []
        latS = option + 'lati'
        lonS = option + 'lon'
        sqllat = 'SELECT {lat} FROM Favs WHERE id = ?'.format(lat=latS, lon=lonS)
        sqllon = 'SELECT {lon} FROM Favs WHERE id = ?'.format(lat=latS, lon=lonS)
        cur.execute(sqllat, (user,))
        location.append(cur.fetchone()[0])
        #location = cur.fetchone()
        cur.execute(sqllon, (user,))
        location.append(cur.fetchone()[0])
        print("in function = " + str(location))
        conn.close
        return location
        

#-------------------------------------------------------------------------

if __name__ == "__main__":
    run()
    #print(str(get('1454392541282560')))
