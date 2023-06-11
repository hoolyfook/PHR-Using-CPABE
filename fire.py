import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import hashlib

# Khởi tạo Firebase Admin SDK với thông tin xác thực từ tệp JSON đã tải xuống
cred = credentials.Certificate('info-7110d-firebase-adminsdk-v1or8-9216d6e154.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://info-7110d-default-rtdb.firebaseio.com/'
})

# Lấy một tham chiếu đến node 'users' trong Realtime Database
ref = db.reference('staff')

# Lấy dữ liệu từ node 'users'
data = ref.get()

# In ra dữ liệu lấy được
print(data)