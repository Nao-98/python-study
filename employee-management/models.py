# データの設計図・型定義
from pydantic import BaseModel, Field

# データモデルの定義
class Employee(BaseModel):
    emp_id: int
    name: str
    role: str
    email: str

# 登録時のデータ構造
class EmployeeCreate(BaseModel):
    # Fieldを使って、画面に出す説明(description)と入力例(examples)を追加
    name: str = Field(..., description="社員の氏名", examples=["荒木"])
    role: str = Field(..., description="役職や部署名", examples=["システムエンジニア"])
    email: str = Field(..., description="連絡用メールアドレス", examples=["araki@example.com"])

class EmployeeUpdate(BaseModel):
    role: str