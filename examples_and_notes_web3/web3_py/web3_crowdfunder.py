import json
import web3.eth as asd

from web3 import Web3
from solc import compile_source
from web3.contract import ConciseContract



# read solidity smart contract
with open("CrowdFunder.sol") as f:
    smrt_cnt=f.read()

#print(smrt_cnt)

# compile solidity
compiled_sol = compile_source(smrt_cnt)
contract_interface = compiled_sol['<stdin>:CrowdFunder']

# tester this code instance web3 and create ten account
# with values assigned (ether value, address ... )
w3 = Web3(Web3.EthereumTesterProvider())

# default account assigned
w3.eth.defaultAccount = w3.eth.accounts[0]
# address_1 =  w3.eth.accounts[0]
print(w3.eth.defaultAccount)

# Instantiate and deploy contract

Funder = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
# In the CrowdFunder contract, the contractor takes certain values, so the values are written here
tx_hash=Funder.constructor(5, "ASDDSA", w3.eth.accounts[1], 7).transact()
#print(w3.eth.getTransactionReceipt(tx_hash))

# Wait for the transaction to be mined, and get the transaction receipt
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
#print(tx_receipt)

# Create the contract instance with the newly-deployed address
greeter = w3.eth.contract(
    address=tx_receipt.contractAddress,
    abi=contract_interface['abi'],
)

# send token
tx_hash=greeter.functions.contribute().transact({'value': w3.toWei(8, 'wei')})
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

print(tx_receipt) # show mined transaction
print(w3.eth.blockNumber) # show total block number
print(w3.eth.getBlock('latest')) # or w3.eth.getBlock(4), show specific block

#show transaction
print(w3.eth.getTransaction(tx_hash))
print(w3.eth.getTransactionReceipt(tx_hash))

# show currency
print(w3.eth.getBalance(w3.eth.accounts[0]))
print(w3.eth.getBalance(w3.eth.accounts[1]))

# show event, part of the CrowdFunder.sol shown with the 'event' keyword
print(greeter.events.LogFundingReceived().processReceipt(tx_receipt))
print(greeter.events.LogWinnerPaid().processReceipt(tx_receipt))