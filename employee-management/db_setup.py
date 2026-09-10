# DB練習場
# サーバー起動を待つ間、裏側の「データベース操作（SQLite）」だけをオフライン環境で練習・構築しているファイル。
import sqlite3
from dataclasses import dataclass

@dataclass
class Employee:
    emp_id: int
    name: str
    role: str
    email: str

# DB接続
conn = sqlite3.connect("company.db")
cursor = conn.cursor()

# =========================================================
# ▼ 昨日書いた「テーブル作成とデータ登録」のコードを合体！
# （すでに存在する場合はスキップされるため、何度実行しても安全です）
cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    emp_id INTEGER PRIMARY KEY,
    name TEXT,
    role TEXT,
    email TEXT
)
""")

cursor.execute("INSERT OR IGNORE INTO employees VALUES (1, 'テスト太郎', 'エンジニア', 'test1@example.com')")
cursor.execute("INSERT OR IGNORE INTO employees VALUES (2, 'てすと次郎', 'エンジニア', 'test2@example.com')")
conn.commit()
# =========================================================

# 課題1: データ取得（SELECT）
cursor.execute("SELECT * FROM employees")
results = cursor.fetchall()

print("▼ 登録されている社員一覧")

# 課題2: オブジェクトへのマッピング
for row in results:
    emp = Employee(row[0], row[1], row[2], row[3])
    print(f"[{emp.emp_id}] {emp.name} ({emp.role}) - {emp.email}")

# =========================================================
# ▼ ここから追加：社員名での検索機能
# =========================================================
print("\n▼ 「太郎」を含む社員の検索結果")

# 検索したいキーワード
search_keyword = "太郎"

# 課題6: 条件を指定して検索(フィルタリング)するSQLを書いてみましょう。
# ヒント: 「WHERE カラム名 LIKE ?」を使います。名前カラムは name です。
cursor.execute("SELECT * FROM employees WHERE name LIKE ?", (f"%{search_keyword}%",))

search_results = cursor.fetchall()

if search_results:
    for row in search_results:
        # 課題7: 先ほどの一覧表示と全く同じように、生のデータ(row)をEmployeeオブジェクトにマッピングしてください。
        emp = Employee(row[0], row[1], row[2], row[3])
        
        print(f"[{emp.emp_id}] {emp.name} ({emp.role}) - {emp.email}")
else:
    print("該当する社員は見つかりませんでした。")

# 接続を閉じる
conn.close()