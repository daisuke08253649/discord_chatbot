# Discordで使えるChatbot
## 参考
* https://python.langchain.com/docs/tutorials/rag/
* https://qiita.com/tinymouse/items/4d359674f6b2494bb22d
* https://github.com/kitadakyou/PyBacklogPy

# 仕様
* Botにメンションをつけてテキストを送信するとレスポンスが返ってくる。
* backlogのwikiの内容について質問するとAIがDBを検索してレスポンスが返ってくる。(RAGを使用)

# DBの更新について
* ソースコード（message.py）を実行したとき、先にDB更新の必要の有無を確認。更新の必要があれば自動で更新される。
* DBの更新が終わったらBotが実行されて使えるようになる。
※更新の必要が無ければそのままBotが実行される。

# 現在の状況
* discordの個人サーバーで実験中
* OpenAIのAPI keyは個人で用意したものを使用中