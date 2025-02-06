# 組織構造管理システム

組織構造をビジュアルに表示し、社員の所属情報を管理するシステムです。

## 機能

- 組織構造のツリー形式表示
- 社員一覧の表示
- 社員の異動履歴の表示
- 時点指定での組織構造表示(過去/未来の組織構造を確認可能)
- 主務/兼務の管理

## 技術スタック

- Backend: FastAPI (Python)
- Database: MySQL
- ORM: SQLAlchemy
- Migration: Alembic

## システム要件

- Python 3.8以上
- MySQL 8.0以上

## セットアップ

1. リポジトリのクローン
```bash
git clone https://github.com/hikiroku/silver-broccoli.git
cd silver-broccoli
```

2. 環境変数の設定
```bash
cp backend/.env.example backend/.env
```

`.env`ファイルを編集してデータベース接続情報を設定:
```
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=rootroot
MYSQL_DB=organization_db
MYSQL_PORT=3306
```

3. データベースの作成とマイグレーション
```bash
cd backend
python scripts/create_database.py
alembic upgrade head
```

4. サンプルデータの投入
```bash
python scripts/create_sample_data.py
```

5. APIサーバーの起動
```bash
uvicorn app.main:app --reload
```

## API仕様

### エンドポイント

#### 組織関連
- GET /api/v1/departments
  - 組織一覧を取得
  - クエリパラメータ:
    - target_date: 指定日時点での組織一覧を取得(オプション)

- GET /api/v1/departments/tree
  - 組織構造をツリー形式で取得
  - クエリパラメータ:
    - target_date: 指定日時点での組織構造を取得(オプション)

#### 社員関連
- GET /api/v1/employees
  - 社員一覧を取得

- GET /api/v1/employees/{id}/history
  - 指定した社員の異動履歴を取得

### レスポンス例

#### 組織ツリー
```json
[
  {
    "id": 1,
    "department_code": "HQ",
    "name": "本社",
    "parent_id": null,
    "valid_from": "2024-04-01T00:00:00",
    "valid_until": null,
    "main_members": [
      {
        "id": 1,
        "employee_code": "E001",
        "name": "山田太郎",
        "email": "yamada@example.com"
      }
    ],
    "concurrent_members": []
  }
]
```

## データベース設計

### テーブル構成

#### departments(組織)
- id: 人工キー
- department_code: 組織コード
- name: 組織名
- parent_id: 親組織ID
- valid_from: 有効期間(開始)
- valid_until: 有効期間(終了)

#### employees(社員)
- id: 人工キー
- employee_code: 社員番号
- name: 氏名
- email: メールアドレス

#### assignments(所属)
- id: 人工キー
- employee_id: 社員ID
- department_id: 組織ID
- is_main: 主務フラグ
- valid_from: 有効期間(開始)
- valid_until: 有効期間(終了)

## 開発者向け情報

### APIドキュメント

APIドキュメントは http://localhost:8000/docs で確認できます。
Swagger UIを使用して、各エンドポイントのリクエスト/レスポンスの詳細を確認できます。
