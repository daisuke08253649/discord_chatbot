from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


class WikiContent():
    @staticmethod
    def get_vectorstore():
        embeddings = HuggingFaceEmbeddings(model_name="pkshatech/GLuCoSE-base-ja-v2")
        # 更新が不要な場合は既存のDBを読み込む
        print("既存のベクトルストアを読み込みます...")
        return Chroma(
            persist_directory="test_chroma_db",
            embedding_function=embeddings
        )