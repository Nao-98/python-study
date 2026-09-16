# データの設計図・型定義
from pydantic import BaseModel

# データモデルの定義（そのまま活かします）
class Employee(BaseModel):
    emp_id: int
    name: str
    role: str
    email: str

class EmployeeCreate(BaseModel):
    name: str
    role: str
    email: str

class EmployeeUpdate(BaseModel):
    role: str