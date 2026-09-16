# 表舞台のAPI受付窓口
from models import EmployeeCreate, EmployeeUpdate
from database import get_all_employees, add_employee, update_employee_role, remove_employee
from fastapi import FastAPI

# アプリの立ち上げ
app = FastAPI()

# 「社員一覧」を実際のDBから取得して返すAPI
@app.get("/employees")
def get_employees():
    # 裏方のdatabase.pyからデータを取ってくる関数を呼び出す
    return get_all_employees()

@app.post("/employees")
def create_employee(emp: EmployeeCreate):  # emp を受け取る
    # 裏方のdatabase.pyからデータを取ってくる関数を呼び出す
    return add_employee(emp)  # 受け取った emp を裏方にそのまま渡す
    

# 社員情報の更新 (PUT)
@app.put("/employees/{emp_id}")
def update_employee(emp_id: int, emp_update: EmployeeUpdate):  # ID, データを受け取る
    # 裏方のdatabase.pyからデータを取ってくる関数を呼び出す
    return update_employee_role(emp_id, emp_update)  # 裏方にそのまま渡す

# 社員情報の削除 (DELETE)
@app.delete("/employees/{emp_id}")
def delete_employee(emp_id: int):  # ID を受け取る
    # 裏方のdatabase.pyからデータを取ってくる関数を呼び出す
    return remove_employee(emp_id)  # 裏方にそのまま渡す