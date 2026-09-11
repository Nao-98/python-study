# DB練習場
# サーバー起動(FastAPIの使用)を待つ間、裏側の「データベース操作（SQLite）」だけをオフライン環境で練習・構築しているファイル。
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

# テーブル作成
cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    emp_id INTEGER PRIMARY KEY,
    name TEXT,
    role TEXT,
    email TEXT
)
""")
conn.commit()

# =========================================================
# ▼ 対話型（CLI）アプリのメインループ
# =========================================================
while True:
    print("\n" + "="*30)
    print("【社員管理システム】")
    print("1: 社員一覧を見る")
    print("2: 社員を検索する")
    print("3: 新規社員を登録する (Create)")
    print("4: 社員の役職を更新する (Update)")
    print("5: 社員情報を削除する (Delete)")
    print("9: 終了")
    print("="*30)
    
    # ユーザーからの入力を受け取る
    # .strip() で見えないスペースを自動削除する
    choice = input("メニュー番号を入力してください: ").strip()

    # 実際にPythonが受け取った文字を画面に出して確認する
    # print(f"→【デバッグ】受け取った文字: [{choice}]")

    # in を使って、半角でも全角でも反応するようにする
    if choice in ["9", "９"]:
        print("システムを終了します。")
        break

    elif choice in ["1", "１"]:
        cursor.execute("SELECT * FROM employees")
        results = cursor.fetchall()
        print("\n▼ 登録されている社員一覧")
        for row in results:
            emp = Employee(row[0], row[1], row[2], row[3])
            print(f"[{emp.emp_id}] {emp.name} ({emp.role}) - {emp.email}")

        # 人間が読むためのストッパー
        input("\nEnterキーを押すとメニューに戻ります...")

    elif choice in ["2", "２"]:
        search_keyword = input("\n検索したい名前を入力してください: ")
        # SQLインジェクション対策として、プリペアードステートメントを使用
        # SQL文に値を直接埋め込まず、プレースホルダー(例:?)を使用して値をあとから設定する手法
        # この手法により、ユーザー入力がSQL文として解釈されることを防ぐ
        cursor.execute("SELECT * FROM employees WHERE name LIKE ?", (f"%{search_keyword}%",))
        results = cursor.fetchall()
        if results:
            for row in results:
                emp = Employee(row[0], row[1], row[2], row[3])
                print(f"[{emp.emp_id}] {emp.name} ({emp.role}) - {emp.email}")
        else:
            print("該当する社員は見つかりませんでした。")

    elif choice in ["3", "３"]:
        print("\n▼ 新規社員の登録")
        new_name = input("名前を入力してください: ")
        new_role = input("役職を入力してください: ")
        new_email = input("メールアドレスを入力してください: ")

        # SQLiteでは、emp_idを指定しないと自動で「連番」を振ってくれる
        # 指定するカラムを name, role, email の3つだけに絞るため、以下のように書く
        # INSERT INTO テーブル名 (カラム1, カラム2, カラム3) VALUES (?, ?, ?)
        cursor.execute("INSERT INTO employees(name, role, email) VALUES (?, ?, ?)", (new_name, new_role, new_email))

        # 登録内容を確定してDBに保存する
        conn.commit()
        print(f"{new_name} さんの情報を登録しました！")

        input("\nEnterキーを押すとメニューに戻ります...")

    elif choice in ["4", "４"]:
        print("\n▼ 社員情報の更新")
    
        # 誰を更新するかIDで指定する
        target_id = input("更新したい社員のID番号を入力してください: ")

        # データベースに該当のIDが存在するか確認する
        # 値を流し込むための「空席」である ?（プレースホルダー）と =
        cursor.execute("SELECT * FROM employees WHERE emp_id = ?", (target_id,))

        # 検索結果から1件だけデータを取り出す
        employee_data = cursor.fetchone()

        if employee_data is None:
            print(f"エラー: ID '{target_id}' の社員は存在しません。")
            input("\nEnterキーを押すとメニューに戻ります...")
            continue  # これより下の処理をキャンセルし、ループの最初(メニュー)に戻る

        new_role = input("新しい役職を入力してください: ")

        # 値を流し込むための「空席」である ?（プレースホルダー）と =
        cursor.execute(("UPDATE employees SET role = ? WHERE emp_id = ?"), (new_role, target_id))

        # 更新内容を確定してDBに保存する
        conn.commit()
        print(f"ID:{target_id} の役職を「{new_role}」に更新しました！")
        
        input("\nEnterキーを押すとメニューに戻ります...")

    elif choice in ["5", "５"]:
        print("\n▼ 社員情報の削除")

        target_id = input("削除したい社員のID番号を入力してください: ")

        cursor.execute("SELECT * FROM employees WHERE emp_id = ?", (target_id,))
        employee_data = cursor.fetchone()

        if employee_data is None:
            print(f"エラー: ID '{target_id}' の社員は存在しません。")
            input("\nEnterキーを押すとメニューに戻ります...")
            continue  # これより下の処理をキャンセルし、ループの最初(メニュー)に戻る

        # 値を流し込むための「空席」である ?（プレースホルダー）と =
        cursor.execute("DELETE FROM employees WHERE emp_id = ?", (target_id,))

        # 削除内容を確定してDBに反映する
        conn.commit()
        print(f"ID:{target_id} の社員情報を削除しました！")

        input("\nEnterキーを押すとメニューに戻ります...")

    else:
        print("正しい番号を入力してください。")

# ループを抜けたら接続を閉じる
conn.close()