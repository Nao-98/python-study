# CSVファイルを読み書きするための専用の道具箱（モジュール）を持ってくる
import csv
# ファイルを移動したりコピーしたりする、OS操作の道具箱を持ってくる
import shutil
# pathlib という道具箱の中から、ファイルの「場所（パス）」を便利に扱うための Path という特定の道具だけを取り出す
from pathlib import Path

# 準備
# ファイルの場所を自分で決めた変数(箱)に記憶させる
tokyo_file = Path("sales_tokyo_20260916.csv")
osaka_file = Path("sales_osaka_20260916.csv")
master_file = Path("社員マスタ.csv")
output_file = Path("report_20260916_done.csv")

# 結合したデータを入れておく空のリスト(箱)を用意
combined_data = []

# 1. 売上データの読み込みとクレンジング
# with open(...) as f: はファイルを安全に開くための決まり文句
# mode="r" は読み込み専用（Read）の意味。開いたファイルを、ここでは f という一時的な変数名で扱う
with open(tokyo_file, mode="r", encoding="utf-8") as f:
    # csvモジュールの DictReader という道具を使い、ファイル f を「列名（ヘッダー）と値のセット（辞書形式）」で読み込み、reader という箱に入れる
    reader = csv.DictReader(f)
    # reader の中からデータを上から1行ずつ取り出し、row という一時的な箱に入れて、下の処理を繰り返すループ文
    for row in reader:
        # もし row の中の "Status" 列の値が "Error" ではない（!=） ならば、下の処理をする
        if row["Status"] != "Error":
            # 問題なかったその1行（row）を、最初に用意した大きな箱（combined_data）に追加（append）
            combined_data.append(row)

# 途中までは、上記の東京データと同じ処理
with open(osaka_file, mode="r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row["Status"] != "Error":
            # もし row の中の "Amount"（金額）が空っぽ（not）だったら、下の処理をする
            if not row["Amount"]:
                # 空っぽだった "Amount" の部分に、文字の "0" を代入して書き換え
                # これで欠損値の穴埋めが完了し、大きな箱（combined_data）に追加される
                row["Amount"] = "0"
            combined_data.append(row)

# 2. 社員マスタの読み込み（辞書化）
# {} は「空の辞書」を作る。検索用のデータをセットで入れておく箱
master_dict = {}
with open(master_file, mode="r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        # EmployeeIDをキーにして、名前と部署名を保存する（これがVLOOKUPの参照先の役割になる）
        master_dict[row["EmployeeID"]] = {
            "Name": row["Name"],
            "Department": row["Department"]
        }

# 3. データの結合（VLOOKUPの実行）
# さっき綺麗にして合体させた売上データの大きな箱から、1行ずつ取り出して data という箱に入れる
for data in combined_data:
    # その行の社員IDを取り出し、emp_id という箱に入れる
    emp_id = data["EmployeeID"]
    # もしその社員IDが、ステップ5で作った辞書（master_dict）の見出しの中に存在するならば、
    if emp_id in master_dict:
        # 辞書から名前を引き出してきて、売上データ側に新しく "Name" という列を作って代入
        data["Name"] = master_dict[emp_id]["Name"]
        # 辞書から部署名を引き出してきて、売上データ側に新しく "Department" という列を作って代入
        data["Department"] = master_dict[emp_id]["Department"]
    else:
        # 社員IDが辞書に存在しなかった場合の、エラー落ちを防ぐ安全処理
        data["Name"] = "不明"
        data["Department"] = "不明"

# 4. 結果を新しいCSVに書き出す
# 出力する列（ヘッダー）の順番をリストで定義
fieldnames = ["TransactionID", "Date", "EmployeeID", "Name", "Department", "Amount", "Status"]

# 今度は書き込み専用（Write）でファイルを開く
with open(output_file, mode="w", encoding="utf-8", newline="") as f:
    # 辞書データをCSVに書き込むための道具（DictWriter）を準備し、列の順番（fieldnames）を教える
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()            # 1行目にヘッダー(列名)を書き込む
    writer.writerows(combined_data) # writerows(複数形)という指示で、加工したデータを一気に書き込む

# 5. 元ファイルの移動
# "processed" という新しいフォルダの名前を変数にセット
processed_dir = Path("processed")
# mkdir（メイクディレクトリ）でフォルダを作成
# exist_ok=True は「もし既に同名フォルダがあっても、エラーで止めずにそのまま進めてね」という安全処理
processed_dir.mkdir(exist_ok=True)
# shutil の move という道具を使って、元のファイル（tokyo_file）を新しいフォルダの中に移動
shutil.move(tokyo_file, processed_dir / tokyo_file.name)
shutil.move(osaka_file, processed_dir / osaka_file.name)

print("マスタ結合とCSV出力が完了しました！")