import os
import sys
from dotenv import load_dotenv
import pymysql

load_dotenv()

def check_tables():
    try:
        # データベースに接続
        connection = pymysql.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", "root"),
            database=os.getenv("MYSQL_DB", "organization_db"),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        with connection.cursor() as cursor:
            # テーブル一覧を取得
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            print("データベース内のテーブル一覧:")
            for table in tables:
                table_name = list(table.values())[0]
                print(f"- {table_name}")
                
                # テーブルの構造を取得
                cursor.execute(f"DESCRIBE {table_name}")
                columns = cursor.fetchall()
                print("  カラム:")
                for column in columns:
                    print(f"    - {column['Field']}: {column['Type']}")
                print()

    except Exception as e:
        print("エラーが発生しました:", str(e))
        print("詳細なエラー情報:")
        import traceback
        print(traceback.format_exc())

    finally:
        connection.close()
        print("データベース接続を閉じました")

if __name__ == "__main__":
    check_tables()
