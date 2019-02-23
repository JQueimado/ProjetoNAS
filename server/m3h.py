import socket
import select
import os
<<<<<<< HEAD
import mysql.connector
=======
import mysql.connector 
>>>>>>> dfdbd41c75919941d043734eef7e6360fc61eadf

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

def getdir(dir, s, data_base):

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

    else:
        
        s.send("Command not found".encode())

    s.close()

    pass

if __name__ == "__main__":
    
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socket_server.bind(("0.0.0.0", Port))
    socket_server.listen(10)

    ports = {}

<<<<<<< HEAD
    # sql # 

    database = mysql.connector.connect(

        host = "192.168.0.15",
        user = "bot",
        passwd = "botpass"

    )

    cursor = database.cursor()

    

    cursor.execute("SHOW DATABASES")

    for x in cursor:
        print(x)
=======
    # data base #

    data_base = mysql.connector.connect(

        host = "localhost",
        user = "bot",
        passwd = "botpass",
        database = "Files"

    )

    print(data_base)
>>>>>>> dfdbd41c75919941d043734eef7e6360fc61eadf

    # dirs #

    if not os.path.exists(StdDir):
        os.makedirs(StdDir)

    # server #

    while True:
       
        print("Waiting...")

        s, addr = socket_server.accept()

        print("Client From: " + str(addr))

        interface(s, data_base)

        print("Client Closed")

    pass