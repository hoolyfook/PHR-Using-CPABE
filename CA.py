from charm.toolbox.pairinggroup import PairingGroup,ZR, G1, G2, GT
from charm.core.engine.util import *
from charm.schemes.abenc.ac17 import AC17CPABE
from charm.toolbox.msp import MSP
from Include import AC17Serialize as AC17Serialize
from Include import CPABE as cp_abe
from Include import SerializeKey as SerializeKey
from Crypto.Util.number import bytes_to_long,long_to_bytes
import json
import socket
import pickle
import base64

if __name__ == '__main__':
    # Khởi tạo server socket
    host = 'localhost'
    port = 62345
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))

    # Lắng nghe kết nối từ client
    server_socket.listen(1)
    print('Server is listening...')
    conn, addr = server_socket.accept()
    print(f'Connected by {addr}')

    import json

    # Nhận dữ liệu từ client

    json_str = conn.recv(1024)
    print("Received data")
    print(json_str)

    with open('attr.txt', 'r') as file:
        server_data = json.load(file)
    # Chuyển đổi chuỗi JSON thành đối tượng Python
    json_data = json.loads(json_str)

    # So sánh dữ liệu và trả về kết quả
    if json_data['ID'] in server_data and json_data["Faculty"].upper() in server_data:
        abe = cp_abe.CP_ABE()
        key = SerializeKey.serializeKey()
        attr_list = [json_data['ID'].upper(), json_data["Faculty"].upper()]
        print(server_data)
        print(attr_list)
        mk = key.load_file_mk()
        pk = key.load_file_pk()
        sk = abe.PrivateKeyGen(pk, mk, attr_list)
        sk_bytes = key.jsonify_sk(sk)
        sk_bytes = base64.b64encode(sk_bytes.encode())
        pk_bytes = key.jsonify_pk(pk)
        pk_bytes = base64.b64encode(pk_bytes.encode())

        print(pk_bytes)
        print(sk_bytes)

        conn.sendall(pk_bytes+sk_bytes)
    else:
        conn.sendall('Data does not match'.encode('utf-8'))
