import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import asyncio
import hashlib
import getpass

def id_index():
    i = 1
    while True:
        ref = db.reference(f'staff/{i}')
        snapshot = ref.get()
        if snapshot is None:
            return i
        i += 1

def authenticate_user(username, password):
    # Khởi tạo Firebase Admin SDK với thông tin xác thực từ tệp JSON đã tải xuống
    cred = credentials.Certificate('info-7110d-firebase-adminsdk-v1or8-9216d6e154.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://info-7110d-default-rtdb.firebaseio.com/'
    })
    user_count = id_index()
    for i in range(1, user_count):
        ref = db.reference('staff/' + str(i))
        data = ref.get()
        if username == data['UserName']:
            # Kiểm tra mật khẩu người dùng và trả về dữ liệu nếu xác thực thành công
            if data['PASS'] == hashlib.sha256(password.encode()).hexdigest():
                return data
    # Nếu không xác thực được, trả về None
    return None

def main():
    # Sử dụng hàm để xác thực người dùng
    username = input("Nhập username: ")
    password = getpass.getpass("Nhập password: ")
    user_data = authenticate_user(username, password)  

    # Kiểm tra kết quả và in ra dữ liệu nếu xác thực thành công
    if user_data:
        print("Đăng nhập thành công")
    else:
        print("Sai thông tin đăng nhập!")

if __name__=="__main__":
    main()