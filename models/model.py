import requests
import json
from pyqrllib.pyqrllib import XmssFast, mnemonic2bin, hstr2bin, getRandomSeed
from qrl.crypto.xmss import XMSS
from qrl.crypto.xmss import XMSS


class Model:
    def __init__(self):
        pass
        
    def getAddress(xmss_height, xmss_hash):
        seed = getRandomSeed(48, '')
        xmss = XMSS(XmssFast(seed, xmss_height, xmss_hash))
        return xmss.qaddress, xmss.mnemonic, xmss.hexseed

    def getAddressExperimental(xmss_height, xmss_hash, mouse_seed):
        xmss = XMSS(XmssFast(mouse_seed, xmss_height, xmss_hash))
        return xmss.qaddress, xmss.mnemonic, xmss.hexseed

    def recoverAddressHexseed(seed):
        bin_seed = hstr2bin(seed)
        recovered_xmss = XMSS.from_extended_seed(bin_seed)
        return recovered_xmss.qaddress

    def recoverAddressMnemonic(seed):
        bin_seed = mnemonic2bin(seed)
        recovered_xmss = XMSS.from_extended_seed(bin_seed)
        return recovered_xmss.qaddress

    def recoverMnemonicHexseed(seed):
        bin_seed = hstr2bin(seed)
        recovered_xmss = XMSS.from_extended_seed(bin_seed)
        return recovered_xmss.mnemonic

    def recoverHexseedMnemonic(seed):
        bin_seed = mnemonic2bin(seed)
        recovered_xmss = XMSS.from_extended_seed(bin_seed)
        return recovered_xmss.hexseed
    
    def getAddressBalance(address):
        request = requests.get('https://testnet-explorer.theqrl.org/api/a/'+address)
        response = request.text
        getAddressResp = json.loads(response)
        jsonResponse = getAddressResp
        return jsonResponse["state"]["balance"]

    def getAddressOtsKeyIndex(address):
        request = requests.get('https://testnet-explorer.theqrl.org/api/a/'+address)
        response = request.text
        getAddressResp = json.loads(response)
        jsonResponse = getAddressResp
        return jsonResponse["state"]["used_ots_key_count"]

    
    def getTransactionByHash(tx_hash):
        request = requests.get('https://testnet-explorer.theqrl.org/api/tx/'+tx_hash)
        response = request.text
        getTXResp = json.loads(response)
        jsonResponse = getTXResp
        return(jsonResponse)


# getting timestamp from transaction hash
# print(Model.getTransactionByHash("992ac5dfdedf7259fed52ce406e961556796fc238ab79cb43331655b670b627a")["transaction"]["header"]["timestamp_seconds"])

# #getting amount from transaction hash
# print(Model.getTransactionByHash("357db33e4fc2944fe6bb3bc630a710df7e107e8394fa154196a6ce7db705e786")["transaction"]["tx"]["amount"])

# #check if it comes from own address or not (+ or -)
# print(Model.getTransactionByHash("1f2a9b8784cc45c41efed0519bc85d3c7040c0f59faf9767f1415f252c8ea81d")["transaction"]["explorer"]["from_hex"])
