import json
import csv  # CSVの中身を綺麗に読み込むための道具
from pathlib import Path
from datetime import datetime  # エラー発生時刻を記録するため

# 前日作ったDB登録関数と、型の設計図をインポートする
from models import EmployeeCreate
from database import add_employee

# 1. jsonの読み込み
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

# 2. configからフォルダのパスを取り出して、変数 folder_path に入れる
folder_path = config["csv_folder_path"]

# 3. 見つけたCSVファイルを1つずつループして処理する
for csv_file in Path(folder_path).glob("*.csv"):

    print(f"--- {csv_file} を処理します ---")
    
    # 4. 見つけたファイル(csv_file)を開いて中身を読む
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)

        # 読み込んだ中身をさらに1行ずつループして表示する
        for row in reader:
            # rowの中身は ['佐藤花子', 'デザイナー', 'hanako.sato@example.com'] のようなリスト

                # リストの0番目(名前)、1番目(役職)、2番目(メール)を取り出して、型にはめる
                emp_data = EmployeeCreate(
                    name=row[0],
                    role=row[1],
                    email=row[2]
                )

                # 型にはめたデータを、database.pyの関数に丸投げして登録！
                result = add_employee(emp_data)

                # 戻り値のメッセージに「エラー」という文字が含まれているかチェック
                if "エラー" in result["message"]:
                    # エラーが起きた時刻を取得
                    error_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    # ログに書き込むメッセージを作成
                    error_msg = f"[{error_time}] 登録失敗: ファイル={csv_file.name}, データ={row}, 原因={result['message']}]\n"

                    # ターミナルにお知らせ
                    print(f"⚠️ 登録スキップ: {row[0]}さん ({result['message']})")

                    # error.log というファイルに「追記モード("a" = append)」で書き込む
                    with open("error.log", "a", encoding="utf-8") as log_file:
                        log_file.write(error_msg)

                else:
                    # 結果 (「～さんを登録しました！」)を画面に表示する
                    print(result["message"])