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

            temp_dir = cur_dir

            if lop[1].startswith("/"):
                temp_dir = lop[1]
            else:
                temp_dir += lop[1]

            dir_arr = temp_dir.split("/")

            dir_send = "/"

            flag = True

            for d in dir_arr:
                dir_send += d + "/"

                s.send( ("getdir " + dir_send).encode() )

                res = s.recv(1024).decode()

                if res == "nack":
                    flag = False
                    break 
                
            if flag:
                cur_dir = temp_dir
            else:
                print("Dir Not Found")

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