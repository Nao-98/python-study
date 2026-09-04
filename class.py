class Cat:
    # コンストラクタ(初期化メソッド)
    def __init__(self, name: str, breed: str):
        self.name = name  # Javaの this.name に相当
        self.breed = breed

    # メソッド(第一引数に必ず self を明記)
    def introduce(self) -> str:
        return f"私は{self.breed}の{self.name}です！"

# インスタンス化(newキーワードは不要)
tama = Cat("たま", "スコティッシュフォールド")
pon = Cat("ぽん", "サイベリアン")

print(tama.introduce())
print(pon.introduce())