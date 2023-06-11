from charm.toolbox.pairinggroup import PairingGroup,ZR, G1, G2, GT
from charm.core.engine.util import *
from charm.toolbox.msp import MSP
import pickle
import json


class serializeKey:
    def __init__(self):
        self.group = PairingGroup('SS512')
        self.util = MSP
    def serialize_pk(self, pk):
        pk['h_A'] = list(map(self.group.serialize, pk['h_A']))
        pk['e_gh_kA'] = list(map(self.group.serialize, pk['e_gh_kA']))
        return pk
    def deserialize_pk(self, pk):
        pk['h_A'] = list(map(self.group.deserialize, pk['h_A']))
        pk['e_gh_kA'] = list(map(self.group.deserialize, pk['e_gh_kA']))
        return pk
    def save_file_pk(self, pk):
        keyser = self.serialize_pk(pk)
        encryptedfile = open("pk.pem", 'wb')
        pickle.dump(keyser, encryptedfile)
        encryptedfile.close()
    def load_file_pk(self):
        encryptedfile = open("pk.pem", 'rb')
        keydeser = pickle.load(encryptedfile)
        keydeser = self.deserialize_pk(keydeser)
        return keydeser
    def serialize_mk(self, mk):
        mk['g'] = self.group.serialize(mk['g'])
        mk['h'] = self.group.serialize(mk['h'])
        mk['g_k'] = list(map(self.group.serialize, mk['g_k']))
        mk['A'] = list(map(self.group.serialize, mk['A']))
        mk['B'] = list(map(self.group.serialize, mk['B']))
        return mk
    def deserialize_mk(self, mk):
        # print(type(mk))
        mk['g'] = self.group.deserialize(mk['g'])
        mk['h'] = self.group.deserialize(mk['h'])
        mk['g_k'] = list(map(self.group.deserialize, mk['g_k']))
        mk['A'] = list(map(self.group.deserialize, mk['A']))
        mk['B'] = list(map(self.group.deserialize, mk['B']))
        return mk
    def save_file_mk(self, mk):
        keyser = self.serialize_mk(mk)
        encryptedfile = open("msk.pem", 'wb')
        pickle.dump(keyser, encryptedfile)
        encryptedfile.close()
    def load_file_mk(self):
        encryptedfile = open("msk.pem", 'rb')
        keydeser = pickle.load(encryptedfile)
        keydeser = self.deserialize_mk(keydeser)
        return keydeser
    def serialize_sk(self, sk):
        sk['attr_list'] = list(map(lambda x: x.encode('utf-8'), sk['attr_list']))
        sk['K_0'] = list(map(self.group.serialize, sk['K_0']))
        for dict_key, value in sk['K'].items():
            for tuple_index, value in enumerate(sk['K'][dict_key]):
                sk['K'][dict_key][tuple_index] = self.group.serialize(
                    value)
        sk['Kp'] = list(map(self.group.serialize, sk['Kp']))
        return sk
    def deserialize_sk(self, sk):
        sk['attr_list'] = list(map(lambda x: x.decode('utf-8'), sk['attr_list']))
        sk['K_0'] = list(map(self.group.deserialize, sk['K_0']))
        for dict_key, value in sk['K'].items():
            for tuple_index, value in enumerate(sk['K'][dict_key]):
                sk['K'][dict_key][tuple_index] = self.group.deserialize(
                    value)
        sk['Kp'] = list(map(self.group.deserialize, sk['Kp']))
        return sk
    def jsonify_sk(self, sk):
        sk = self.serialize_sk(sk)
        sk['attr_list'] = list(map(lambda x: x.decode('utf-8'), sk['attr_list']))
        sk['K_0'] = list(map(lambda x: x.decode('utf-8'), sk['K_0']))
        for dict_key, value in sk['K'].items():
            for tuple_index, value in enumerate(sk['K'][dict_key]):
                sk['K'][dict_key][tuple_index] = value.decode('utf-8')
        sk['Kp'] = list(map(lambda x: x.decode('utf-8'), sk['Kp']))
        return json.dumps(sk)
    def unjsonify_sk(self, sk):
        sk = json.loads(sk)
        sk['attr_list'] = list(map(lambda x: x.encode('utf-8'), sk['attr_list']))
        sk['K_0'] = list(map(lambda x: x.encode('utf-8'), sk['K_0']))
        for dict_key, value in sk['K'].items():
            for tuple_index, value in enumerate(sk['K'][dict_key]):
                sk['K'][dict_key][tuple_index] = value.encode('utf-8')
        sk['Kp'] = list(map(lambda x: x.encode('utf-8'), sk['Kp']))
        return self.deserialize_sk(sk)

    def jsonify_pk(self, pk):
        pk = self.serialize_pk(pk)
        pk['e_gh_kA'] = list(map(lambda x: x.decode('utf-8'), pk['e_gh_kA']))
        pk['h_A'] = list(map(lambda x: x.decode('utf-8'), pk['h_A']))
        return json.dumps(pk)
    def unjsonify_pk(self, pk):
        pk = json.loads(pk)
        pk['e_gh_kA'] = list(map(lambda x: x.encode('utf-8'), pk['e_gh_kA']))
        pk['h_A'] = list(map(lambda x: x.encode('utf-8'), pk['h_A']))
        return self.deserialize_pk(pk)
