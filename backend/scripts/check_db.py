import pymysql

def check_db():
    # データベースに接続
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='rootroot',
        database='organization_db'
    )

    try:
        with connection.cursor() as cursor:
            # テーブルごとのレコード数を確認
            tables = ['employees', 'departments', 'main_assignments', 'concurrent_assignments']
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"{table}: {count}件")

    except Exception as e:
        print(f"エラーが発生しました: {e}")
    
    finally:
        connection.close()

if __name__ == "__main__":
    check_db()
