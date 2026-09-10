from pydantic import BaseModel

# BaseModelを継承するだけで、__init__が不要になる（裏で自動生成される）
class Employee(BaseModel):
    emp_id: int
    name: str
    role: str
    email: str