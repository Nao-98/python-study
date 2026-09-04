# カプセル化について
class Cat:
    def __init__(self, name: str, weight: float):
        self.name = name
        # アンダースコア2つをつけると「疑似的なprivate」になる(名前修飾)
        self.__weight = weight

    # 【ゲッター】@property をつけると、メソッドではなく変数のようにアクセスできる
    @property
    def weight(self) -> float:
        return self.__weight

    # 【セッター】@変数名.setter をつけることで、代入時のバリデーションが可能に
    @weight.setter
    def weight(self, value: float):
        if value <= 0:
            print(f"エラー: {self.name}の体重は0より大きくしてください！")
            return
        self.__weight = value

# インスタンス化
tama = Cat("たま", 3.8)

# ゲッターの呼び出し( ()が不要で、変数に直接アクセスしているように見える！)
print(f"たまの体重は {tama.weight} kg")

# セッターの呼び出し(代入演算子 = を使うと自動的にセッターが走る！)
tama.weight = -2.0
tama.weight = 4.1