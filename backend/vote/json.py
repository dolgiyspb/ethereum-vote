from flask.json import JSONEncoder
from web3.utils.datastructures import HexBytes

class CustomJSONEncoder(JSONEncoder):

    def default(self, obj):
        if isinstance(obj, HexBytes):
            return obj.hex()
        return JSONEncoder.default(self, obj)