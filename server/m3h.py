import socket
import select
import os
import mysql.connector 

IP = "localhost"
Port = 5000
StdDir = "Data/"

# Send File

def sendfile(form, s, data_base):
    name = form[1]

    size = int( form[2] )

    # data base #

    # get id 
    cursor1 = data_base.cursor()

    cursor1.execute("SELECT * FROM Files")

    i = len( cursor1.fetchall() )

    ic = "%03d" % (i)

    # set file 
    cursor2 = data_base.cursor()

    sql = "INSERT INTO Files VALUES (%s, %s, %s)"
    vls = (ic, name, "000")

    cursor2.execute(sql, vls)

    data_base.commit()

    #recv file

    f = open( StdDir + name, 'wb+')

    s.send("ack".encode())

    while(size > 0 ):

        data = s.recv(1024)

        f.write(data)

        size -= len(data)

        s.send("ack".encode())

    f.close()

# Get Dir

def getdir(dirs, s, data_base):

    if dirs.startswith("/"):
        dirs = "root" + dirs

    dirs = dirs.split("/")

    # resolts for dirs 

    curssor1 = data_base.cursor()

    curssor1.execute(
        "SELECT m.dirname FROM Dirs e INNER JOIN Dirs m ON m.dirloc = e.dircode WHERE e.dirname = '" + dirs[len(dirs) - 2] + "';"
    )

    res1 = curssor1.fetchall()

    # resolts for files 

    curssor2 = data_base.cursor()

    curssor2. execute("SELECT fname FROM Dirs NATURAL JOIN Files WHERE dirname = '" + dirs[len(dirs) - 2] + "';")
    
    res2 = curssor2.fetchall()

    # join results 

    if len(res1) == 0 and len(res2) == 0:
        s.send("nack".encode())
        return

    res = ""

    for r in res1:
        res += r[0] + " "

    for r in res2:
        res += r[0] + " "    

    s.send(res.encode())

    pass


# Manage Interfaces

def interface(s, data_base):

    msg = s.recv(1024).decode()

    form = msg.split(' ')

    if( form[0] == "sendfile" ):

        print("Client Send File")

        sendfile(form, s, data_base)

        print("Done Sending")

    elif( form[0] == "remove" ):

        print("Client Remove File")

        #removefile(form, s, data_base)

        print("Done Removing")

    elif( form[0] == "getdir" ):

        print("Client GetDir File")

        getdir( form[1], s, data_base)

        print("Done GetDirs")

    elif form[0] == "exit":

        s.close()

    else:
        
        s.send("Command not found".encode())

    pass

if __name__ == "__main__":
    
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socket_server.bind(("0.0.0.0", Port))
    socket_server.listen(10)

    ports = {}

    # data base #

    data_base = mysql.connector.connect(

        host = "localhost",
        user = "bot",
        passwd = "botpass",
        database = "Files"

    )

    print(data_base)

    # dirs #

    if not os.path.exists(StdDir):
        os.makedirs(StdDir)

    # server #

    while True:
       
        print("Waiting...")

        s, addr = socket_server.accept()

        print("Client From: " + str(addr))

        try:

            while True:

                interface(s, data_base)

        except:

            pass

        print("Client Closed")

    pass