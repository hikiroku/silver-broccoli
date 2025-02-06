# データベース設計

## テーブル構造

### employees(社員マスタ)
| カラム名 | 型 | 説明 | 
|---------|------|------|
| id | BIGINT | 主キー(人工キー) |
| employee_code | VARCHAR(10) | 社員番号(UK) |
| name | VARCHAR(100) | 氏名 |
| email | VARCHAR(256) | メールアドレス |
| created_at | DATETIME | 作成日時 |
| updated_at | DATETIME | 更新日時 |

### departments(組織マスタ)
| カラム名 | 型 | 説明 |
|---------|------|------|
| id | BIGINT | 主キー(人工キー) |
| department_code | VARCHAR(10) | 組織コード(UK) |
| name | VARCHAR(100) | 組織名 |
| parent_id | BIGINT | 親組織ID(FK: departments.id) |
| valid_from | DATE | 有効期間開始日 |
| valid_until | DATE | 有効期間終了日 |
| created_at | DATETIME | 作成日時 |
| updated_at | DATETIME | 更新日時 |

### main_assignments(主務所属)
| カラム名 | 型 | 説明 |
|---------|------|------|
| id | BIGINT | 主キー(人工キー) |
| employee_id | BIGINT | 社員ID(FK: employees.id) |
| department_id | BIGINT | 組織ID(FK: departments.id) |
| valid_from | DATE | 有効期間開始日 |
| valid_until | DATE | 有効期間終了日 |
| created_at | DATETIME | 作成日時 |
| updated_at | DATETIME | 更新日時 |

### concurrent_assignments(兼務所属)
| カラム名 | 型 | 説明 |
|---------|------|------|
| id | BIGINT | 主キー(人工キー) |
| employee_id | BIGINT | 社員ID(FK: employees.id) |
| department_id | BIGINT | 組織ID(FK: departments.id) |
| valid_from | DATE | 有効期間開始日 |
| valid_until | DATE | 有効期間終了日 |
| created_at | DATETIME | 作成日時 |
| updated_at | DATETIME | 更新日時 |

## ビュー

### v_current_organization
現在時点の組織構造を表示するビュー

### v_employee_assignments
社員の現在の所属(主務・兼務)を表示するビュー

### v_assignment_history
社員の異動履歴を表示するビュー

## インデックス

### employees
- PRIMARY KEY (id)
- UNIQUE KEY uk_employee_code (employee_code)

### departments
- PRIMARY KEY (id)
- UNIQUE KEY uk_department_code (department_code)
- INDEX idx_parent_id (parent_id)
- INDEX idx_valid_period (valid_from, valid_until)

### main_assignments
- PRIMARY KEY (id)
- INDEX idx_employee_id (employee_id)
- INDEX idx_department_id (department_id)
- INDEX idx_valid_period (valid_from, valid_until)

### concurrent_assignments
- PRIMARY KEY (id)
- INDEX idx_employee_id (employee_id)
- INDEX idx_department_id (department_id)
- INDEX idx_valid_period (valid_from, valid_until)
