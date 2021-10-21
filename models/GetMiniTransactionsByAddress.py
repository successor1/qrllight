# coding=utf-8
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
import heapq
from os import stat
from grpc import ServicerContext, StatusCode
from pyqrllib.pyqrllib import str2bin, hstr2bin, bin2hstr

from qrl.core import config
from qrl.core.AddressState import AddressState
from qrl.core.OptimizedAddressState import OptimizedAddressState
from qrl.core.PaginatedBitfield import PaginatedBitfield
from qrl.core.Block import Block
from qrl.core.TransactionMetadata import TransactionMetadata
from qrl.core.ChainManager import ChainManager
from qrl.core.GenesisBlock import GenesisBlock
from qrl.core.State import State
from qrl.core.TransactionInfo import TransactionInfo
from qrl.core.txs.TransferTransaction import TransferTransaction
from qrl.core.misc import logger
from qrl.core.node import SyncState, POW
from qrl.core.p2p.p2pfactory import P2PFactory
from qrl.core.qrlnode import QRLNode
from qrl.crypto.misc import sha256
from qrl.generated import qrl_pb2
from qrl.services.PublicAPIService import PublicAPIService
from qrl.generated import qrl_pb2_grpc, qrl_pb2
import grpc
import base64

CONNECTION_TIMEOUT = 5

class TableOutput:
    pass

    def getMiniTransactionsByAddressHashes(qrl_address):
        binary_qrl_address = bytes(hstr2bin(qrl_address[1:]))
        node_public_address = 'testnet-1.automated.theqrl.org:19009'
        channel = grpc.insecure_channel(node_public_address)
        stub = qrl_pb2_grpc.PublicAPIStub(channel)
        request = qrl_pb2.GetMiniTransactionsByAddressReq(address=binary_qrl_address,
                                                              item_per_page=100000,
                                                              page_number=1)
        response = stub.GetMiniTransactionsByAddress(request, timeout=CONNECTION_TIMEOUT)
        transaction_hashes = []
        for i in range(len(response.mini_transactions)):
            transaction_hashes.append(response.mini_transactions[i].transaction_hash)
        return transaction_hashes

    def getMiniTransactionsByAddressAmount(qrl_address):
        binary_qrl_address = bytes(hstr2bin(qrl_address[1:]))
        node_public_address = 'testnet-1.automated.theqrl.org:19009'
        channel = grpc.insecure_channel(node_public_address)
        stub = qrl_pb2_grpc.PublicAPIStub(channel)
        request = qrl_pb2.GetMiniTransactionsByAddressReq(address=binary_qrl_address,
                                                              item_per_page=100000,
                                                              page_number=1)
        response = stub.GetMiniTransactionsByAddress(request, timeout=CONNECTION_TIMEOUT)
        amount = []
        for i in range(len(response.mini_transactions)):
            amount.append(response.mini_transactions[i].amount)
        return amount
            

    def GetTransactionsByAddressAddrFrom(qrl_address):
        binary_qrl_address = bytes(hstr2bin(qrl_address[1:]))
        node_public_address = 'testnet-1.automated.theqrl.org:19009'
        channel = grpc.insecure_channel(node_public_address)
        stub = qrl_pb2_grpc.PublicAPIStub(channel)
        request = qrl_pb2.GetTransactionsByAddressReq(address=binary_qrl_address,
                                                    item_per_page=1000000,
                                                    page_number=1)
        response = stub.GetTransactionsByAddress(request, timeout=CONNECTION_TIMEOUT)
        addr_from = []
        for i in range(len(response.transactions_detail)):
            addr_from.append("Q" + bin2hstr(response.transactions_detail[i].addr_from))
        return addr_from

    def GetTransactionsByAddressAmounts(qrl_address):
        binary_qrl_address = bytes(hstr2bin(qrl_address[1:]))
        node_public_address = 'testnet-1.automated.theqrl.org:19009'
        channel = grpc.insecure_channel(node_public_address)
        stub = qrl_pb2_grpc.PublicAPIStub(channel)
        request = qrl_pb2.GetTransactionsByAddressReq(address=binary_qrl_address,
                                                    item_per_page=1000000,
                                                    page_number=1)
        response = stub.GetTransactionsByAddress(request, timeout=CONNECTION_TIMEOUT)
        amount = []
        addrs_to = []
        test = []
        amount_length_data = []
        length_list = []
        for i in range(len(response.transactions_detail)):
            amount_length_data.append(response.transactions_detail[i].tx.transfer.amounts)
            for addrs in response.transactions_detail[i].tx.transfer.addrs_to:
                addrs_to.append("Q"+ bin2hstr(addrs))
            if response.transactions_detail[i].tx.transfer.amounts:
                for address, amounts in zip(response.transactions_detail[i].tx.transfer.addrs_to, response.transactions_detail[i].tx.transfer.amounts):
                    if qrl_address != "Q" + bin2hstr(bytes(address)):
                        test.append("-" + str(amounts / 1000000000))
                    elif qrl_address == "Q" + bin2hstr(bytes(address)):
                        test.append("+" + str(amounts / 1000000000))
            elif response.transactions_detail[i].tx.transfer_token.amounts:
                amount.append(str(response.transactions_detail[i].tx.transfer_token.amounts[0] / 10000000000) + " " + "Tokens")
            elif response.transactions_detail[i].tx.message.message_hash:
                try:
                    amount.append(response.transactions_detail[i].tx.message.message_hash.decode("utf-8"))
                except:
                    amount.append("Failed to decode")
            else:
                for addressAmount in response.transactions_detail[i].tx.token.initial_balances:
                    amount.append(str(addressAmount.amount / 10000000000) + " " + response.transactions_detail[i].tx.token.symbol.decode("utf-8"))
        for brackets in amount_length_data:
            length_list.append(len(brackets))
        out = []
        start=0
        for step in length_list:
            end = start+step
            l = list(map(float, test[start:end]))
            if len(set(i < 0 for i in l)) > 1:
                l = [i for i in l if i>0]
            s = sum(l)
            out.append('%s%.2f' % ('+' if s >=0 else '' , s))
            start = end
        x = 0
        for index, item in enumerate(out):
            if item == "+0.00":
                try:
                    out[index] = amount[x]
                except:
                    out[index] = amount[x - 1]
                x += 1
        return out

# print(TableOutput.GetTransactionsByAddressAmounts("Q010400b49d2ebb003d69db2a66cc179a87592649d9b83cfb32a1200f72dbc62b4aa4903b4dd322"))
# print(TableOutput.GetTransactionsByAddressAmounts("Q010400b49d2ebb003d69db2a66cc179a87592649d9b83cfb32a1200f72dbc62b4aa4903b4dd322"))

# Q0105006e70719c46cc85a69d6b7d0a1e642968d5c996fd9fa4b6641337f13ba2213749fd19dd11