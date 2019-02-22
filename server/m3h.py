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

    while "" in dirs:
        dirs.remove("")

    # resolts for dirs 

    curssor1 = data_base.cursor()

    curssor1.execute(
        "SELECT m.dirname FROM Dirs e INNER JOIN Dirs m ON m.dirloc = e.dircode WHERE e.dirname = 'root';"
    )

    r = curssor1.fetchall()

    ls = []

    for i in r:
        
        ls.append(i[0])

    for i in range(1,len(dirs)):

        if not dirs[i] in ls:
            
            s.send("nack".encode())
            
            return
        
        else:

            curssor1.execute(
                "SELECT m.dirname FROM Dirs e INNER JOIN Dirs m ON m.dirloc = e.dircode WHERE e.dirname = '" + dirs[i] + "';"
            )

            r = curssor1.fetchall()

            ls = []

            for i in r:
                ls.append(i[0])

    # get res to dirs #

    curssor1.execute(
        "SELECT m.dirname FROM Dirs e INNER JOIN Dirs m ON m.dirloc = e.dircode WHERE e.dirname = '" + dirs[len(dirs) - 1] + "';"
    )

    res1 = curssor1.fetchall()

    curssor1.execute(
        "SELECT fname FROM Dirs JOIN Files WHERE dircode = floc AND dirname = '" + dirs[len(dirs) - 1] + "';"
    )

    res2 = curssor1.fetchall()

    # join results 

    if len(res1) + len(res2) == 0:
        s.send("Empty".encode())
        return

    res = ""

    for r in res1:
        res += "/" + r[0] + " "

    for r in res2:
        res += r[0] + " "    

    s.send(res.encode())

    pass

def removefile(form, s, data_base):

    if (form[1].startswith("/")):
        form[1] = "root" + form[1]

    dr = form[1].split("/")

    while "" in dr:
        dr.remove("")

    print(dr)

    d = dr[len(dr) - 2]
    n = dr[len(dr) - 1]

    cusrsor = data_base.cursor()

    cusrsor.execute("SELECT id FROM Dirs JOIN Files WHERE dircode = floc AND dirname = '"+d+"' AND fname = '"+n+"';" )

    res = cusrsor.fetchall()

    print (res)

    for r in res:
        cusrsor.execute("UPDATE Files SET floc = '001' WHERE id = '" + r[0] + "';")
    data_base.commit()

    s.send("ack".encode())

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

        removefile(form, s, data_base)

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

        except Exception as e:

            print(e)

        print("Client Closed")

    pass