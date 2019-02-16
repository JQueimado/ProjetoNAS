import socket
import select

IP = "localhost"
Port = 5000
StdDir = "Data/"

def interface(s):

    msg = s.recv(1024).decode()

    form = msg.split(' ')

    if( form[0] == "sendfile" ):

        print("Client Send File")

        name = form[1]

        size = int( form[2] )

        f = open( StdDir + name, 'wb+')

        s.send("ack".encode())

        while(size > 0 ):

            data = s.recv(1024)

            f.write(data)

            size -= len(data)

            s.send("ack".encode())

        f.close()

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

    while True:
       
        s, addr = socket_server.accept()

        print("Client From: " + str(addr))

        interface(s)

        print("Client Closed")

    pass