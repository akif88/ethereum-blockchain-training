import json
import web3

from web3 import Web3
from solc import compile_source
from web3.contract import ConciseContract

# Solidity source code
with open("Greeter.sol") as f:
    contract_source_code = f.read()


# Compiled source code
compiled_sol = compile_source(contract_source_code)
contract_interface = compiled_sol['<stdin>:Greeter']

# web3.py instance
w3 = Web3(Web3.EthereumTesterProvider())

# set pre-funded(önceden finanse edilen) account as sender
w3.eth.defaultAccount = w3.eth.accounts[0]
#print(w3.eth.accounts)
print(w3.eth.getBalance(w3.eth.defaultAccount))

# Instantiate and deploy contract
Greeter = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

# Submit the transaction that deploys the contract
tx_hash = Greeter.constructor().transact()

# Wait for the transaction to be mined, and get the transaction receipt
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

# Create the contract instance with the newly-deployed address
greeter = w3.eth.contract(
    address=tx_receipt.contractAddress,
    abi=contract_interface['abi'],
)


# Display the default greeting from the contract
print('Default contract greeting: {}'.format(
    greeter.functions.greet().call()
))

print('Setting the greeting to Nihao...')
tx_hash = greeter.functions.setGreeting('Nihao').transact()

# Wait for transaction to be mined...
w3.eth.waitForTransactionReceipt(tx_hash)

# Display the new greeting value
print('Updated contract greeting: {}'.format(
    greeter.functions.greet().call()
))

# When issuing a lot of reads, try this more concise reader:
reader = ConciseContract(greeter)
assert reader.greet() == "Nihao"
