from models import EmployeeCreate

# テスト用の関数は必ず「test_」から始めます
def test_employee_create_success():
    # 1. テスト用のダミーデータを作成（準備）
    emp = EmployeeCreate(
        name="テスト太郎",
        role="エンジニア",
        email="test@example.com"
    )
    
    # 2. assert（アサート）＝「〜〜であるはずだ！」とプログラムに宣言して検証する
    assert emp.name == "テスト太郎"
    assert emp.role == "エンジニア"
    assert emp.email == "test@example.com"

    print("出力")