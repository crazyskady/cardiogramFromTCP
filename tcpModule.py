#! /usr/bin/env python
# _*_ coding: utf-8 _*_

# This file implement TCP/IP server & client class
# Author: crazyskady@sina.com

from socket import *
from optparse import OptionParser
import sys

from time import ctime

DEFAULT_LOCAL_HOST = 'localhost'
DEFAULT_PORT       = 21567
DEFAULT_BUFSIZE    = 1024

class TcpBase(object):
	def __init__(self, host, port, bufSize):
		self.addr = (host, port)
		self.sock = socket(AF_INET, SOCK_STREAM)
		self.bufSize = bufSize

	def getSockIf(self):
		return self.sock

class TcpServer(TcpBase):
	def __init__(self, port=DEFAULT_PORT, bufSize=DEFAULT_BUFSIZE, maxConnection=100, recvCallback=None, sendCallback=None):
		super(TcpServer, self).__init__('', port, bufSize)  # Server don't need to set host
		self.currentClientSock = None
		self.maxConnection = maxConnection
		self.recvCallback = recvCallback
		self.sendCallback = sendCallback

	def startServer_Test(self):
		self.startServer()	

		print('Waiting for connection...')
		self.currentClientSock, addr = self.sock.accept()
		print('...connected from: ', addr)
		while True:
			data = str(self.currentClientSock.recv(self.bufSize), encoding='utf-8')
			if not data:
				break

			self.currentClientSock.send(bytes('[%s]: %s'%(ctime(), data), 'utf-8'))

	def closeServer_Test(self):
		self.closeServer()

	def startServer(self):
		self.sock.bind(self.addr)
		self.sock.listen(self.maxConnection)
		
	def closeServer(self):
		self.sock.close()
		if self.currentClientSock != None:
			self.currentClientSock.close()
			self.currentClientSock = None

	def listenLoop(self):
		while True:
			print('Waiting for connection...')
			self.currentClientSock, addr = self.sock.accept()
			print('...connected from: ', addr)
			while True:
				#try:
				data = str(self.currentClientSock.recv(self.bufSize), encoding='utf-8')
				if not data:
					print("Received Data ERROR.")
					break	
				if self.recvCallback != None:
					self.recvCallback(data)		
				if self.sendCallback != None:
					sendData = self.sendCallback()
					self.currentClientSock.send(bytes(sendData, 'utf-8'))
				#except:
					#break
			self.currentClientSock.close()
			self.currentClientSock = None
		return

class TcpClient(TcpBase):
	def __init__(self, host=DEFAULT_LOCAL_HOST, port=DEFAULT_PORT, bufSize=DEFAULT_BUFSIZE, maxConnection=100, recvCallback=None):
		super(TcpClient, self).__init__(host, port, bufSize)
		self.recvCallback = recvCallback

	def startClient_Test(self):
		self.startClient()
		while True:
			data = input('> ')
			if not data:
				break		

			self.sock.send(bytes(data, 'utf-8'))
			data = self.sock.recv(self.bufSize)
			if not data:
				break
			print(str(data, encoding='utf-8'))

	def closeClient_Test(self):
		self.closeClient()

	def startClient(self):
		print(self.addr)
		self.sock.connect(self.addr)

	def closeClient(self):
		self.sock.close()

	def sendData(self, data):
		self.sock.send(bytes(data, 'utf-8'))
		retData = str(self.sock.recv(self.bufSize), encoding='utf-8')
		if not retData:
			print("Server don't return any data!")
			return False
		if self.recvCallback != None:
			self.recvCallback(retData)
		return True

if __name__ == '__main__':
	parser = OptionParser(usage="%prog [-s] | [-c]", version="%prog 1.0")
	parser.add_option("-s", "--server", dest="_startServer", action="store_true", default=False, help="Start a tcp server")
	parser.add_option("-c", "--client", dest="_startClient", action="store_true", default=False, help="Start a tcp client")
	parser.add_option("-t", "--host",   dest="_host",        default=DEFAULT_LOCAL_HOST,         help="Set host for TCP/IP client")
	parser.add_option("-p", "--port",   dest="_port",        default=DEFAULT_PORT,               help="Set port for TCP/IP")
	parser.add_option("-b", "--bsize",  dest="_buffersize",  default=DEFAULT_BUFSIZE,            help="Set buffer size for TCP/IP")

	(options, args) = parser.parse_args()

	# Here should add some parameters validation
	if options._startServer == True and options._startClient == False:
		s = TcpServer(options._port, options._buffersize)
		s.startServer_Test()
		s.closeServer_Test()
	elif options._startServer == False and options._startClient == True:
		c = TcpClient(options._host, options._port, options._buffersize)
		c.startClient_Test()
		c.closeClient_Test()
	else:
		print("You need to start one and only one Server or Client.")

	sys.exit(0)