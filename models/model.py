import os
import numpy as np
import requests
import json
from pyqrllib.pyqrllib import str2bin, XmssFast, mnemonic2bin, hstr2bin, bin2hstr, SHAKE_128, SHAKE_256, SHA2_256, getRandomSeed
from qrl.core.misc import logger
from qrl.crypto.xmss import XMSS
from qrl.crypto.xmss import XMSS, hash_functions
from qrl.core.Wallet import Wallet, WalletDecryptionError


class Model:
    def __init__(self):
        pass
        
    def getAddress(xmss_height, xmss_hash):
        seed = getRandomSeed(48, '')
        xmss = XMSS(XmssFast(seed, xmss_height, xmss_hash))
        return xmss.qaddress, xmss.mnemonic, xmss.hexseed
    def getMnemonic():
        xmss_height = 10
        seed = getRandomSeed(48, '')
        xmss = XMSS(XmssFast(seed, xmss_height))
        return xmss.mnemonic
    def getHexSeed():
        xmss_height = 10
        seed = getRandomSeed(48, '')
        xmss = XMSS(XmssFast(seed, xmss_height))
        return xmss.hexseed

    def recoverAddressHexseed(seed):
        bin_seed = hstr2bin(seed)
        recovered_xmss = XMSS.from_extended_seed(bin_seed)
        return recovered_xmss.qaddress

    def recoverAddressMnemonic(seed):
        bin_seed = mnemonic2bin(seed)
        recovered_xmss = XMSS.from_extended_seed(bin_seed)
        return recovered_xmss.qaddress

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