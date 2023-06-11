from charm.toolbox.pairinggroup import PairingGroup,ZR, G1, G2, GT
from charm.core.engine.util import *
from charm.schemes.abenc.ac17 import AC17CPABE
from charm.toolbox.msp import MSP
from Include import AC17Serialize as AC17Serialize
from Include import CPABE as cp_abe
from Include import SerializeKey as SerializeKey
from Crypto.Util.number import bytes_to_long,long_to_bytes
import json

if __name__ == '__main__':
    sourcefile = open("phr.json", 'rb')
    msg = sourcefile.read()
    sourcefile.close()
    msg_dict = json.loads(msg)
    policy = '((' + msg_dict["ID"] + ') or (' 
    for item in msg_dict['NGUOIPHUTRACH']:
        if msg_dict['NGUOIPHUTRACH'][-1] != item:
            policy += "(" + item['ID'] + ' and ' + item['khoa'].upper() + ")" + " or "
        else:
            policy += "(" + item['ID'] + ' and ' + item['khoa'].upper() + ")" + '))'

    print(policy)
    #attr_list = [msg_dict["ID"]]
    attr_list = ["BS001", "psychology".upper()]

    # convert attr_list to a JSON string
    attr_list_json = json.dumps(attr_list)

    # write JSON string to file
    with open("attr.txt", "w") as sourcefile:
        sourcefile.write(attr_list_json)

    abe = cp_abe.CP_ABE()
    key = SerializeKey.serializeKey()

    pk, mk = abe.KeyGen()

    key.save_file_mk(mk)
    key.save_file_pk(pk)

    mk1 = key.load_file_mk()
    pk1 = key.load_file_pk()
    
    
    sk = abe.PrivateKeyGen(pk1, mk1, attr_list )
    sk = key.serialize_sk(sk)
    sk = key.deserialize_sk(sk)

    cipher, cipherName = abe.ABEencryption('phr.json', pk1, policy)

    sourcefile = open(cipherName, 'wb')
    sourcefile.write(cipher)
    sourcefile.close()

    plt = abe.ABEdecryption(cipherName, pk1, sk)
    print(plt)
    
    # with open('text.json', 'w', encoding='utf-8') as f:
    #     json.dump(plt, f, ensure_ascii=False, indent=4)
