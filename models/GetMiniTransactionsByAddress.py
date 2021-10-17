# coding=utf-8
# Distributed under the MIT software license, see the accompanying
# file LICENSE or http://www.opensource.org/licenses/mit-license.php.
import heapq
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
                                                              item_per_page=1000,
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
                                                              item_per_page=1000,
                                                              page_number=1)
        response = stub.GetMiniTransactionsByAddress(request, timeout=CONNECTION_TIMEOUT)
        amount = []
        for i in range(len(response.mini_transactions)):
            amount.append(response.mini_transactions[i].amount)
        return amount

# print(TableOutput.getMiniTransactionsByAddressHashes("Q0105006e70719c46cc85a69d6b7d0a1e642968d5c996fd9fa4b6641337f13ba2213749fd19dd11"))

# Q0105006e70719c46cc85a69d6b7d0a1e642968d5c996fd9fa4b6641337f13ba2213749fd19dd11