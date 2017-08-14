from socket import *
import datetime
import threading
import os
import sys
import json

s1_dir = os.path.dirname(os.path.realpath(__file__))

class CreateThread(threading.Thread):
	def __init__(self,connect,address):
		threading.Thread.__init__(self)
		self.conn_sock = connect
		self.addr = address

	def run(self):
		try:

			while True:
				data = conn_sock.recv(2048)
				if not data:
					break


				blocks = data.split('\n\r\n')
				header1 = blocks[0].split('\n')
				inputs = header1[0].split()


				if inputs[0] == 'GET':

					filename = inputs[1]
					if filename == '/s2.py':
						message = 'HTTP/1.1 403 Forbidden Status\r\n\r\n'
						message2 = '<html><body><h1>Permission Denied</h1></body></html>'
						conn_sock.send(message+message2)
						break
					
					flag = 0
					path = s1_dir+filename
					if os.path.isfile(path):
						message = 'HTTP/1.1 200 OK\r\n\r\n'
					else:
						message = 'HTTP/1.1 404 Not Found\r\n\r\n'
						conn_sock.send(message)
						flag = 1

					if flag == 1:
						message = '<html><head><title>Welcome'+str(addr)+'</title></head>'
						message2 = '<body><h1>404 NOT FOUND</h1></body>'
						conn_sock.send(message+message2)
						break

					else:
						if os.access(path,os.R_OK):
							f = open(path,'rb')
							output = f.read()
							f.close()
							message = 'HTTP/1.1 200 OK\r\n'
							time = datetime.datetime.now()
							messages2 = 'Content-Length:'+str(len(output))+'\r\n'+'Keep-Alive:'+'timeout=10,max=100'+'\r\n'+'Connection:Keep-Alive\r\n\r\n'
							conn_sock.send(message+messages2)

							f = open(path,'rb')
							l = f.read(2048)
							while(l):
								conn_sock.send(l)
								l = f.read(2048)
							f.close()
							break

						else:
							message = 'HTTP/1.1 403 Forbidden Status\r\n\r\n'
							conn_sock.send(message)

							message = '<html><head><title>Welcome '+str(addr)+'</title></head>'
							message2 = '<body><h1>Permission Denied</h1></body></html>'
							conn_sock.send(message + message2)
							break




				elif inputs[0] == 'POST':

					length = len(blocks)
					poi = 1

					while poi<length:
						header = blocks[poi].split('\n')
						len2 = len(header)
						if len2 == 3:
							line2 = header[1].split('; ')
							len3 = len(line2)
							if len3 == 3:
								values = line2[2].split('\"')
								filename = values[1]

								f = open(filename,'wb')
								f.write(blocks[poi+1])
								f.close()

								print filename + ':\n' + blocks[poi+1] + '\n\n'
						poi = poi+2


					message = 'HTTP/1.1 200 OK\r\n\r\n'
					message2 = '<html><head><title>Welcome</title></head><body><h1>Posted Successfully</h1></body></html>'
					conn_sock.send(message + message2)
	#				conn_sock.close()
					break

				elif inputs[0] == 'PUT':
					filename = inputs[1]
					if filename == '/s2.py':
						message = 'HTTP/1.1 403 Forbidden Status\r\n\r\n'
						message2 = '<html><body><h1>Permission Denied</h1></body></html>'
						conn_sock.send(message+message2)
						break

					flag = 0
					path = s1_dir+filename
					if os.path.exists(path):
						os.chmod(path,0664)
						message = 'HTTP/1.1 201 Created\r\n\r\n'
						f = open(path,'wb')
						f.write(blocks[1])
						f.close()
						message2 = '<html><head><title>Welcome</title></head><body><h1>File Successfully Created</h1></body></html>'
						conn_sock.send(message+message2)
						break
					else:
						f = open(path,'wb')
						f.write(blocks[1])
						f.close()
						message = 'HTTP/1.1 201 Created\r\n\r\n'
						message2 = '<html><head><title>Welcome</title></head><body><h1>File Successfully Created</h1></body></html>'
						conn_sock.send(message+message2)
						break

					print path + ':\n' + blocks[1] + '\n'
		except:
			print "some error occured"

		conn_sock.close()

sock = socket(AF_INET,SOCK_STREAM)
port = 5689
host = ''
sock.bind((host,port))
sock.listen(20)

threads = []

while True:
	conn_sock,addr = sock.accept()
	sub_thread = CreateThread(conn_sock,addr)
	sub_thread.start()
	threads.append(sub_thread)

sock.close()

