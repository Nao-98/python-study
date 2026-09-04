# 継承について
# PythonはJavaのように厳格なルールはない
# 1ファイル＝1クラス の縛りがない

# 親クラス
class Cat:
    def __init__(self, name: str):
        self.name = name

    def speak(self) -> str:
        return f"{self.name}が鳴きました：にゃー"

# 子クラス：カッコの中に親クラスを書いて継承
class Siberian(Cat):
    def __init__(self, name: str, fluffiness: str):
        # 親のコンストラクタを呼び出す(Javaの super(name) に相当)
        super().__init__(name)
        # 子クラス独自のフィールドを追加
        self.fluffiness = fluffiness

    # オーバーライド(親と同じ名前のメソッドを定義するだけで上書き)
    def speak(self) -> str:
        # super().speak() で親の処理を再利用することも可能
        original = super().speak()
        return f"{original}ではなくクルル！({self.fluffiness}のしっぽを揺らしている)"

# 実行と確認
pon = Siberian("ぽん", "超もふもふ")
print(pon.speak())