import json
from charm.core.engine.util import *
from charm.toolbox.msp import MSP
from charm.toolbox.pairinggroup import PairingGroup,ZR, G1, G2, GT
from charm.core.math.integer import integer,serialize,deserialize

class mySerializeAPI:
        def __init__(self):
            self.group = PairingGroup('SS512')
            self.util = MSP
        def serialize_ctxt(self, ctxt):
                #print(ctxt)
                ctxt['policy'] = ctxt['policy'].__str__()
                ctxt['Cp'] = self.group.serialize(ctxt['Cp'])
                ctxt['C_0'] = list(map(self.group.serialize, ctxt['C_0']))
                for dict_key, value in ctxt['C'].items():
                    for tuple_index, value in enumerate(ctxt['C'][dict_key]):
                        ctxt['C'][dict_key][tuple_index] = self.group.serialize(
                            value)
                return ctxt

        def deserialize_ctxt(self, ctxt):
            # print(type(ctxt))
            ctxt['policy'] = self.util.createPolicy(MSP,policy_string=ctxt['policy'])
            ctxt['Cp'] = self.group.deserialize(ctxt['Cp'])
            ctxt['C_0'] = list(map(self.group.deserialize, ctxt['C_0']))
            for dict_key, value in ctxt['C'].items():
                for tuple_index, value in enumerate(ctxt['C'][dict_key]):
                    ctxt['C'][dict_key][tuple_index] = self.group.deserialize(
                        value)
            return ctxt
        def jsonify_ctxt(self, ctxt):
            ctxt = self.serialize_ctxt(ctxt)
            ctxt['Cp'] = ctxt['Cp'].decode('utf-8')
            ctxt['C_0'] = list(map(lambda x: x.decode('utf-8'), ctxt['C_0']))
            for dict_key, value in ctxt['C'].items():
                for tuple_index, value in enumerate(ctxt['C'][dict_key]):
                    ctxt['C'][dict_key][tuple_index] = value.decode('utf-8')
            return json.dumps(ctxt)
        def unjsonify_ctxt(self, ctxt):
            ctxt = json.loads(ctxt)
            ctxt['Cp'] = ctxt['Cp'].encode('utf-8')
            ctxt['C_0'] = list(map(lambda x: x.encode('utf-8'), ctxt['C_0']))
            for dict_key, value in ctxt['C'].items():
                for tuple_index, value in enumerate(ctxt['C'][dict_key]):
                    ctxt['C'][dict_key][tuple_index] = value.encode('utf-8')
            return self.deserialize_ctxt(ctxt)