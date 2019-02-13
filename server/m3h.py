import socket
import select

IP = "localhost"
Port = 5000

def interface(s):

    msg = s.recv(1024).decode()

    if( msg.startswith("sendfile") ):

        name = msg.remove("sendfile ")

        s.send("ack".encode())

    else:
        s.send("Command not found".encode())

    s.close()

    pass

if __name__ == "__main__":
    
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socket_server.bind(("0.0.0.0", Port))
    socket_server.listen(10)
    socket_server.setblocking(0)

    socket_list = []
    socket_list.append(socket_server)

    ports = {}

    while True:

        for s in socket_list:
            if s.fileno() < 0:
                socket_list.remove(s)
                print("Client Closed: " + str(len(socket_list)-1))

        rsock,_,_ = select.select(socket_list,[],[],5)

        for s in rsock:
            if s == socket_server:
                ns,_ = s.accept()
                ns.setblocking(0)
                socket_list.append(ns)
                print("New Client: " + str(len(socket_list)-1))
            else:
                interface(s)

    pass