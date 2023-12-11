import psycopg2
import datetime

def register(cursor, username, password):
    #when taking username and password, check if username already exists.
    cursor.execute("SELECT username FROM UserInformation WHERE username = %s", (username,))
    if cursor.fetchone() is not None:
        return 0 #fail condition checked during program invalid username
    #   yes; return 0
    #   no; add to database with userID = number of users + 1 unless no users then = 1
    else:
        cursor.execute("SELECT COUNT(*) FROM UserInformation")
        if cursor.fetchone is None:
            userID = 1
        else:
            tuple = cursor.fetchone()
            print(tuple[0])
            userID = tuple[0] + 1
        cursor.execute("INSERT INTO UserInformation(userID, username, password) \
                        VALUES (%s, %s, %s)", [userID, username, password])
        con.commit()

def login(cursor, username, password):
    #check database for username;
    cursor.execute("SELECT username FROM userinformation WHERE username = %s", (username,))
    if cursor.fetchone() is None:
        return 0 #fail condition invalid username
    # username exists; check password against password associated with username
    else:
        cursor.execute("SELECT password FROM userinformation WHERE username = %s", (username,))
        ohgod = cursor.fetchone()
        if password == ohgod[0]:
            cursor.execute("SELECT userid FROM userinformation WHERE username = %s", (username,))
            userid = cursor.fetchone()
            return userid[0] #return userid
        else:
            return -1 #fail invalid password
        
def addFriend(cursor, userid, freindid):
    #insert with friend ID into friends table
    cursor.execute("INSERT INTO FriendList (userid, friendid) VALUES (%s, %s);", [userid, freindid])
    con.commit()

def addLog(cursor, userid, speciesid, date):
    #insert into the database based on userid and species id. Add date
    cursor.execute("INSERT INTO userlog (userid, birdid, date) VALUES (%s, %s, %s)", [userid, speciesid, date])
    #update nbirdlogged value for that user
    cursor.execute("SELECT nlogs FROM nbirdlogged WHERE userid = %s", (userid,))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO nbirdlogged (userid, nlogs) VALUES (%s, 1)", (userid,))
    else:
        logedItems = cursor.fetchone()
        nItems = logedItems[0] + 1
        cursor.execute("UPDATE nbirdlogged SET nlogs = %s WHERE userid = %s", [nItems, userid])
    con.commit()
    

def viewLog(cursor, userid, date):
    #grab birdid from userlog based on date and userid
    cursor.execute("SELECT birdid FROM userlog WHERE userid = %s AND date = %s", [userid, date])
    birdid = cursor.fetchone()
    #use birdid to display everything about the speicies logged from that log
    cursor.execute("SELECT genus, species.species, commonname FROM species WHERE species.speciesid = %s", (birdid[0],))
    print(cursor.fetchone())

def findBirdId(cursor, birdname):
    cursor.execute("SELECT speciesid FROM species WHERE commonname = %s", (birdname,))
    if cursor.fetchone() is not None:
        bird = cursor.fetchone()
        return bird[0]
    else:
        return -1 #not found


#MAIN
#Initialize connection

con = psycopg2.connect(host= "localhost",
                    database = "BirdLog",
                    user = "postgres",
                    password = "Di20amo11nd!",
                    port = "5432"
                     )

cursor = con.cursor()
option = -1
userid = -1
while option != '0':
    #prompt for input login or register or exit
    option = input("Select an option: \n 0. Exit 1. Login 2. Register \n")
    #1
    if (option == '1'):
    #login:
        loggedin = False
        while loggedin == False:
            #prompt for username: store it
            usernameUser = input("Type a username: ")
            #prompt for password: store it
            passUser = input("Type a password: ")
            #call login(cursor, username, password)
            answer = login(cursor, usernameUser, passUser)
            #if login 0 print that it failed and change option to login
            if answer == 0:
                print("Invalid username")
            elif answer == -1:
                print("Invalid password")
            else:
                userid = answer
                loggedin = True         
        #if login is succesful, prompt for options of friends and other stuff, logout changes option to 0 and exits
        #login succesful when loop ends
        loginoption = input("Select an option: \n 0. Exit \n 1. Add Friend \n 2. Remove Friend \n 3. Add Log \n 4. View Log  \n 5.View Freinds \n \
                             6. View Friend Log \n 7. View Number of Logs \n 8. View Friends Number of Logs \n 9. View UserID \n")
        match loginoption:
            case '0':
                option = 0
            case '1':
                friendid = input("Enter the userID of your freind: ")
                addFriend(cursor, userid, friendid)
            case '2':
                #prompt for friend
                friendToDelete = input("Enter the name of the friend you would like to remove")
                #find id
                cursor.execute("SELECT userid FROM userinformation WHERE username = %s", (friendName,))
                friendid = cursor.fetchone()
                #delete from friend list
                cursor.execute("DELETE FROM friendlist WHERE friendid = %s AND userid = %s", [friendid, userid])
                con.commit()

            case '3':
                log = input("Enter the common name of the bird: ")
                #find the bird
                birdid = findBirdId(cursor, log)
                if birdid == -1:
                    print("Name not found, it may have been typed wrong or it may not exist in the database \n")
                else:
                    date = input("Enter the date for the log: ")
                    addLog(cursor, userid, birdid, date)
            case '4':
                date = input("Enter the date of the log: ")
                viewLog(cursor, userid, date)
            case '5':
                #query for viewing friends
                cursor.execute("SELECT userinformation.username FROM userinformation JOIN friendlist ON userinformation.userid = friendlist.friendid WHERE %s = friendlist.userid", (userid,))
                print("Friend names: ")
                print(cursor.fetchall())
            case '6':
                #prompt for specific friend
                friendName = input("Enter the user name of your friend: ")
                #find that friendid and verify that they are friends with you
                #find their id based on the unique username
                cursor.execute("SELECT userid FROM userinformation WHERE username = %s", (friendName,))
                friendid = cursor.fetchone()
                #verify if they are friends with the logged in user
                cursor.execute("SELECT friendid FROM friendlist WHERE friendid = %s AND userid = %s", [friendid[0], userid])
                #if yes: prompt for date and display log
                if cursor.fetchone() is not None:
                    date = input("Enter the date of the log you wish to view: ")
                    viewLog(cursor, friendid, date)
                #if no: print that you entered someone you are not friends with
                else:
                    print("You are not friends with this person or the person does not exist")
            case '7':
                #query nLogs for this userid
                cursor.execute("SELECT nlogs FROM nbirdlogged WHERE userid = %s", (userid,))
                print("Number of birds: ")
                print(cursor.fetchone())
            case '8':
                #prompt for friend
                friendName = input("Enter the user name of your friend: ")
                #find that friendid and verify that they are friends with you
                #find their id based on the unique username
                cursor.execute("SELECT userid FROM userinformation WHERE username = %s", (friendName,))
                friendid = cursor.fetchone()
                #verify if they are friends with the logged in user
                cursor.execute("SELECT friendid FROM friendlist WHERE friendid = %s AND userid = %s", [friendid[0], userid])
                #verify they are friends
                if cursor.fetchone() is not None:
                    cursor.execute("SELECT nlogs FROM nbirdlogged WHERE userid = %s", (friendid[0],))
                    #query for nLogs for friend userid
                    print("Number of birds: ")
                    print(cursor.fetchone())
                else:
                    print("You are not friends with this person or the person does not exist")
            case '9':
                    print("Your User ID is ",userid)
                    
                

        

    #2 register
    #register:
    if option == '2':
        registered = False
        while registered == False:
            userNameReg = input("Type a username: ")
        #prompt for username: store it
            passwordReg = input("Type a password: ")
        #prompt for password: store it
        #call register and check status
            reg = register(cursor, userNameReg, passwordReg)
        #register fail, go agian
            if reg == 0:
                print("username already in user")
        #register complete return to main screen
            else:
                option = -1
                registered == True
                

cursor.close()
con.close()