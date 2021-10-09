from solc import compile_source

from web3 import Web3

# read smart-contract
with open("RegistrarContract.sol") as f:
    smart_contract = f.read()

#compile smart contract solidity with solc
compiled_solidity = compile_source(smart_contract)
contract_interface = compiled_solidity['<stdin>:RegistrarContract']

# create web3 object
w3 = Web3(Web3.EthereumTesterProvider())
#w3 = Web3(Web3.IPCProvider("/home/akif/.ethereum/geth.ipc"))

# Instantiate and deploy contract
Registrar = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])


# add new account blockchainas as a paitent
name_personal = input("Enter Your User Name: ")
pass_personal = input("Enter Your New Pass: ")
new_addr = w3.personal.newAccount(pass_personal)

print(name_personal)
print(new_addr)

w3.eth.defaultAccount = w3.eth.accounts[0]

print(w3.personal.listAccounts)


# add blockchain new personal with constructor
tx_hash = Registrar.constructor().transact()
#  Wait for the transaction to be mined, and get the transaction receipt
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
#print(tx_receipt)

print(Web3.fromWei(w3.eth.getBalance(w3.eth.accounts[0]), 'wei'))
print(w3.eth.getBalance(new_addr))


registry = w3.eth.contract(
    address=tx_receipt.contractAddress,
    abi=contract_interface['abi'],
)

tx_hash = registry.functions.initialAccount(new_addr, name_personal.encode(), 8).transact({'value': w3.toWei(8, 'wei')})
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

print(w3.eth.getBalance(new_addr))
print(Web3.fromWei(w3.eth.getBalance(w3.eth.accounts[0]), 'wei'))

print(tx_receipt)

# add provider new patient record
# add new account blockchainas as a paitent
name_personal = input("Enter Your User Name: ")
pass_personal = input("Enter Your New Pass: ")
new_addr = w3.personal.newAccount(pass_personal)

print(name_personal)
print(new_addr)

# loop if err then enter new username
try:
    tx_hash = registry.functions.initialAccount(new_addr, name_personal.encode(), 8).transact({'value': w3.toWei(8, 'wei')})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
except:
    print("already exist that username")

print(tx_receipt)

# this can be used with local db
print(registry.events.LogAccountAdded().processReceipt(tx_receipt))
events = registry.events.LogAccountAdded().processReceipt(tx_receipt);
print("username: {}".format(events[0]['args']['_username'].decode()))
print("patient address: {}".format(events[0]['args']['_patientAddress']))

tx_hash = registry.functions.summaryContractReference(name_personal.encode(), new_addr).transact()
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)


print(w3.personal.listAccounts)

print(w3.eth.getBalance(new_addr))
print(Web3.fromWei(w3.eth.getBalance(w3.eth.accounts[0]), 'wei'))

print(tx_receipt)


print(registry.functions.getAddress(name_personal.encode()).call())


# -----------Summary Constract--------------

# read smart-contract
with open("SummaryContract.sol") as f:
    smart_contract = f.read()

#compile smart contract solidity with solc
compiled_solidity_SC = compile_source(smart_contract)
contract_interface_SC = compiled_solidity_SC['<stdin>:SummaryContract']

# Instantiate and deploy contract
Summary = w3.eth.contract(abi=contract_interface_SC['abi'], bytecode=contract_interface_SC['bin'])

print(w3.personal.listAccounts)


# search patient address with username in RegistrarContract
username = input("Enter Your Username: ")
patient_address = registry.functions.getAddress(username.encode()).call()


# add blockchain new summary constract with constructor
tx_hash = Summary.constructor(patient_address).transact()
#  Wait for the transaction to be mined, and get the transaction receipt
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
print(tx_receipt)


# Create the contract instance with the newly-deployed address
summary = w3.eth.contract(
    address=tx_receipt.contractAddress,
    abi=contract_interface_SC['abi'],
)

print("Provider Address: {}".format(summary.functions.getProviderAddress().call()))
print("Patient Address: {}".format(summary.functions.getPatientAddress().call()))

print("SC Status for PPR: {}".format(summary.functions.getStatus(patient_address).call()))
tx_hash = summary.functions.setStatus(patient_address).transact()
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
print("SC Status for PPR: {}".format(summary.functions.getStatus(patient_address).call()))
print(tx_receipt)
print(summary.address)


#------------PPR Contract------------------------

# read smart-contract
with open("PatientProviderRelationship.sol") as f:
    smart_contract = f.read()

#compile smart contract solidity with solc
compiled_solidity_PPR = compile_source(smart_contract)
contract_interface_PPR = compiled_solidity_PPR['<stdin>:PatientProviderRelationship']

Relationship = w3.eth.contract(abi=contract_interface_PPR['abi'], bytecode=contract_interface_PPR['bin'])

from web3 import miner
#tx_hash = Relationship.constructor(patient_address).transact()
print(w3.eth.coinbase)
asd = miner.Miner(w3)
#asd.setEtherBase(w3.eth.accounts[1])
print(w3.eth.coinbase)

#print(w3.eth.getBlock(3))
