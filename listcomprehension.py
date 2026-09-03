# リスト内包表記 (List Comprehension)
# JavaのStream APIや、TypeScriptの filter() + map() に相当する処理を1行で書く技術です。
numbers = [1, 2, 3, 4, 5, 6]

# 従来（Javaなど）の書き方（for文とif文のネスト）
# result = []
# for n in numbers:
#     if n % 2 == 0:
#         result.append(n * 2)

# 【Pythonic】リスト内包表記での書き方: [式 for 変数 in リスト if 条件]
even_doubled = [n * 2 for n in numbers if n % 2 == 0]

print(f"偶数を2倍にしたリスト: {even_doubled}")