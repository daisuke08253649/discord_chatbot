from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
import time

class Chatgpt():
    _vectorstore = None
    _qa_chain = None

    @classmethod
    def set_vectorstore(cls, vectorstore):
        # vectorstoreを設定するクラスメソッド
        cls._vectorstore = vectorstore

        llm = ChatOpenAI(model="gpt-4o")
        # RAGチェーンの作成
        cls._qa_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=cls._vectorstore.as_retriever(search_kwargs={"k": 3}),
            return_source_documents=True,
        )

    def __init__(self, message):
        self.message = message
        if Chatgpt._vectorstore is None or Chatgpt._qa_chain is None:
            raise ValueError("vectorstore または qa_chain が初期化されていません")

    def resChatgpt(self):
        start = time.time() # 開始時間
        # 質問と回答
        result = Chatgpt._qa_chain({
            "question": self.message,
            "chat_history": []
        })

        end = time.time() # 終了時間
        response_time = f"回答処理時間: {end - start:.2f}秒"

        return result["answer"], response_time
    

if __name__ == "__main__":
    test_text = input("質問を書いてください：")
    chatbot = Chatgpt(test_text)
    response = chatbot.resChatgpt()
    print('回答：', response)
    print('-' * 50)