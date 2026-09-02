# 1. 品物が2つ入ったリストを作る
shopping_list = ["りんご", "牛乳"]

# 2. ユーザーに入力を促して、変数 new_item に格納する
new_item = input("他に追加したいものはありますか？: ")

# 3. リストに new_item (新しい品物) を追加する
shopping_list.append(new_item)

# 4. for文を使って、リストの中身を順番に表示する
for item in shopping_list:
    print(f"{item}を買います！")