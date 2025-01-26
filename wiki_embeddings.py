import json
import os
import shutil
import configparser
from datetime import datetime
from pybacklogpy.Wiki import Wiki
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document


class WikiContent():
    @staticmethod
    def should_update_db(force_update=False):
        # 強制更新フラグがTrueの場合は即座に更新
        if force_update:
            return True
        
        today = datetime.now()

        # 毎月1日かチェック
        if today.day == 1:
            return True
            
        # chroma_dbが存在しないケースもTrue
        if not os.path.exists("./chroma_db"):
            return True
            
        return False

    # wikiのIDからテキストを取得
    @staticmethod
    def get_wiki():
        # secretsファイルから設定を読み込む
        config = configparser.ConfigParser()
        config.read('secrets')

        # ProjectIdsを取得し、カンマで分割してリスト化
        project_ids = config['backlog']['ProjectIds'].split(',')

        wiki_id_list = []
        wiki_text_list = []
        wiki_api = Wiki()

        # 各プロジェクトのWikiを取得
        for project_id in project_ids:
            try:
                response = wiki_api.get_wiki_page_list(
                    project_id_or_key=project_id,
                )

                if not response.ok:
                    print(f"Warning: プロジェクト {project_id} のWiki一覧の取得に失敗しました")
                    continue

                # wiki_IDをリストに格納
                wiki_pages = json.loads(response.text)
                for wiki in wiki_pages:
                    wiki_id_list.append({
                        'id': wiki['id'],
                        'project_id': project_id
                    })

            except Exception as e:
                print(f"Error: プロジェクト {project_id} の処理中にエラーが発生: {e}")
                continue

        # 各WikiページのIDから内容を取得
        for wiki_info in wiki_id_list:
            try:
                response = wiki_api.get_wiki_page(
                    wiki_id=wiki_info['id']
                )

                if not response.ok:
                    print(f"Warning: Wiki ID {wiki_info['id']} の内容取得に失敗")
                    continue

                wiki_data = json.loads(response.text)
                wiki_content = wiki_data['content']
                wiki_text = wiki_content.replace('\r\n', '').replace('\n', '')
                
                # プロジェクト情報も含めて保存
                wiki_text_list.append({
                    'text': wiki_text,
                    'project_id': wiki_info['project_id'],
                    'wiki_id': wiki_info['id']
                })

            except Exception as e:
                print(f"Error: Wiki ID {wiki_info['id']} の処理中にエラーが発生: {e}")
                continue

        print(f"合計 {len(wiki_text_list)} 件のWikiを取得しました")
        return wiki_text_list


    @staticmethod
    def get_vectorstore(force_update=False):
        embeddings = HuggingFaceEmbeddings(model_name="pkshatech/GLuCoSE-base-ja-v2")

        # 更新が必要かチェック
        if WikiContent.should_update_db(force_update):
            print(f"ベクトルDBの更新を開始します（{datetime.now().strftime('%Y-%m-%d')}）")

            # Wikiテキストを取得
            wiki_texts = WikiContent.get_wiki()

            # テキストが空でないことを確認
            if not wiki_texts:
                print("警告: Wikiテキストが取得できませんでした")
                if os.path.exists("./chroma_db"):
                    print("既存のベクトルストアを使用します...")
                    return Chroma(
                        persist_directory="./chroma_db",
                        embedding_function=embeddings
                    )
                else:
                    raise ValueError("Wikiテキストが空で、既存のベクトルストアもありません")

            print(f"取得したWikiの数: {len(wiki_texts)}")  # デバッグ用
            
            # 既存のDBが存在する場合は削除
            if os.path.exists("./chroma_db"):
                shutil.rmtree("./chroma_db")
            
            # テキストを分割
            text_splitter = CharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=50
            )

            # Document形式に変換
            documents = [
                Document(page_content=text['text'], metadata={'project_id': text['project_id'], 'wiki_id': text['wiki_id']})
                for text in wiki_texts
            ]

            split_texts = text_splitter.split_documents(documents)

            if not split_texts:
                raise ValueError("テキスト分割後のドキュメントが空です")
            
            vectorstore = Chroma.from_documents(
                documents=split_texts,
                embedding=embeddings,
                persist_directory="./chroma_db"
            )
            print("ベクトルDBの更新が完了しました")
            return vectorstore
        
        # 更新が不要な場合は既存のDBを読み込む
        print("既存のベクトルストアを読み込みます...")
        return Chroma(
            persist_directory="./chroma_db",
            embedding_function=embeddings
        )




if __name__ == "__main__":
    # vectorstore = WikiContent.get_vectorstore()
    # print("ベクトルストアの準備が完了しました")

    texts = WikiContent.get_wiki()
    print(f"取得したWikiテキスト数: {len(texts)}")
    if texts:
        print("最初のテキストのサンプル:", texts[0])
    
    # テキストが取得できた場合のみベクトル化を実行
    if texts:
        vectorstore = WikiContent.get_vectorstore(force_update=True)
        print("ベクトルストアを更新しました")