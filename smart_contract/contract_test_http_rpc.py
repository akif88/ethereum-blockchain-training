from solc import compile_source
from web3 import Web3, HTTPProvider
from web3 import admin, personal, eth, miner


# read smart-contract
with open("MyToken.sol") as f:
    smart_contract = f.read()

# compile MyToken smart contract with solc
compiled_solidity_MT = compile_source(smart_contract)
contract_interface_MT = compiled_solidity_MT['<stdin>:MyToken']

    
# read smart-contract
with open("RegistrarContract.sol") as f:
    smart_contract = f.read()

#compile smart contract solidity with solc
compiled_solidity = compile_source(smart_contract)
contract_interface = compiled_solidity['<stdin>:RegistrarContract']


# read smart-contract
with open("SummaryContract.sol") as f:
    smart_contract = f.read()

#compile smart contract solidity with solc
compiled_solidity_SC = compile_source(smart_contract)
contract_interface_SC = compiled_solidity_SC['<stdin>:SummaryContract']

# read smart-contract
with open("PatientProviderRelationship.sol") as f:
    smart_contract = f.read()

#compile smart contract solidity with solc
compiled_solidity_PPR = compile_source(smart_contract)
contract_interface_PPR = compiled_solidity_PPR['<stdin>:PatientProviderRelationship']


# used with geth
w3 = Web3(HTTPProvider("http://127.0.0.1:8545"))

admin_w3 = admin.Admin(w3)
# not work, why? started with geth console > admin.startRPC()
#admin_w3.startRPC()

print(w3.isConnected())
print(admin_w3.peers)
print(admin_w3.nodeInfo)

# start personal to create, list etc.
personal_w3 = personal.Personal(w3)
# start ethereum
eth_w3 = eth.Eth(w3)
# start miner for mining, coinbase, setEtherBase
miner_w3 = miner.Miner(w3)

'''
print(eth_w3.getBlock(1))
print(eth_w3.getBlock('latest'))
print(eth_w3.blockNumber)

print(admin_w3.peers)

print(eth_w3.coinbase)


miner_w3.setEtherBase(eth_w3.accounts[1])
print(eth_w3.coinbase)

print(len(personal_w3.listAccounts))
'''

# --------------- Start web3 with Smart Contract---------------------
# Instantiate and deploy contract
Registrar = eth_w3.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

# if not set miner address *(geth sets account[0] if account created )
#miner_w3.setEtherBase("0x7df9a875a174b3bc565e6424a0050ebc1b2d1d82")
print("Miner Address: {}".format(eth_w3.coinbase))

# unlock initial account in genesis.json
personal_w3.unlockAccount(w3.toChecksumAddress("0x4b4e4db940550756be6360923b36653965c9d551"), "12345")
#personal_w3.unlockAccount(w3.toChecksumAddress("0x1ca831f426d705baa9e60b47cc2b1bd5aa3c0313"), "123")

# set default account from genesis to transaction
#eth_w3.defaultAccount = eth_w3.accounts[1] <= not work with geth!!!



# --------------- Start MyToken Smart Contract ----------------------
# Instantiate and deploy contract
MyToken = eth_w3.contract(abi=contract_interface_MT['abi'], bytecode=contract_interface_MT['bin'])

# initial value for MyToken
token = 1000000000
tx_hash = MyToken.constructor(token).transact(
    {
        "from": eth_w3.accounts[0],
        "value": w3.toWei(0, 'wei'),
        "gas":  3000000
    }
)

# for control mining
print("MyToken Constructor: {}".format(eth_w3.getTransactionReceipt(tx_hash)))
miner_w3.start(8)
eth_w3.waitForTransactionReceipt(tx_hash)
miner_w3.stop()
print("MyToken Constructor: {}".format(eth_w3.getTransactionReceipt(tx_hash)))
# get block
tx_receipt = eth_w3.getTransactionReceipt(tx_hash)

# Create the contract instance with the newly-deployed address
mytoken = eth_w3.contract(
    address=tx_receipt.contractAddress,
    abi=contract_interface_MT['abi']
)

personal_w3.unlockAccount(eth_w3.accounts[22], "asd")

tx_hash = mytoken.functions.transfer(eth_w3.accounts[22], 1000).transact(
    {'from': eth_w3.accounts[0],
     'value': w3.toWei(0, 'wei'),
     'gas': 3000000}
)

# for control mining
print("MyToken Constructor: {}".format(eth_w3.getTransactionReceipt(tx_hash)))
miner_w3.start(8)
eth_w3.waitForTransactionReceipt(tx_hash)
miner_w3.stop()
print("MyToken Constructor: {}".format(eth_w3.getTransactionReceipt(tx_hash)))

# --------------- end MyToken ---------------------------------------------------------------

# add new account blockchain as a patient
name_personal = input("Enter Your User Name: ")
pass_personal = input("Enter Your New Pass: ")
new_addr = personal_w3.newAccount(pass_personal)

print("Account Number: {}".format(personal_w3.listAccounts))

# unlock personal account
personal_w3.unlockAccount(new_addr, pass_personal)

# add blockchain new personal with constructor
tx_hash = Registrar.constructor().transact(
    {
        "from": eth_w3.accounts[0],
        "value": w3.toWei(0, 'wei'),
        "gas": 1000000

    }
)


# for control mining
print("Registrar Constructor: {}".format(eth_w3.getTransactionReceipt(tx_hash)))
miner_w3.start(8)
eth_w3.waitForTransactionReceipt(tx_hash)
miner_w3.stop()
print("Registrar Constructor: {}".format(eth_w3.getTransactionReceipt(tx_hash)))
# get block
tx_receipt = eth_w3.getTransactionReceipt(tx_hash)


# Create the contract instance with the newly-deployed address
registry = eth_w3.contract(
    address=tx_receipt.contractAddress,
    abi=contract_interface['abi']
)

tx_hash = registry.functions.initialAccount(new_addr, name_personal.encode(), 100).transact(
    {'from': eth_w3.accounts[0],
     'value': w3.toWei(100, 'wei')}
)

# for control mining
print("Registrar Initial Account: {}".format(eth_w3.getTransactionReceipt(tx_hash)))
miner_w3.start(2)
eth_w3.waitForTransactionReceipt(tx_hash)
miner_w3.stop()
print("Registrar Initial Account: {}".format(eth_w3.getTransactionReceipt(tx_hash)))
# get block
tx_receipt_initial_RC = eth_w3.getTransactionReceipt(tx_hash)


# -------Summary Contract-----------

# Instantiate and deploy contract
Summary = eth_w3.contract(abi=contract_interface_SC['abi'], bytecode=contract_interface_SC['bin'])

# search patient address with username in RegistrarContract
username = name_personal    # input("Enter Your Username: ")
patient_address = registry.functions.getAddress(username.encode()).call()

tx_hash = Summary.constructor(patient_address).transact({'from': eth_w3.accounts[0]})
# for control mining
print("Summary Constructor: {}".format(eth_w3.getTransactionReceipt(tx_hash)))
miner_w3.start(2)
eth_w3.waitForTransactionReceipt(tx_hash)
miner_w3.stop()
print("Summary Constructor: {}".format(eth_w3.getTransactionReceipt(tx_hash)))
# get block
tx_receipt = eth_w3.getTransactionReceipt(tx_hash)

# Create the contract instance with the newly-deployed address
summary = eth_w3.contract(
    address=tx_receipt.contractAddress,
    abi=contract_interface_SC['abi'],
)

# send Registrar Contract Summary Contract Address (who send?****)
tx_hash = registry.functions.summaryContractReference(name_personal.encode(), summary.address).transact(
    {
        "from": eth_w3.accounts[0],
        "value": w3.toWei(0, "wei"),
        "gas": 3000000
    }
)
# for control mining
print("Send Summary Reference: {}".format(eth_w3.getTransactionReceipt(tx_hash)))
miner_w3.start(2)
eth_w3.waitForTransactionReceipt(tx_hash)
miner_w3.stop()
print("Send Summary Reference: {}".format(eth_w3.getTransactionReceipt(tx_hash)))
# get block
tx_receipt = eth_w3.getTransactionReceipt(tx_hash)

# ------- PPR Contract ----------

# Instantiate and deploy contract
Relationship = eth_w3.contract(abi=contract_interface_PPR['abi'], bytecode=contract_interface_PPR['bin'])

tx_hash = Relationship.constructor(patient_address).transact({'from': eth_w3.accounts[0]})
# for control mining
print("PPR Constructor: {}".format(eth_w3.getTransactionReceipt(tx_hash)))
miner_w3.start(2)
eth_w3.waitForTransactionReceipt(tx_hash)
miner_w3.stop()
print("PPR Constructor: {}".format(eth_w3.getTransactionReceipt(tx_hash)))
# get block
tx_receipt = eth_w3.getTransactionReceipt(tx_hash)

ppr = eth_w3.contract(
    address=tx_receipt.contractAddress,
    abi=contract_interface_PPR['abi'],
)

# send PPR address to summary contract
tx_hash = summary.functions.addPPRAddress(ppr.address, patient_address).transact({'from': eth_w3.accounts[0]})
# for control mining
print("Add PPR Address: {}".format(eth_w3.getTransactionReceipt(tx_hash)))
miner_w3.start(2)
eth_w3.waitForTransactionReceipt(tx_hash)
miner_w3.stop()
print("Add PPR Address: {}".format(eth_w3.getTransactionReceipt(tx_hash)))
# get block
tx_receipt = eth_w3.getTransactionReceipt(tx_hash)

# add ppr patient query miner address and query
access_info = "http://127.0.0.1:1234"
db_query = "select * from provider_db_table"
tx_hash = ppr.functions.addDatabaseInfo(patient_address, access_info, db_query).transact({'from': eth_w3.accounts[0]})
# for control mining
print("Add PPR Patient DB Query: {}".format(eth_w3.getTransactionReceipt(tx_hash)))
miner_w3.start(2)
eth_w3.waitForTransactionReceipt(tx_hash)
miner_w3.stop()
print("Add PPR Patient DB Query: {}".format(eth_w3.getTransactionReceipt(tx_hash)))
# get block
tx_receipt = eth_w3.getTransactionReceipt(tx_hash)

block_no = tx_receipt['blockNumber']
block = eth_w3.getBlock(block_no)
# example miner address to send smart contract
print("Miner Address: ", block['miner'])
miner_address = block['miner']
tx_hash = ppr.functions.addMinerAddress(patient_address, miner_address).transact({'from': eth_w3.accounts[0]})
# for control mining
print("Add PPR Miner Address: {}".format(eth_w3.getTransactionReceipt(tx_hash)))
miner_w3.start(2)
eth_w3.waitForTransactionReceipt(tx_hash)
miner_w3.stop()
print("Add PPR Miner Address: {}".format(eth_w3.getTransactionReceipt(tx_hash)))
# get block
tx_receipt = eth_w3.getTransactionReceipt(tx_hash)

miner_db_query = "select * from provider_db_table"
tx_hash = ppr.functions.addMiningBounty(miner_db_query, patient_address, miner_address).transact({'from': eth_w3.accounts[0]})
# for control mining
print("Add PPR Miner DB Query: {}".format(eth_w3.getTransactionReceipt(tx_hash)))
miner_w3.start(2)
eth_w3.waitForTransactionReceipt(tx_hash)
miner_w3.stop()
print("Add PPR Miner DB Query: {}".format(eth_w3.getTransactionReceipt(tx_hash)))
# get block
tx_receipt = eth_w3.getTransactionReceipt(tx_hash)

# emit event, patient enter system, draw flowchart ...

# show event log after successful recording
event_RegistrarContract = registry.events.LogAccountAdded().processReceipt(tx_receipt_initial_RC)
print(event_RegistrarContract)
print("Patient Name: {}".format(event_RegistrarContract[0]['args']['_username'].decode()))
print("Patient Address: {}".format(event_RegistrarContract[0]['args']['_patientAddress']))
