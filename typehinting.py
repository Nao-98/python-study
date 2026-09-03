# Pythonはもともと、変数にどんなデータでも入れられる
# 「動的型付け言語（PHPやJavaScriptと同じ）」だが、
# 最近の開発現場では「型ヒント（Type Hinting）」をつけて
# 安全かつ読みやすく実装するのがスタンダードになっている

# 1. 従来のPython（動的型付け：引数や戻り値の型がわからない）
def calculate_total(price, tax_rate=0.1):
    return int(price * (1 + tax_rate))

# ---------------------------------------------------

# 2. モダンなPython（型ヒントあり：TypeScriptやKotlinのような書き方）
def calculate_total_modern(price: int, tax_rate: float = 0.1) -> int:
    """税込み価格を計算する関数"""
    return int(price * (1 + tax_rate))

# リストや辞書を型に指定することも可能（Python 3.9以降）
def get_adult_names(users: list[dict[str, int]]) -> list[str]:
    """辞書のリストから20歳以上の名前だけを抽出する"""
    # 先ほど学んだ内包表記(List Comprehension)がここでも活きる！
    return [user["name"] for user in users if user["age"] >= 20]