import socket
import os

host = "localhost"
port = 5000

def sendfile(filename, s):
    
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

    name = input("file name: ")

    sendfile(name, s)

    s.close()
    
    pass