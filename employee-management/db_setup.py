import sqlite3
from dataclasses import dataclass

# 課題1: 先ほど書いた Employee クラスを、モダンな @dataclass で書き換えてみましょう。
# @dataclass をつけると、def __init__(self, ...): の記述が丸ごと不要になります！
@dataclass
class Employee:
    # ここにプロパティ名と型ヒント（int や str）だけを並べてください。
    emp_id: int
    name: str
    role: str
    email: str

# 課題2: データベースファイル（company.db）に接続するコードを書いてみましょう。
# ヒント: sqlite3.connect("ファイル名") を使います。
conn = sqlite3.connect("company.db")
cursor = conn.cursor()

# 課題3: テーブルの作成
# データベースに「社員を保存するための表（テーブル）」を作ります。
# ヒント: SQLを実行するには cursor.execute() を使います。
cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    emp_id INTEGER PRIMARY KEY,
    name TEXT,
    role TEXT,
    email TEXT
)
""")

# 課題4: モックデータ（仮データ）の登録
# 作成したテーブルに、社員データを1件登録してみましょう。
# ヒント: ここでも cursor.execute() を使います。
cursor.execute("INSERT OR IGNORE INTO employees VALUES (1, 'テスト太郎', 'エンジニア', 'test1@example.com')")
cursor.execute("INSERT OR IGNORE INTO employees VALUES (2, 'てすと次郎', 'エンジニア', 'test2@example.com')")
cursor.execute("INSERT OR IGNORE INTO employees VALUES (3, '試験花子', '人事', 'test3@example.com')")

# 課題5: 変更の確定（保存）
# データベースへの変更（追加や更新）をファイルに完全に書き込むには、「コミット」という操作を行う必要があります。
# ヒント: conn に対して commit() メソッドを呼び出します。
conn.commit()

print("テーブルの作成とデータの登録に成功しました！")

# 処理が終わったら接続を閉じる（お約束）
conn.close()