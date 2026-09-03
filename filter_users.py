# APIのレスポンスを想定したユーザーデータ（辞書のリスト）
users_data = [
    {"name": "田中", "age": 27},
    {"name": "佐藤", "age": 18},
    {"name": "鈴木", "age": 32}
]

# 1. 戻り値の型ヒントを設定する（文字列のリスト）
def get_adult_names(users: list[dict]) -> list[str]:
    # 2. リスト内包表記で、20歳以上のユーザーの "name" だけを抽出する
    # 内包表記の基本は [式 for 変数 in リスト if 条件]
    return [user["name"] for user in users if user["age"] >= 20]

# 実行して ['田中', '鈴木'] と表示されれば成功
print(get_adult_names(users_data))