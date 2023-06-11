import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import pyrebase
import hashlib
import json
import getpass

#Configure and Connext to Firebase

firebaseConfig = {'apiKey': "AIzaSyCm2TtbR9FJ-skypYmkTni9W39D-aM7f6I",
  		  'authDomain': "info-7110d.firebaseapp.com",
  		  'databaseURL': "https://info-7110d-default-rtdb.firebaseio.com/",
  		  'projectId': "info-7110d",
  		  'storageBucket': "info-7110d.appspot.com",
   		  'messagingSenderId': "245144296743",
   		  'appId': "1:245144296743:web:b7410edad92e54eb1ddd02",
  		  'measurementId': "G-DW920V64MP"}

firebase=pyrebase.initialize_app(firebaseConfig)
auth=firebase.auth()
dab = firebase.database()

#Login function

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

def login():
    print("Log in...")
    email=input("Enter email: ")
    password=input("Enter password: ")
    try:
        login = auth.sign_in_with_email_and_password(email, password)
        user_id = login['localId']
        print("Successfully logged in!")
            # print(auth.get_account_info(login['idToken']))
            # email = auth.get_account_info(login['idToken'])['users'][0]['email']
            # print(email)
        # Check if user is admin
        admin = dab.child("admin").get()
        admin_id = admin.val().get("id")
        if user_id == admin_id:
            # User is admin, return data
            data = dab.child("admin_data").get().val()
            print("Welcome admin!")
            print(data)
        else:
            # User is not admin, do something else
            print("Welcome user!")
            user_data = authenticate_user(email, password)
            if user_data:
                with open('user.json', 'w', encoding='utf-8') as f:
                    json.dump(user_data, f, ensure_ascii=False, indent=4)
                print("Success")
            else:
                print("Sai thông tin đăng nhập!")
    except:
        print("Invalid email or password")
    return

#Signup Function

def signup():
    print("Sign up...")
    email = input("Enter email: ")
    password=input("Enter password: ")
    try:
        user = auth.create_user_with_email_and_password(email, password)
        ask=input("Do you want to login?[y/n]")
        if ask=='y':
            login()
    except: 
        print("Email already exists")
    return

#Main

ans=input("Are you a new user?[y/n]")

if ans == 'n':
    login()
elif ans == 'y':
    signup()

