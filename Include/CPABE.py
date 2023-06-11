from charm.toolbox.pairinggroup import PairingGroup,ZR, G1, G2, GT
from charm.core.engine.util import *
from charm.schemes.abenc.ac17 import AC17CPABE
from . import AC17Serialize as ac17
from Crypto.Util.number import bytes_to_long,long_to_bytes
from Crypto.Cipher import AES 
import hashlib , base64, zlib, json
import binascii
import os
import pickle
import struct
"""
===============================================================================================
Encryption : 
1. Random session_key 
2. Encrypt session_key with CP-ABE , this produced session_key_ctxt 
3. Serialize session_key_ctxt then attach to the output file
4. Pack the length of serialized session_key_ctxt and write to the first 8 bytes of output
6. Random IV (16 bytes) then write to the output file
7. Hash the session_key to make aes_key
8. Encrypt the file with AES256-CFB then write the encrypted data to the output 
===============================================================================================
Output file structure : [8][16][session_key][encrypted_data]
===============================================================================================
Decryption : 
1. Extract the session_key_size , IV 
2. Recover session_key_ctxt_b = ciphertext[24:session_key_len+24] 
3. Deserialized session_key_ctxt_b then decrypt it
4. If policy satisfied to decrypt the session_key_ctxt_b, we hash the session_key to retrive the 
aes_key
5. Decrypt the file with aes_key
===============================================================================================


"""
class CP_ABE:

    def __init__(self):
        self.groupObj = PairingGroup('SS512')
        self.cpabe = AC17CPABE(self.groupObj,2)

    def ABEencryption(self, filename,pk,policy):
        msg = open(filename,"rb").read()
        """
        Create Session key then encrypt with CP-ABE 
        Encode Session key and attach to file
        """

        serialize_encoder = ac17.mySerializeAPI()


        session_key = self.groupObj.random(GT)
        session_key_ctxt = self.cpabe.encrypt(pk,session_key,policy)

        session_key_ctxt_b = serialize_encoder.jsonify_ctxt(session_key_ctxt)
        session_key_ctxt_b = base64.b64encode(session_key_ctxt_b.encode())
        session_key_size = len(session_key_ctxt_b)
        stream = struct.pack('Q',session_key_size)
        namesplit = filename.split('/')
        outname = f"{namesplit[len(namesplit)-1]}.scd"

        """
        Use AES to encrypt the file then attach needed component
        """

        aes_key = hashlib.sha256(str(session_key).encode()).digest()
        iv = os.urandom(16)

        encryptor = AES.new(aes_key,AES.MODE_CFB,iv)
        encrypted_data = encryptor.encrypt(msg)
        output = stream + iv + session_key_ctxt_b + encrypted_data

        return output,outname.encode()


    def ABEdecryption(self, filename,pk,sk):
        serialize_encoder = ac17.mySerializeAPI()
        ciphertext_stream = open(filename,"rb")
        session_key_size = struct.unpack('Q',ciphertext_stream.read(struct.calcsize('Q')))[0]
        ciphertext_stream.close()
        ciphertext = open(filename,"rb").read()
        iv = ciphertext[8:24]
        session_key_ctxt_b = ciphertext[24:session_key_size+24]
        session_key_ctxt_b = base64.b64decode(session_key_ctxt_b)
        session_key_ctxt = serialize_encoder.unjsonify_ctxt(session_key_ctxt_b)
        session_key = self.cpabe.decrypt(pk,session_key_ctxt,sk)
        #output_filename = filename.replace('./ServerStorage/','').replace('.scd','')
        if(session_key):
            aes_key = hashlib.sha256(str(session_key).encode()).digest()
            encryptor = AES.new(aes_key,AES.MODE_CFB,iv)
            decrypted_data = encryptor.decrypt(ciphertext[8+16+session_key_size:])

            return decrypted_data
        else:
            return None

    def LoadKey(self, key):
        key = bytesToObject(key, self.groupObj)
        return key

    def KeyToBytes(self, pk,mk):
        pkb = objectToBytes(pk, self.groupObj)
        mkb = objectToBytes(mk, self.groupObj)
        return pkb,mkb

    def KeyGen(self):
        (pk,mk) = self.cpabe.setup()
        return pk,mk

    def PrivateKeyGen(self, pk,mk,attribute):
        sk = self.cpabe.keygen(pk,mk,attribute)
        return sk 
