import discord
import os
from dotenv import load_dotenv
from keep_alive import keep_alive
from wiki_assistant import Chatgpt
from wiki_embeddings import WikiContent

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print('ログインしました')

@client.event
async def on_message(message):
    # 自身が送信したメッセージには反応しない
    if message.author == client.user:
        return

    if client.user in message.mentions:
        print(message.content)
        chatgpt = Chatgpt(message.content)
        resMessage = chatgpt.resChatgpt()
        await message.channel.send(resMessage)



print("ベクトルDBの状態を確認中...")
vectorstore = WikiContent.get_vectorstore()
Chatgpt.set_vectorstore(vectorstore)
print("ベクトルDBの準備完了")

# Web サーバの立ち上げ
keep_alive()

# Bot起動
client.run(TOKEN, reconnect=True)