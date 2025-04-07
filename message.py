import os
import discord
import asyncio
# from wiki_assistant import Chatgpt
# from wiki_embeddings import WikiContent
from dotenv import load_dotenv
from datetime import datetime
from app import keep_alive

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
client = discord.Client(intents=intents)


## Botの起動
@client.event
async def on_ready():
    print("Start")


# メッセージ受信時の処理
@client.event
async def on_message(message):
    # Bot自身のメッセージの場合は無視
    if message.author == client.user:
        return
    
    if client.user in message.mentions:
        print(message.content)
        # chatgpt = Chatgpt(message.content)
        # resMessage = chatgpt.resChatgpt()
        await message.channel.send("resMessage")


# DBチェック
def db_check():
    print("ベクトルDBの状態を確認中...")
    # vectorstore = WikiContent.get_vectorstore()
    # vectorstoreをChatgptクラスに設定
    # Chatgpt.set_vectorstore(vectorstore)
    print("ベクトルDBの準備完了")


if __name__ == '__main__':
    # DBチェック
    # db_check()

    # Web サーバの立ち上げ
    keep_alive()
    
    # Bot起動
    client.run(DISCORD_TOKEN)