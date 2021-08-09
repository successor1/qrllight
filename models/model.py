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

    def getAddress():
        xmss_height = 10
        seed = getRandomSeed(48, '')
        xmss = XMSS(XmssFast(seed, xmss_height))
        print(xmss.qaddress)
        print(xmss.mnemonic)
        print(xmss.hexseed)

    def recoverAddress():
        seed = ""
        bin_seed = mnemonic2bin(seed)
        recovered_xmss = XMSS.from_extended_seed(bin_seed)
        print(recovered_xmss.qaddress)

    # def getAddressBalance():
    #     address = "Q01050048f13d469bd98bd83ae31427e6fd980a299016cfbbfe6802e36123c42e98350d4103e983"
    #     request = requests.get('https://explorer.theqrl.org/api/a/'+address)
    #     response = request.text
    #     getAddressResp = json.loads(response)
    #     jsonResponse = getAddressResp
    #     print(jsonResponse)


Model.getAddressBalance()