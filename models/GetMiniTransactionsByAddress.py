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

    def GetTransactionsByAddress(qrl_address):
        binary_qrl_address = bytes(hstr2bin(qrl_address[1:]))
        node_public_address = 'testnet-1.automated.theqrl.org:19009'
        channel = grpc.insecure_channel(node_public_address)
        stub = qrl_pb2_grpc.PublicAPIStub(channel)
        request = qrl_pb2.GetTransactionsByAddressReq(address=binary_qrl_address,
                                                    item_per_page=1000000,
                                                    page_number=1)
        response = stub.GetTransactionsByAddress(request, timeout=CONNECTION_TIMEOUT)
        amount = []
        test = []
        testtwo = []
        for i in range(len(response.transactions_detail)):
            amount.append(response.transactions_detail[i].tx.transfer.addrs_to)
            test.append(response.transactions_detail[i].tx.transfer.amounts)
        addrs_to_outputs = []
        addrs_to = []
        for amounts in amount:
            addrs_to_outputs.append(amounts)
        for i in addrs_to_outputs:
            for j in i:
                addrs_to.append("Q"+ bin2hstr(j))
        for z in test:
            for j in z:
                testtwo.append(j)
        new_list = []
        length_list = []
        for qrl_addresses, shor_amounts  in zip(amount, test):
            length_list.append(len(shor_amounts))
            for a, b in zip(qrl_addresses,shor_amounts):
                if bytes(hstr2bin(qrl_address[1:])) != a:
                    new_list.append("-" + str(b / 1000000000))
                elif bytes(hstr2bin(qrl_address[1:])) == a:
                    new_list.append("+" + str(b / 1000000000))
        out = []
        start=0
        for step in length_list:
            end = start+step
            l = list(map(float, new_list[start:end]))
            if len(set(i < 0 for i in l)) > 1:
                l = [i for i in l if i>0]
            s = sum(l)
            out.append('%s%.1f' % ('+' if s >=0 else '' , s))
            start = end
        for i in addrs_to:
            print(bytes(hstr2bin(i)))
        print(out)
            

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

    # def GetTransactionsByAddressAddrTo(qrl_address):
    #     binary_qrl_address = bytes(hstr2bin(qrl_address[1:]))
    #     node_public_address = 'testnet-1.automated.theqrl.org:19009'
    #     channel = grpc.insecure_channel(node_public_address)
    #     stub = qrl_pb2_grpc.PublicAPIStub(channel)
    #     request = qrl_pb2.GetTransactionsByAddressReq(address=binary_qrl_address,
    #                                                 item_per_page=1000000,
    #                                                 page_number=1)
    #     response = stub.GetTransactionsByAddress(request, timeout=CONNECTION_TIMEOUT)
    #     addrs_to = []
    #     for i in range(len(response.transactions_detail)):
    #         addrs_to.append("Q" + bin2hstr(response.transactions_detail[i].tx.transfer.addrs_to[0]))
    #     return addrs_to

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
        for i in range(len(response.transactions_detail)):
            amount.append(response.transactions_detail[i].tx.token.initial_balances)
        return amount


# print(TableOutput.GetTransactionsByAddressAmounts("Q010400b49d2ebb003d69db2a66cc179a87592649d9b83cfb32a1200f72dbc62b4aa4903b4dd322"))
# print(TableOutput.GetTransactionsByAddressAmounts("Q010400b49d2ebb003d69db2a66cc179a87592649d9b83cfb32a1200f72dbc62b4aa4903b4dd322"))

# Q0105006e70719c46cc85a69d6b7d0a1e642968d5c996fd9fa4b6641337f13ba2213749fd19dd11