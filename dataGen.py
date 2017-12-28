#! /usr/bin/env python
# _*_ coding: utf-8 _*_

# Thie file will read "data.txt" and send the data via TCP/IP client.
# Sent data structure is JSON

# Author: crazyskady@sina.com

from tcpModule import *
import json
import time

# Just an example, if file is very large, should use generator(yield)
def getDataFromFile(filename):
	fn = open(filename, 'r')
	datas_str = fn.readlines()
	fn.close()
	datas = []
	for data_str in datas_str:
		tmpStr = data_str.replace("\t", "").replace("  ", " ").strip().split(" ")
		idx = int(tmpStr[0])
		value = float(tmpStr[1])
		datas.append({"index":idx, "value":value})

	return datas

def serverReturnCallback(data):
	pass

# send one json to tcp server per 2 ms
def sendDataPer2ms(datas):
	tcpClient = TcpClient(recvCallback=serverReturnCallback)
	tcpClient.startClient()

	for idx, dic in enumerate(datas):
		data = json.dumps(dic)
		print(data)
		tcpClient.sendData(data)
		time.sleep(0.002)  # 2ms

	tcpClient.closeClient()

if __name__ == '__main__':
	sendDataPer2ms(getDataFromFile('data.txt'))