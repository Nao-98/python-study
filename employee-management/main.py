# 表舞台のAPI受付窓口
from typing import Optional  # 条件が「空」でもOKにするため
from fastapi import FastAPI, HTTPException, Security, status, Depends, Request, Query
from fastapi.security import APIKeyHeader
import time  # 処理時間を計算するため
from datetime import datetime  # 現在時刻を取得するため
from models import EmployeeCreate, EmployeeUpdate
from database import get_all_employees, add_employee, update_employee_role, remove_employee

# アプリの立ち上げ
app = FastAPI(
    title="社員管理システム API",
    description="フロントエンド連携用の社員管理API仕様書です。APIキー認証が必要です。",
    version="1.0.0"
)

# アクセスログを記録するミドルウェア
@app.middleware("http")
async def log_requests(request: Request, call_next):
    # リクエストが来た瞬間の時間を記録(ストップウォッチ開始)
    start_time = time.time()

    # 実際のAPI処理へリクエストを受け渡す(裏側でDB処理などが走る)
    response = await call_next(request)

    # 処理が終わって返ってきたら、かかった時間を計算(ストップウォッチ停止)
    process_time = (time.time() - start_time) * 1000  # ミリ秒(ms)に変換

    # ログに記録したくないURLのリスト
    excluded_paths = ["/docs", "/openapi.json"]

    # アクセスされたURLが除外リストに「含まれていない(not in)」場合だけログを記録
    if request.url.path not in excluded_paths:
        # ログに記録するメッセージを作成
        log_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{log_time}] {request.method} {request.url.path} | Status: {response.status_code} | Time: {process_time: 2f}ms\n"

        # api.log というファイルに追記モード("a")で書き込む
        with open("api.log", "a", encoding="utf-8") as f:
            f.write(log_msg)

    return response

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
# 検索機能付きのGETメソッド
@app.get(
        "/employees",
        tags=["社員管理"],
        summary="社員一覧の取得（検索対応）",
        description="登録されている社員の一覧を取得します。役職や名前での絞り込みが可能です。"
)
def get_employees(
    role: Optional[str] = Query(None, description="役職で完全一致検索（例：エンジニア）"),
    name: Optional[str] = Query(None, description="名前で部分一致（例：荒）"),
    api_key: str = Depends(verify_api_key)
):
    # 確認用
    print("🚀🚀🚀最新のmain.pyが動いています🚀🚀🚀")

    # 裏方のdatabase.pyからデータを取ってくる関数を呼び出す
    all_emps = get_all_employees()

    # 検索条件が指定されていれば、リストを絞り込む
    result = all_emps

    if role:
        # 役職が一致する人だけを残す
        result = [emp for emp in result if emp["role"] == role]
        
    if name:
        # 名前に検索文字が含まれる人だけを残す（部分一致）
        result = [emp for emp in result if name in emp["name"]]
        
    return result

# エンドポイントにタグと説明
@app.post(
        "/employees",
        tags=["社員管理"],
        summary="新規社員の登録",
        description="新しい社員情報をデータベースに登録します。※メールアドレスは重複できません。",
        responses={
            200: {
                "description": "登録成功時のレスポンス"
            },
            400: {
                "description": "入力エラー（メールアドレスの重複など）",
                "content": {
                    "application/json": {
                        "example": {"detail": "このメールアドレスは既に登録されています"}
                    }
                }
            },
            401: {
                "description": "認証エラー（APIキーが無効または未指定）",
                "content": {
                    "application/json": {
                        "example": {"detail": "無効なAPIキーです。アクセス権限がありません。"}
                    }
                }
            }
        }
)
def create_employee(emp: EmployeeCreate, api_key: str = Depends(verify_api_key)):  # emp を受け取る
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