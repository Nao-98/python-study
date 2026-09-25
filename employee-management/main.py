# 表舞台のAPI受付窓口
from fastapi import FastAPI, HTTPException, Security, status, Depends
from fastapi.security import APIKeyHeader
from models import EmployeeCreate, EmployeeUpdate
from database import get_all_employees, add_employee, update_employee_role, remove_employee

# アプリの立ち上げ
app = FastAPI()

# 許可する合言葉(APIキー)
VALID_API_KEY = "my-super-secret-key-2026"

# クライアントが「X-API-Key」という名前で鍵を送ってくることを指定
api_key_header = APIKeyHeader(name="X-API-Key")

# 関所となる検証関数
def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != VALID_API_KEY:
        # キーが間違っている場合は 401(Unauthorized) で返す
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="無効なAPIキーです。アクセス権限がありません。"
        )
    return api_key

# 「社員一覧」を実際のDBから取得して返すAPI
@app.get("/employees")
def get_employees(api_key: str = Depends(verify_api_key)):
    # 確認用
    print("🚀🚀🚀最新のmain.pyが動いています🚀🚀🚀")
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