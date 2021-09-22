import os
from binascii import hexlify, a2b_base64
from collections import namedtuple
from decimal import Decimal
from random import seed
from typing import List

import grpc
import simplejson as json
from google.protobuf.json_format import MessageToJson
from pyqrllib.pyqrllib import mnemonic2bin, hstr2bin, bin2hstr

from qrl.core import config
from qrl.core.Wallet import Wallet, WalletDecryptionError
from qrl.core.misc.helper import parse_hexblob, parse_qaddress
from qrl.core.MultiSigAddressState import MultiSigAddressState
from qrl.core.txs.MessageTransaction import MessageTransaction
from qrl.core.txs.SlaveTransaction import SlaveTransaction
from qrl.core.txs.TokenTransaction import TokenTransaction
from qrl.core.txs.Transaction import Transaction
from qrl.core.txs.TransferTokenTransaction import TransferTokenTransaction
from qrl.core.txs.TransferTransaction import TransferTransaction
from qrl.core.txs.multisig.MultiSigCreate import MultiSigCreate
from qrl.core.txs.multisig.MultiSigSpend import MultiSigSpend
from qrl.crypto.xmss import XMSS, hash_functions
from qrl.generated import qrl_pb2_grpc, qrl_pb2
from qrl.crypto.doctest_data import *

from models.model import Model

def slave_tx_generate(xmss_pk, src_xmss, xmss):
    """
    Generates Slave Transaction for the wallet
    """
    access_types = []
    fee_shor = 0
    master_addr = None

    slave_xmss = []
    slave_pks = []
    slave_xmss_seed = []

    for i in range(100):
        print("Generating Slave #" + str(i + 1))
        xmss = XMSS.from_height(config.dev.xmss_tree_height)
        slave_xmss.append(xmss)
        slave_xmss_seed.append(xmss.extended_seed)
        slave_pks.append(xmss.pk)
        access_types.append(0)
        print("Successfully Generated Slave %s/%s" % (str(i + 1), 100))

    try:
        tx = SlaveTransaction.create(slave_pks = slave_pks,
                                    access_types = access_types,
                                    fee = fee_shor,
                                    xmss_pk = src_xmss.pk,
                                    master_addr = master_addr)
        tx.sign(src_xmss)
        with open('slaves.json', 'w') as f:
            json.dump([bin2hstr(src_xmss.address), slave_xmss_seed, tx.to_json()], f)
        print('Successfully created slaves.json')
        print('Move slaves.json file from current directory to the mining node inside ~/.qrl/')
    except Exception as e:
        print("Unhandled error: {}".format(str(e)))
        quit(1)