# クラスの定義だけをemployee.pyに切り出しているのも、実務のアーキテクチャ（関心の分離）として大正解

from pydantic import BaseModel

# BaseModelを継承するだけで、__init__が不要になる（裏で自動生成される）
class Employee(BaseModel):
    emp_id: int
    name: str
    role: str
    email: str