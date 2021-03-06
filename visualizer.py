import cv2
import youtube_dl
import sys
import io
import threading
from pynput import keyboard
import time

import requests
from PIL import Image as Img
from io import BytesIO
import numpy

#CHARS = ' .,-~:;=!*#$@' # 13
CHARS = '⠄⠆⠖⠶⡶⣩⣪⣫⣾⣿' # 11
#CHARS = ' ⠆⠶⣩⣫⣿' # 11

nw = 30
flag = 0
result_available = threading.Event()	

def getImg(url):
	# from url, get image content in bytes
	request = requests.get(url)
	stream = BytesIO(request.content)
	image = Img.open(stream).convert('RGBA')
	return image

def visualizeImg(pilImage):
	# when read directly as cv2 image, it's in BGR
	#img = cv2.imread('test.jpg')
	#img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	# when read from pil Image, needs to be converted accordingly (which is it in RGBA)
	img = cv2.cvtColor(numpy.array(pilImage), cv2.COLOR_RGB2GRAY)

	h,w = img.shape
	
	nh = int(h/w*nw)
	
	img = cv2.resize(img, (nw, nh))
	count = 0
	array = []
	for row in img:
		temp = ''
		for pixel in row:
			index = int(pixel / 256 * len(CHARS))
			temp = temp + (CHARS[index])
		array.append(temp)
		count = count + 1
		#print()
	return array

def visualizeVid():
	# TODO: need to fix
	cv2.startWindowThread()
	cv2.namedWindow('ImageWindow')
				
	sys.stdout = io.TextIOWrapper(sys.stdout.detach(),encoding = 'utf-8')
	sys.stderr = io.TextIOWrapper(sys.stderr.detach(),encoding= 'utf-8')

	cap = cv2.VideoCapture('test.mp4')
	
	print("\x1b[2J", end='')
	while cap.isOpened():
		#print('read')
		ret, img = cap.read()
	
		if not ret:
			break

		img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		
		h, w = img.shape

		nh = int(h/w*nw)

		img2 = cv2.resize(img, (nw*2,nh))	

		for row in img2:
			for pixel in row:
				index = int(pixel / 256 * len(CHARS))
				print(CHARS[index], end='')
			print()
		if (flag == 1):
			cv2.imwrite("frame.jpg", img)
			cv2.imshow('ImageWindow', img)
			cv2.waitKey(0)
			result_available.wait()
		#while (flag == 1):
		#	time.sleep(1)
		print('\x1b[H', end='')
	return

def downloader(link):
	ydl = youtube_dl.YoutubeDL({'outtmpl': 'test.mp4'})

	with ydl:
		ydl.download([link])
	return


def on_press(key):
	global flag
	if (key == keyboard.Key.f9):
		flag = not flag		
		if (flag == 0):
			result_available.set()
			result_available.clear()	
	return


def main():
	request = getImg('https://static01.nyt.com/images/2020/04/27/us/politics/00-trump-cand-page/00-trump-cand-page-videoSixteenByNineJumbo1600.jpg')
	array = visualizeImg(request)
	joined_string = "\n".join(array)
	print(joined_string)
	#link = input("Copy & paste the youtube URL:- ")
	#downloader(link.strip())
	#for i in array:
	#	print(i)
	#listener = keyboard.Listener(on_press=on_press)
	#listener.start()
	#visualizeVid()
		

if __name__ == '__main__':
	main()

