import pymysql
from app.core.config import settings

def reset_migrations():
    # データベースサーバーに接続
    connection = pymysql.connect(
        host=settings.MYSQL_HOST,
        user=settings.MYSQL_USER,
        password=settings.MYSQL_PASSWORD,
        database=settings.MYSQL_DB
    )
    
    try:
        with connection.cursor() as cursor:
            # alembic_versionテーブルを削除
            cursor.execute("DROP TABLE IF EXISTS alembic_version")
            connection.commit()
            print("マイグレーション履歴をリセットしました。")
    
    except Exception as e:
        print(f"エラーが発生しました: {e}")
    
    finally:
        connection.close()

if __name__ == "__main__":
    reset_migrations()
