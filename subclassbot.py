# bot.py
import os
import random
import re

import discord

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

#intents = discord.Intents.all()
#client = discord.Client(intents=intents)

class CustomClient(discord.Client):
	# class var
	state = 0
	onReg = '이루다.'
	#def __init__(client, **options):
	#	super().__init__(**options)

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
		print(f'Guild Members:\n - {members}')
		print(guild.members)
	
	async def on_message(message):
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
	
		if state == 0 and re.search(message.content, onReg):
			state = 1
			print('message received')
			response = random.choice(wakeup_quotes)
			await message.channel.send(response)
def main():
	intents = discord.Intents.all()
	#client = discord.Client(intents=intents)
	instance = CustomClient(intents=intents)
	instance.run(TOKEN)
	#client.run(TOKEN)

if __name__ == "__main__": main()

