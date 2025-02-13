from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
# from wiki_embeddings import WikiContent


class Chatgpt():
    # クラス変数としてvectorstoreを保持
    _vectorstore = None

    @classmethod
    def set_vectorstore(cls, vectorstore):
        # vectorstoreを設定するクラスメソッド
        cls._vectorstore = vectorstore

    def __init__(self, message):
        self.message = message
        if self._vectorstore is None:
            raise ValueError("vectorstoreが初期化されていません")

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