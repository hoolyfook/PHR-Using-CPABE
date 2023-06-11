from charm.toolbox.pairinggroup import PairingGroup, GT, G1
from charm.toolbox.symcrypto import SymmetricCryptoAbstraction
from charm.toolbox.secretutil import SecretUtil
from charm.toolbox.ABEnc import ABEnc
from charm.toolbox.msp import MSP
from charm.toolbox.hash_module import Waters
from charm.toolbox.symcrypto import AuthenticatedCryptoAbstraction
from charm.core.math.pairing import hashPair as sha2
from charm.schemes.abenc.ac17 import AC17CPABE
import json
import pickle



class AC17CPABE_:
    def __init__(self):
        self.group = PairingGroup('MNT224')
        self.cpabe = AC17CPABE(self.group, 2)
    def gen_key(self):
        # Generate public key and master secret key
        pk, msk = self.cpabe.setup()
        return pk, msk
    def gen_sk(self, pk, msk, attr_list):
        # Generate secret key
        sk = self.cpabe.keygen(pk, msk, attr_list)
        return sk
    
    def encryption(self, pk, policy_str, msg):
        key = self.group.random(GT)
        c1 = self.cpabe.encrypt(pk, key, policy_str)
        cipher = AuthenticatedCryptoAbstraction(sha2(key))
        c2= cipher.encrypt(msg)
        print(type(c1))
        print(type(c2))
        result = {
        "c1": c1,
        "c2": c2
        }
        return result
    
    def decryption(self, pk, sk, cipher):
        c1 = cipher["c1"]
        c2 = cipher["c2"]
        try:
            
            key1 = self.cpabe.decrypt(pk, c1, sk)
            cipher1 = AuthenticatedCryptoAbstraction(sha2(key1))
            rec_msg = cipher1.decrypt(c2)
            return rec_msg
        except:
            print("You can't access")
            exit
    def verify_msg(self, msg, rec_msg):
        if rec_msg == msg:
            print("Successful decryption.")
        else:
            print("Decryption failed.")


if __name__ == '__main__':
    sourcefile = open("phr.json", 'rb')
    msg = sourcefile.read()
    sourcefile.close()
    msg_dict = json.loads(msg)


    abe = AC17CPABE_()
    # Generate public key and master secret key
    pk, msk = abe.gen_key()
    
    # Generate a key for a list of attributes
    attr_list = [msg_dict["ID"]]
    sk = abe.gen_sk(pk, msk, attr_list)

    # Generate a ciphertext
    # policy = '((ONE or THREE) or (TWO OR FOUR))'
    policy = '((' + msg_dict["ID"] + ' or ' + msg_dict["ID_BS"] + '))'

    cipher = abe.encryption(pk, policy, msg)

    re_msg = abe.decryption(pk, sk, cipher)

    re_msg_dict = json.loads(re_msg)
    with open('text.json', 'w', encoding='utf-8') as f:
        json.dump(re_msg_dict, f, ensure_ascii=False, indent=4)

    abe.verify_msg(msg, re_msg)