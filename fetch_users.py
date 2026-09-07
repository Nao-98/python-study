import requests

# 取得したデータを格納するためのクラスを定義
class User:
    def __init__(self, name: str, company_name: str):
        self.name = name
        self.company_name = company_name

    def introduce(self) -> str:
        return f"{self.name}(所属：{self.company_name})"

# 外部APIからのデータの取得
url = "https://jsonplaceholder.typicode.com/users"

# サーバーに「これは一般的なブラウザからのアクセスです」と伝えるためのヘッダー設定
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# headersを追加してGETリクエストを送信
response = requests.get(url, headers=headers)
# 生のJSONデータ(辞書のリスト)
raw_users = response.json()

# リスト内包表記で、辞書をUserクラスのインスタンスに変換
# raw_usersからuser(辞書)を1つずつ取り出し、Userクラスに当てはめていく
user_objects = [User(user["name"], user["company"]["name"]) for user in raw_users]

# さらにリスト内包表記で、特定の条件(例：会社名に"Group"が含まれる人)だけを抽出
group_members = [u for u in user_objects if "Group" in u.company_name]

# 出力の結果
print("▼ Group系の会社に所属しているユーザー一覧")
for member in group_members:
    print(member.introduce())