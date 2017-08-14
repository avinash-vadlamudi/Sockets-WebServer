from socket import *
import threading
import os
import sys
import json
import datetime
import time

s1_dir = os.path.dirname(os.path.realpath(__file__))
global array
global len_array
global cur_time

array=[]
array = list(array)
cur_time = time.time()
len_array = 0

class CreateThread(threading.Thread):
	def __init__(self,connect,address):
		threading.Thread.__init__(self)
		self.conn_sock = connect
		self.addr = address
		self.flag = 1

	def run(self):

		global len_array
		global array
		global cur_time

		array = list(array)

		try:
			while True:
				data = conn_sock.recv(2048)
				if not data:
					break

				blocks = data.split('\n\r\n')
				header1 = blocks[0].split('\n')
				inputs = header1[0].split()

				p=0
				flag2 = 0
				while(p < len_array ):
					if array[p][0][0] == self.addr[0]:
						self.flag = array[p][1]
						flag2 =1
						array[p][2]+=1
						break
					p+=1

				if flag2 == 0:
					array.append([addr,2,1,cur_time])
					len_array+=1

				print array				
				if cur_time-array[p][3]>60:
					array[p][3]=cur_time
					array[p][1]=1
					array[p][2]=1

				if array[p][2]>15:
					message = 'HTTP/1.1 200 OK\r\n\r\n'
					conn_sock.send(message)
					message2 = '<html><head><title>Welcome</title></head>'
					message3 = '<body><h1>This IP has been blocked</h1></body>'
					conn_sock.send(message2+message3)
					conn_sock.close()
					break

				if inputs[0]=='GET' and array[p][1]==2:
					array[p][1]=1
					self.flag = 1

				if self.flag == 1:

					message = 'HTTP/1.1 200 OK\r\n\r\n'
					conn_sock.send(message)
					path1 = s1_dir + '/auth.html'
					f = open(path1,'rb')
					l = f.read(2048)
					while(l):
						conn_sock.send(l)
						l = f.read(2048)
					f.close()
					self.flag = 2
					print self.flag
					array[p][1]=2
					conn_sock.close()
					break
				elif self.flag == 2:
					info = blocks[1]
					print info
					values = info.split('&')
					identifier = values[2]
					net_value = values[0]+';'+values[1]+'\n'
					print net_value
					if net_value == 'username=;password=\n' or net_value.split(';')[1]=='password=\n' or net_value.split(';')[0]=='username=':
						identifier = 'submit=SIGN_IN'

					if identifier == 'submit=SIGN_UP':
						f = open('ip.logs','r')
						flag2 = 0
						l = f.readlines()
						f.close()
						for line in l:
							if line.split(';')[0] == net_value.split(';')[0]:
								flag2 =1
								break
						if flag2 ==1:
							array[p][1]=2
							message = 'HTTP/1.1 200 OK\r\n\r\n'
							conn_sock.send(message)
							path1 = s1_dir + '/auth.html'
							f = open(path1,'rb')
							l = f.read(2048)
							while(l):
								conn_sock.send(l)
								l = f.read(2048)
							f.close()
							message = '<html><body>Already present Username or password</body></html>'
							conn_sock.send(message)
							conn_sock.close()
							break
						else:
							f = open('ip.logs','a+')
							f.write(net_value)
							array[p][1]=0
							f.close()
					else:
						f = open('ip.logs','r')
						flag2 = 0
						l = f.readlines()
						print l
						f.close()
						for line in l:
							if line == net_value:
								flag2 =1
								break
						if flag2 ==1:
							array[p][1]=0
						else:
							array[p][1]=2
							message = 'HTTP/1.1 200 OK\r\n\r\n'
							conn_sock.send(message)
							path1 = s1_dir + '/auth.html'
							f = open(path1,'rb')
							l = f.read(2048)
							while(l):
								conn_sock.send(l)
								l = f.read(2048)
							f.close()
							message = '<html><body>Invalid login</body></html>'
							conn_sock.send(message)
							conn_sock.close()
							break

					inputs[0] = 'GET'
					self.flag = 0


				if inputs[0] == 'GET':


					filename = inputs[1]
					if filename == '/s2.py':
						message = 'HTTP/1.1 403 Forbidden Status\r\n\r\n'
						message2 = '<html><body><h1>Permission Denied</h1></body></html>'
						conn_sock.send(message+message2)
						conn_sock.close()
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
						conn_sock.close()
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
							conn_sock.close()
							break

						else:
							message = 'HTTP/1.1 403 Forbidden Status\r\n\r\n'
							conn_sock.send(message)

							message = '<html><head><title>Welcome '+str(addr)+'</title></head>'
							message2 = '<body><h1>Permission Denied</h1></body></html>'
							conn_sock.send(message + message2)
							conn_sock.close()
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
					conn_sock.close()
					break

				elif inputs[0] == 'PUT':
					filename = inputs[1]
					if filename == '/s2.py':
						message = 'HTTP/1.1 403 Forbidden Status\r\n\r\n'
						message2 = '<html><body><h1>Permission Denied</h1></body></html>'
						conn_sock.send(message+message2)
						conn_sock.close()
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
						conn_sock.close()
						break
					else:
						f = open(path,'wb')
						f.write(blocks[1])
						f.close()
						message = 'HTTP/1.1 201 Created\r\n\r\n'
						message2 = '<html><head><title>Welcome</title></head><body><h1>File Successfully Created</h1></body></html>'
						conn_sock.send(message+message2)
						conn_sock.close()
						break
			
					print path + ':\n' + blocks[1] + '\n'

		except:
			print "some error occured"
			print data

		# conn_sock.close()


sock = socket(AF_INET,SOCK_STREAM)
port = 56789
host = ''
sock.bind((host,port))
sock.listen(20)

threads = []

while True:
	cur_time = time.time()
	conn_sock,addr = sock.accept()
	sub_thread = CreateThread(conn_sock,addr)
	sub_thread.start()
	threads.append(sub_thread)

sock.close()

