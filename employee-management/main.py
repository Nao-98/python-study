from fastapi import FastAPI
from pydantic import BaseModel

# 1. アプリの立ち上げ
app = FastAPI()

# 2. データモデルの定義（先ほどのコード）
class Employee(BaseModel):
    emp_id: int
    name: str
    role: str
    email: str

# 3. モック（仮）データ
MOCK_EMPLOYEES = [
    Employee(emp_id=1, name="テスト太郎", role="エンジニア", email="test1@example.com"),
    Employee(emp_id=2, name="てすと次郎", role="エンジニア", email="test2@example.com"),
    Employee(emp_id=3, name="試験花子", role="人事", email="test3@example.com"),
    Employee(emp_id=4, name="てすと大輔", role="エンジニア", email="test4@example.com"),
    Employee(emp_id=5, name="試験よし子", role="エンジニア", email="test5@example.com"),
]

# 4. 「社員一覧」を返すAPI（エンドポイント）
@app.get("/employees")
def get_employees():
    return MOCK_EMPLOYEES