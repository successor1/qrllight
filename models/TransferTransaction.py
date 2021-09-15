import os
from binascii import hexlify, a2b_base64
from collections import namedtuple
from decimal import Decimal
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

def _quanta_to_shor(x: Decimal, base=Decimal(config.dev.shor_per_quanta)) -> int:
    print(int(Decimal(x * base).to_integral_value()))

def tx_unbase64(tx_json_str):
    tx_json = json.loads(tx_json_str)
    tx_json["publicKey"] = base64tohex(tx_json["publicKey"])
    tx_json["signature"] = base64tohex(tx_json["signature"])
    tx_json["transactionHash"] = base64tohex(tx_json["transactionHash"])
    tx_json["transfer"]["addrsTo"] = [base64tohex(v) for v in tx_json["transfer"]["addrsTo"]]
    return json.dumps(tx_json, indent=True, sort_keys=True)

def base64tohex(data):
    return hexlify(a2b_base64(data))

CONNECTION_TIMEOUT = 5
def tx_transfer(addrs_to, amounts, message_data, fee, xmss_pk, src_xmss, ots_key):
 # Create transaction
    
    tx = TransferTransaction.create(addrs_to = addrs_to,
                                        amounts = amounts,
                                        message_data = message_data,
                                        fee = fee,
                                        xmss_pk= xmss_pk,
                                        master_addr=None)

        # Sign transaction
    src_xmss = src_xmss
    src_xmss.set_ots_index(ots_key)
    tx.sign(src_xmss)

        # Print result
    txjson = tx_unbase64(tx.to_json())
    print(txjson)

    if not tx.validate():
        print("It was not possible to validate the signature")
        quit(1)

    print("\nTransaction Blob (signed): \n")
    txblob = tx.pbdata.SerializeToString()
    txblobhex = hexlify(txblob).decode()
    print(txblobhex)

    # Push transaction
    print("Sending to a QRL Node...")
    node_public_address = 'mainnet-1.automated.theqrl.org:19009'
    channel = grpc.insecure_channel(node_public_address)
    stub = qrl_pb2_grpc.PublicAPIStub(channel)
    push_transaction_req = qrl_pb2.PushTransactionReq(transaction_signed=tx.pbdata)
    push_transaction_resp = stub.PushTransaction(push_transaction_req, timeout=CONNECTION_TIMEOUT)

    # Print result
    print(push_transaction_resp)