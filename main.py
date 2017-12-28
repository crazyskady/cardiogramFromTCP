#! /usr/bin/env python
# _*_ coding: utf-8 _*_

# Author: crazyskady@sina.com

import threading
import queue
import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from tcpModule import *

data_queue = queue.Queue()  # This is a FIFO queue to save the data from tcp/ip

def serverRecvCallback(data):
	data_queue.put(json.loads(data))
	return

def serverSendCallback():
	return "OK"

def createTcpServer():
	tcpServer = TcpServer(recvCallback=serverRecvCallback, sendCallback=serverSendCallback)
	tcpServer.startServer()
	tcpServer.listenLoop()  # Seems no need to closed in this example. >_<

def data_gen():
	counter = 0
	while True:
		data = 0
		if False == data_queue.empty():
			rawData = data_queue.get()
			data = rawData["value"]
		else:
			print("queue is empty")
		yield counter, data
		counter += 1

def run(data):
	t, y = data
	xmin, xmax = ax.get_xlim()	
	if t >= xmax:
		del ydata[0]
		ydata.append(y)
	else:
		xdata.append(t)
		ydata.append(y)
	line.set_data(xdata, ydata)	
	return line,

if __name__ == '__main__':
	tcpThread = threading.Thread(target=createTcpServer)
	tcpThread.start()	

	# init GUI
	fig, ax = plt.subplots()
	line, = ax.plot([], [], lw=1)
	ax.set_ylim(-2.0, 2.0)
	ax.set_xlim(0, 800)
	ax.grid()
	xdata, ydata = [], []
	
	# start GUI
	ani = animation.FuncAnimation(fig, run, data_gen, blit=True, interval=2, repeat=False)
	plt.show()