"""
?????
    https://medium.com/@jgm.orinoco/ethereum-smart-service-payment-with-tokens-60894a79f75c

    --- Yes, either sending tokens or approving another party to transfer tokens on your behalf requires you to create
    a transaction and costs Ether. *** At current Ethereum does not provide a way around this *** , although there are some
    proposals to allow for a third party to pay a transaction’s gas costs.
-------------------------------------??????????????--------------------------------------------------
    https://www.reddit.com/r/ethereum/comments/6pbhf2/do_i_need_gas_to_transfer_erc20_tokens/
    --- Do I need gas to transfer ERC20 tokens?
    --- You will need ETH for gas if in the future you want to transfer those ERC20 Tokens

?????
"""

from solc import compile_source
from web3 import Web3, HTTPProvider
from web3 import admin, personal, eth, miner


# https://web3py.readthedocs.io/en/stable/examples.html#interacting-with-an-erc20-contract

# read smart-contract
with open("MyToken.sol") as f:
    smart_contract = f.read()

# compile MyToken smart contract with solc
compiled_solidity= compile_source(smart_contract)
contract_interface = compiled_solidity['<stdin>:MyToken']

# used with geth
w3 = Web3(HTTPProvider("http://127.0.0.1:8545"))
print(w3.isConnected())

admin_w3 = admin.Admin(w3)
# start personal to create, list etc.
personal_w3 = personal.Personal(w3)
# start ethereum
eth_w3 = eth.Eth(w3)
# start miner for mining, coinbase, setEtherBase
miner_w3 = miner.Miner(w3)

# unlock initial account in genesis.json
personal_w3.unlockAccount(eth_w3.accounts[0], "12345")
personal_w3.unlockAccount(eth_w3.accounts[7], "asd")

# --------------- Start MyToken Smart Contract ----------------------
# Instantiate and deploy contract
MyToken = eth_w3.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

# initial value for MyToken. Also set token name and token symbol.
token = 1000
tx_hash = MyToken.constructor(token, "BBM", "BBM").transact(
    {
        "from": eth_w3.accounts[0],
        "value": w3.toWei(0, 'wei'),
        "gas":  3000000
    }
)

# Deploy Contract
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
    abi=contract_interface['abi']
)



# add new account blockchain as a patient
name_personal = input("Enter Your User Name: ")
pass_personal = input("Enter Your New Pass: ")
new_addr = personal_w3.newAccount(pass_personal)

print("Account Number: {}".format(personal_w3.listAccounts))

# unlock personal account
personal_w3.unlockAccount(new_addr, pass_personal)

"""
    #owner give certain amount mytoken(BBM) to new users
"""

personal_w3.unlockAccount(eth_w3.accounts[7], "asd")
tx_hash = mytoken.functions.transfer(eth_w3.accounts[7], 1).transact(
    {
        'from': eth_w3.accounts[0],    # other users can transfer, if they have eth (or wei) and MyToken(BBM)
        'value': w3.toWei(10, 'wei'),  # send eth or wei to other users is necessary for transaction
        'gas': 3000000,
    }
)

# for control mining
print("MyToken Transfer: {}".format(eth_w3.getTransactionReceipt(tx_hash)))
miner_w3.start(8)
eth_w3.waitForTransactionReceipt(tx_hash)
miner_w3.stop()
print("MyToken Transfer: {}\n".format(eth_w3.getTransactionReceipt(tx_hash)))
tx_receipt_transfer = eth_w3.getTransactionReceipt(tx_hash)


# show event Transfer in MyToken.sol
event_myToken_Transfer = mytoken.events.Transfer().processReceipt(tx_receipt_transfer)
print(event_myToken_Transfer)

print("\nSender: {}".format(event_myToken_Transfer[0]['args']['_from']))
print("Receiver: {}".format(event_myToken_Transfer[0]['args']['_to']))
print("Value: {} BBM".format(event_myToken_Transfer[0]['args']['_value']))

# get users amount of tokens
my_balance = mytoken.functions.getBalanceOf(eth_w3.accounts[7]).call()
print(my_balance)

