import socket
import os

host = "localhost"
port = 5000

def sendfile(name, s):
    
    f = open(name, 'rb')

    size = os.stat(name).st_size

    s.send( ("sendfile " + name + ' ' + str(size) ).encode() )

    resp = s.recv(1024).decode()

    if (resp != "ack"):
        
        print("Error")
        
    else:

        totalsize = size

        os.system('setterm -cursor off')

        print ( "file: " + name)

        while(size > 0 ):

            data = f.read(1024)

            s.send(data)

            resp = s.recv(1024).decode()

            if ( resp != "ack" ):
                print("Error")
                break

            size -= len(data)

            perc = ( 1 - ( size / totalsize ) ) * 100

            print(
                "\r%d" % ( perc ) + '%',
                "[" + int(perc/2) * '|' + int(( 100 - perc )/2) *' ' + "]",
                end = '\r'
                )

        print( "Done" )

        os.system('setterm -cursor on')

    f.close()


if __name__ == "__main__":

    s = socket.socket()
    s.connect((host, port))

    cur_dir = "/"

    while True:

        op = input( cur_dir + " > ")

        lop = op.split(" ")

        if( lop[0] == "sendfile" ):

            sendfile(lop[1], s)

            continue

        if( lop[0] == "cd" ):

            # go back #

            if lop[1].startswith("..") :

                t = cur_dir.split("/")

                while "" in t:
                    t.remove("")

                cur_dir = "/"

                if len(t) != 1:
                    for i in range(0, len(t) - 2):
                        cur_dir += "/" + t[i]

                lop[1] = (lop[1])[2:]

                if lop[1].startswith("/"):
                    lop[1] = (lop[1])[1:]

                if len(lop[1]) == 0:
                    lop[1] = "/"

            temp_dir = cur_dir

            if lop[1].startswith("/"):
                temp_dir = lop[1]
            else:
                temp_dir += lop[1]

            s.send( ("getdir " + temp_dir).encode() )

            res = s.recv(1024).decode()

            if res == "nack":
                print("Dir not found")
                continue

            cur_dir = temp_dir

            continue

        if( lop[0] == "ls"):

            s.send( ("getdir " + cur_dir).encode() )
            
            print(s.recv(1024).decode())
            
            continue

        if( lop[0] == "exit"):
            
            s.send("exit".encode())

            break

        print("comand " + op + " not found.")

    print("Closing connection")
    
    pass