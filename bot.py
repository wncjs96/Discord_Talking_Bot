# bot.py
import os
import random
import re
import time

import discord

import requests

from dotenv import load_dotenv
import urllib
import json
import math

# personal files
import visualizer
import crawler

load_dotenv()
#env values
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
EMAIL = os.getenv('PINGPONG_EMAIL')
PASSWORD = os.getenv('PINGPONG_PASSWORD')
payload = {'email': EMAIL, 'password': PASSWORD}
MAX_LENGTH = 2000

intents = discord.Intents.all()
client = discord.Client(intents=intents)
response = requests.post('https://builder.pingpong.us/api/builder/user/login', data=payload)
cookie = response.headers['Set-Cookie']
headers = {'cookie': cookie}

# class var
state = 0
regex = re.compile('(.)*루다(.)*')
regex2 = re.compile('(.)*꺼져(.)*')

regex3 = re.compile('(.)*\.(.)*')

vis = visualizer.Vis()

@client.event
async def on_ready():
	print(f'{client.user} has connected to Discord!')
		
	for guild in client.guilds:
		if guild.name == GUILD:
			break
	print (
		f'{client.user} is connected to the following guild:\n'
		f'{guild.name}(id: {guild.id})\n'
	)
	
	members = '\n - '.join([member.name for member in guild.members])
	#print(f'Guild Members:\n - {members}')
	#print(guild.members)

@client.event
async def on_message(message):
	global state
	#print('message = ' + message.content)
	#print('state = ' + str(state))
	if message.author == client.user:
		return
	
	wakeup_quotes = [
		'일어났어요. 안녕하세요? 오랜만이에요.',
		'이루다 로봇. 출격준비 완료.',
		'일어났어요. 오랜만이에요',
		'이미 일어나 있거든? 왜 깨우고 그래!',
		'깨워줘서 고마워. 너무 춥고 어두웠어.',
		'반가워. 오랜만이야?',
		'응? 안녕안녕 오랜만!',
		'컨텐츠를 입력해주시기 바랍니다.',
		'반가워요.',
		'일어났습니다.'
	]	
	
	sleep_quotes = [
		'이루다 로봇, 활동 정지.',
		'이제 사라져줄게. 안녕.',
		'담에 또 봐요 안녕!'
	]
	#response = random.choice(wakeup_quotes)
	#await message.channel.send(response)
	#print(regex.match(message.content))
	# 이루다 is off

	# collection for messages sent	
	msgCollection = []

	if message.content.startswith('!vis'):
		# get second arg
		arg = (' ').join(message.content.split(' ')[1:])
		if(regex3.match(arg)):
			img = vis.getImg(arg)
			arr = vis.visualizeImg(img)
		else:
			nresults = crawler.google_image_search(arg)
			dir_name = arg
			file_name = arg + '/' + vis.getOrder() + '.png'
			print(file_name)
			arr = vis.visualizeImg2(file_name)
		row_length = len(arr[0])
		msg_threshold = int(MAX_LENGTH/row_length)
		msg_threshold = msg_threshold - math.ceil(msg_threshold/row_length)
		# check if 2000 >= row_length * msg_threshold + msg_threshold, if so, decrease msg_threshold by ceil(msg_threshold/row_length)
			
		curr = 0
		while (curr < len(arr)):
			joined_string = "\n".join(arr[curr:curr+msg_threshold])
			joined_string = joined_string + "\n"
			print(len(joined_string))
			curr = curr+msg_threshold
			msg = await message.channel.send(joined_string)
			msgCollection.append(msg)
		
		time.sleep(4)
		
		for msg in msgCollection:
			#print(msg)
			await msg.delete()
			
		
		#for i in arr:
		#	await message.channel.send(i)
	elif (message.content.startswith('!setNw')):
		arg = (' ').join(message.content.split(' ')[1:])
		temp = re.compile('^\d+$')
		
		if (temp.match(arg)):
			vis.setNw(int(arg))
			await message.channel.send('크기 설정 완료')		
	elif (message.content.startswith('!setOrder')):
		arg = (' ').join(message.content.split(' ')[1:])
		temp = re.compile('^\d+$')
		
		if (temp.match(arg)):
			vis.setOrder(arg)
			await message.channel.send('순서 설정 완료')		
		
		
	elif (state == 0):
		if(regex.match(message.content)):
			state = 1
			print('message received')
			response = random.choice(wakeup_quotes)
			await message.channel.send(response)
			#state = 0
	else:
		if(regex2.match(message.content)):
			state = 0
			response = random.choice(sleep_quotes)
			await message.channel.send(response)
			#state = 1
		else:
			# message.content goes into query
			url = 'https://builder.pingpong.us/api/builder/60383642e4b078d873a0ac13/chat/simulator?query=' + urllib.parse.quote(message.content)
			response = requests.get(url, headers=headers)
			
			res = json.loads(response.text)
			
			print(res)
			print(len(res['response']['replies']))
			
			#choice = 0
			choice = len(res['response']['replies'])-1
			await message.channel.send(res['response']['replies'][0]['reply'])
			if (choice != 0):
				await message.channel.send(res['response']['replies'][choice]['reply'])
		

	#		# instead of having it as dictionary, text is handled manually.. for emoji?
	#		count = 1
	#		temp = ''
	#		temp2 = ''
	#		n = response.text.find('reply')+7
	#		x = 0
	#		while (response.text[n+count] != '"'):
	#			if (x == 0):
	#				if (response.text[n+count] == '\\'):
	#					x = 1
	#					temp2 = temp2 + '\\'	
	#				else:
	#					temp = temp + response.text[n+count]
	#			else:
	#				if(response.text[n+count] == ' '):	
	#					x = 0
	#				else:
	#					temp2 = temp2 + response.text[n+count]
	#			count = count + 1

	#		await message.channel.send(temp)
			#TODO: add emoji
			#await message.add_reaction('')
				
client.run(TOKEN)
