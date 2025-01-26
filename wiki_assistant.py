from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from wiki_embeddings import WikiContent


class Chatgpt():
    # クラス変数としてvectorstoreを保持
    _vectorstore = None

    def __init__(self, message):
        self.message = message
        # vectorstoreが未初期化の場合のみ実行
        if Chatgpt._vectorstore is None:
            Chatgpt._vectorstore = WikiContent.get_vectorstore()

    def resChatgpt(self):
        # ChatGPTモデルの設定
        llm = ChatOpenAI(model="gpt-4o-mini")

        # RAGチェーンの作成
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=self._vectorstore.as_retriever(search_kwargs={"k": 3}),
            return_source_documents=True,
        )

        # 質問と回答
        result = qa_chain({"question": self.message, "chat_history": []})

        return result["answer"]
    

if __name__ == "__main__":
    # テスト用
    test_text = input("質問を書いてください：")
    chatbot = Chatgpt(test_text)
    response = chatbot.resChatgpt()
    print('回答：', response)
    print('-' * 50)