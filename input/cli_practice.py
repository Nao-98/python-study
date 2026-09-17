import argparse
import csv
import logging
import shutil
from pathlib import Path

# --------------------------------------------------
# 1. ログの設定 (logging)
# --------------------------------------------------
# app.log というファイルに INFO (情報) レベル以上のログを書き込む設定
logging.basicConfig(
    filename="app.log",
    encoding="utf-8",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# --------------------------------------------------
# 2. RPAからの引数受け取り設定 (argparse)
# --------------------------------------------------
# 引数を受け取るためのパーサー(解析機)の準備
parser = argparse.ArgumentParser(description="売上データ加工スクリプト")

# RPAから渡される "--input"(入力元ファイル)と "--output"(出力先ファイル)という引数を定義する
parser.add_argument("--input", required=True, help="処理するCSVのパス")
parser.add_argument("--output", required=True, help="出力先のパス")

# 実際に受け取った引数を解析して args という箱に入れる
args = parser.parse_args()

# --------------------------------------------------
# 3. メイン処理
# --------------------------------------------------
def main():
    # ログに「処理開始」と記録する
    logging.info("処理を開始します。")

    # RPAから受け取ったパスを pathlib の Path に変換する
    input_file = Path(args.input)
    output_file = Path(args.output)
    # マスタは固定の場所に置く運用とする
    master_file = Path("社員マスタ.csv")

    # 入力ファイルが存在するかチェックする防衛的処理
    if not input_file.exists():
        # ログにエラーとして記録し、処理を終了する
        logging.error(f"ファイルが見つかりません: {input_file}")
        return
    if not master_file.exists():
        logging.error(f"マスタファイルが見つかりません: {master_file}")
        return

    # 結合したデータを入れておく空のリスト(箱)を用意
    combind_data = []

    # 入力された売上データの読み込みとクレンジング
    try:
        with open(input_file, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["Status"] != "Error":
                    if not row["Amount"]:  # 空欄は 0 に
                        row["Amount"] = "0"
                    combind_data.append(row)
        logging.info(f"{input_file.name} のクレンジングが完了しました。")
    except Exception as e:
        #予期せぬエラーが起きたらログに残して異常終了させる
        logging.error(f"データの読み込み中にエラーが発生しました: {e}")
        return

    # 社員マスタの読み込み (辞書化)
    master_dict = {}
    with open(master_file, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            master_dict[row["EmployeeID"]] = {
                "Name": row["Name"],
                "Department": row["Department"]
            }
    logging.info("社員マスタの読み込みが完了しました。")

    # データの結合 (VLOOKUP)
    for data in combind_data:
        emp_id = data["EmployeeID"]
        if emp_id in master_dict:
            data["Name"] = master_dict[emp_id]["Name"]
            data["Department"] = master_dict[emp_id]["Department"]
        else:
            data["Name"] = "不明"
            data["Department"] = "不明"

    # 結果を新しいCSVに書き出す
    fieldnames = ["TransactionID", "Date", "EmployeeID", "Name", "Department", "Amount", "Status"]
    with open(output_file, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(combind_data)
    logging.info(f"{output_file.name} の作成が完了しました。")

    # 元ファイルの移動
    processed_dir = Path("processed")
    processed_dir.mkdir(exist_ok=True)
    shutil.move(input_file, processed_dir / input_file.name)
    logging.info("ファイルの移動が完了しました。")

    logging.info("処理が正常に完了しました。")

# スクリプトが直接実行されたときだけmain()を動かす決まり文句
if __name__ == "__main__":
    main()
