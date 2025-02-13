import os
import discord
from wiki_assistant import Chatgpt
from wiki_embeddings import WikiContent
from dotenv import load_dotenv
from datetime import datetime

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
    try:
        print("ベクトルDBの状態を確認中...")
        vectorstore = WikiContent.get_vectorstore()
        # vectorstoreをChatgptクラスに設定
        Chatgpt.set_vectorstore(vectorstore)
        print("ベクトルDBの準備完了")

        # Bot起動
        client.run(token)

    except Exception as e:
        print(f"エラーが発生しました: {e}")