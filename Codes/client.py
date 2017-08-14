import socket
import sys
try:
    req_type = sys.argv[1];
    host = sys.argv[2];
    port = sys.argv[3];
    filename = sys.argv[4];
except:
    print 'Follow the format given in README';
    exit(1);
def get():
    client = socket.socket();
    try:
        client.connect((host,int(port)));
    except:
        print 'Server busy/ not available. Try later'
        client.close();
        exit();
    header = 'GET /%s HTTP/1.1\r\n\r\n' %(filename);
    try:
        client.send("%s" %(header));
        response_message = client.recv(2048);
        final = "";
        while response_message:
            final += response_message;
            response_message = client.recv(2048);
        client.close();
    except:
        print 'Error in GET';
        exit();
    print final;
    return
def postput():
    client = socket.socket();
    try: 
        client.connect((host,int(port)));
    except:
        print 'Server busy. Try later'
        client.close();
        exit();
    if req_type == "POST":
        header = 'POST /%s HTTP/1.1\r\n\r\n' %(filename);
    elif req_type == "PUT":
        header = 'PUT /%s HTTP/1.1\r\n\r\n' %(filename);
    try:
        f = open(filename,'rb');
    except:
        print 'Can\'t open the given file';
        exit(1);
    client.send("%s" %(header));
    try:
        l = f.read(2048);
        while(l):
            client.send(l);
            l = f.read(2048);
        f.close();
        response_message = client.recv(2048);
        final = "";
        while response_message:
            final += response_message;
            response_message = client.recv(2048);    
        client.close();
    except:
        print 'Error in POST/PUT';
        exit(1);
    print final
    return
if req_type == "GET":
    get();
elif req_type == "POST" or req_type == "PUT":
    postput();
else:
    print 'Only GET/POST/PUT requests can be sent'
