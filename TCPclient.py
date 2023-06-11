import socket
import json
import base64
from Include import SerializeKey as SerializeKey
from Include import CPABE as cp_abe

if __name__ == '__main__':
    # Kết nối đến máy chủ đích
    host = 'localhost'
    port = 62345
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Gửi chuỗi JSON qua kết nối
    with open('user.json', 'r') as file:
        json_data = json.load(file)
    json_str = json.dumps(json_data)
    print(json_str)
    client_socket.sendall(json_str.encode('utf-8'))
    print("Sended")

    # Đợi phản hồi từ server
    key = SerializeKey.serializeKey()

    # receive the first response
    response = ''
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            response += data.decode('utf-8')
        except socket.timeout:
            print('Timeout occurred')
            break

    response1 = response[:880]
    response2 = response[880:]

    pk_bytes = base64.b64decode(response1)
    pk = key.unjsonify_pk(pk_bytes)
    print(pk)

    sk_bytes = base64.b64decode(response2)
    sk = key.unjsonify_sk(sk_bytes)
    print(sk)

    # Đóng kết nối
    client_socket.close()

    abe = cp_abe.CP_ABE()
    plt = abe.ABEdecryption('phr.json.scd', pk, sk)
    print(plt)

    with open('text.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(plt.decode('utf-8'), ensure_ascii=False, indent=4))
