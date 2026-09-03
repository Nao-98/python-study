# 辞書（Dictionary）の作成と反復処理
# TypeScriptのオブジェクトや、PHPの連想配列に相当します。
frameworks = {"PHP": "Laravel", "TypeScript": "Next.js", "Java": "Spring"}

# 【Pythonic】items() を使うと、キーと値を同時にスッキリ取り出せる
for lang, fw in frameworks.items():
    print(f"{lang}の代表的なフレームワークは{fw}です。")