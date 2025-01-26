import os
import discord
from wiki_assistant import Chatgpt
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TOKEN")

intents = discord.Intents.default()
client = discord.Client(intents=intents)


## Botの起動
@client.event
async def on_ready():
    print('Start')


# メッセージ受信時の処理
@client.event
async def on_message(message):
    # Bot自身のメッセージの場合は無視
    if message.author == client.user:
        return
    
    if client.user in message.mentions:
        print(message.content)
        chatgpt = Chatgpt(message.content)
        resMessage = chatgpt.resChatgpt()
        await message.channel.send(resMessage)



if __name__ == '__main__':
    # Bot起動
    client.run(token)
