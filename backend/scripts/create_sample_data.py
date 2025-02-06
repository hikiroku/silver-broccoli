import os
import sys
from datetime import datetime, date
import pymysql
from dotenv import load_dotenv

load_dotenv()

def create_sample_data():
    try:
        # データベースに接続
        connection = pymysql.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", "rootroot"),
            database=os.getenv("MYSQL_DB", "organization_db"),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        with connection.cursor() as cursor:
            now = datetime.now()
            print("組織データを生成中...")

            # 本部データを作成
            print("本部データを登録中...")
            departments = [
                ("HQ", "本社", None),
                ("SALES", "営業本部", 1),
                ("DEV", "開発本部", 1),
                ("SALES_1", "第一営業部", 2),
                ("SALES_2", "第二営業部", 2),
                ("DEV_1", "第一開発部", 3),
                ("DEV_2", "第二開発部", 3),
            ]
            
            for code, name, parent_id in departments:
                cursor.execute("""
                    INSERT INTO departments 
                    (department_code, name, parent_id, valid_from, valid_until, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (code, name, parent_id, date(2024, 4, 1), None, now, now))
            
            # 社員データを作成
            print("社員データを登録中...")
            employees = [
                ("E001", "山田太郎", "yamada@example.com"),
                ("E002", "鈴木花子", "suzuki@example.com"),
                ("E003", "佐藤次郎", "sato@example.com"),
                ("E004", "田中三郎", "tanaka@example.com"),
                ("E005", "高橋四郎", "takahashi@example.com"),
            ]
            
            for code, name, email in employees:
                cursor.execute("""
                    INSERT INTO employees 
                    (employee_code, name, email, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s)
                """, (code, name, email, now, now))
            
            # 所属データを作成
            print("所属データを登録中...")
            assignments = [
                (1, 1, True),  # 山田太郎 - 本社
                (2, 2, True),  # 鈴木花子 - 営業本部
                (2, 3, False), # 鈴木花子 - 開発本部(兼務)
                (3, 4, True),  # 佐藤次郎 - 第一営業部
                (4, 6, True),  # 田中三郎 - 第一開発部
                (5, 7, True),  # 高橋四郎 - 第二開発部
            ]
            
            for employee_id, department_id, is_main in assignments:
                cursor.execute("""
                    INSERT INTO assignments 
                    (employee_id, department_id, is_main, valid_from, valid_until, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (employee_id, department_id, is_main, date(2024, 4, 1), None, now, now))
            
            connection.commit()
            print("サンプルデータの作成が完了しました")

    except Exception as e:
        print("エラーが発生しました:", str(e))
        print("詳細なエラー情報:")
        import traceback
        print(traceback.format_exc())
        connection.rollback()

    finally:
        connection.close()
        print("データベース接続を閉じました")

if __name__ == "__main__":
    create_sample_data()
