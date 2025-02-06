import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

def create_database():
    try:
        # rootユーザーでMySQLに接続
        connection = pymysql.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", "root"),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        with connection.cursor() as cursor:
            # データベースを作成(既存の場合は一旦削除)
            db_name = os.getenv("MYSQL_DB", "organization_db")
            cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
            cursor.execute(f"CREATE DATABASE {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print("データベースが正常に作成されました。")

    except Exception as e:
        print("エラーが発生しました:", str(e))
        print("詳細なエラー情報:")
        import traceback
        print(traceback.format_exc())

    finally:
        connection.close()

if __name__ == "__main__":
    create_database()
