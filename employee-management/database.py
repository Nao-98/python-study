# 裏方のDB操作・SQL職人
import sqlite3
from models import EmployeeCreate, EmployeeUpdate

# DBファイル名を指定
DB_FILE = "company_v2.db"

def get_all_employees():
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

def add_employee(emp: EmployeeCreate):
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

def update_employee_role(emp_id: int, emp_update: EmployeeUpdate):
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
    return {"message": f"'{emp_id}' の役職を「{emp_update.role}」に更新しました！"}

def remove_employee(emp_id: int):
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