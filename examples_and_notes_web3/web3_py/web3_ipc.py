import requests


import web3.testing as asd


from web3 import Web3, HTTPProvider, IPCProvider



#web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3 = Web3(IPCProvider("/home/akif/.ethereum/rinkeby/geth.ipc"))


print(w3.isConnected())


print(w3.eth.blockNumber)



