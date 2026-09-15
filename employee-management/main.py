import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel

# 1. アプリの立ち上げ
app = FastAPI()

# DBファイル名を指定（ご自身の環境に合わせて変更してください）
DB_FILE = "company_v2.db"

# 2. データモデルの定義（そのまま活かします）
class Employee(BaseModel):
    emp_id: int
    name: str
    role: str
    email: str

class EmployeeCreate(BaseModel):
    name: str
    role: str
    email: str

class EmployeeUpdate(BaseModel):
    role: str

# 3. 「社員一覧」を実際のDBから取得して返すAPI
@app.get("/employees")
def get_employees():
    # DBに接続
    conn = sqlite3.connect(DB_FILE)
    
    # ★魔法の設定：データを「辞書型（列名と値のセット）」で扱いやすくする
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # 実際のテーブルからデータを取得（※テーブル名や列名が違う場合は修正してください）
    cursor.execute("SELECT emp_id, name, role, email FROM employees")
    rows = cursor.fetchall()
    
    # 接続を閉じる
    conn.close()
    
    # 取得したデータを辞書のリストに変換してFastAPIに返す（自動でJSONになります）
    return [dict(row) for row in rows]

@app.post("/employees")
def create_employee(emp: EmployeeCreate):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        # 昨日のCLIアプリと同じ「プレースホルダー(?)」を使った安全な登録処理
        cursor.execute(
            "INSERT INTO employees(name, role, email) VALUES (?, ?, ?)", 
            (emp.name, emp.role, emp.email)
        )
        conn.commit()
        message = f"{emp.name}さんの情報を登録しました！"
    except sqlite3.IntegrityError:
        # メールアドレス重複エラーのハンドリング
        message = f"エラー: '{emp.email}' は既に登録されています。"
    finally:
        conn.close()
        
    return {"message": message}

# 社員情報の更新 (PUT)
@app.put("/employees/{emp_id}")
def update_employee(emp_id: int, emp_update: EmployeeUpdate):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # 役職を更新する
    cursor.execute("UPDATE employees SET role = ? WHERE emp_id = ?", (emp_update.role, emp_id))
    conn.commit()

    # 更新された「行数」を見て、IDが存在したかチェックする
    if cursor.rowcount == 0:
        conn.close()
        return {"message": f"エラー: ID '{emp_id}' の社員は見つかりませんでした。"}

    conn.close()
    return {"message": f"エラー: ID '{emp_id}' の役職を「{emp_update.role}」に更新しました！"}

# 社員情報の削除 (DELETE)
@app.delete("/employees/{emp_id}")
def delete_employee(emp_id: int):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # 該当IDの社員を削除する
    cursor.execute("DELETE FROM employees WHERE emp_id = ?", (emp_id,))
    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return {"message": f"エラー: ID '{emp_id}' の社員は見つかりませんでした。"}

    conn.close()
    return {"message": f"ID:{emp_id} の社員情報を削除しました！"}