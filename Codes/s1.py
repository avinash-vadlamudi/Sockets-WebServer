import socket
import os
sock = socket.socket()
host= ''
port = 5678
sock.bind((host,port))
sock.listen(10)
s1_dir = os.path.dirname(os.path.realpath(__file__))
while True:
    try:
        conn,addr = sock.accept()
        data = conn.recv(2048)
        print data
    except:
        conn.close()
        continue
    datas = data.split('\n')
    inputs = datas[0].split()
    filename = inputs[1]
    flag=0
    path = s1_dir + filename
    try:
        if os.path.isfile(path):
            message = 'HTTP/1.1 200 OK\n\n'
            conn.send(message)
        else:
            message = 'HTTP/1.1 404 Not Found\n\n'
            conn.send(message)
            flag=1
    except:
        conn.close()
        continue
    try:
        if flag==1:
            message = '<html><head><title>Welcome '+str(addr)+'</title></head>'
            message2= '<body><h1>404 NOT FOUND</h1></br></body></html>'
            conn.send(message+message2)
        else:
            if os.access(path,os.R_OK):
                f = open(path,'rb')
                l = f.read(2048)
                while(l):
                    conn.send(l)
                    l = f.read(2048)
                f.close()
            else:
                message = '<html><head><title>Welcome '+str(addr)+'</title></head>'
                message2= '<body><h1>Permission Denied</h1></body></html>'
                conn.send(message+message2)
    except:
        conn.close()
        continue
    conn.close()
