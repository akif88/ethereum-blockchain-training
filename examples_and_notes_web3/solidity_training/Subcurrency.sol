pragma solidity ^0.4.21;

contract Coin {
	
	// address ==> It is suitable for storing addresses of contracts 
	// or keypairs belonging to external persons. 
	
	// public ==> The keyword public automatically generates a function that allows 
	// you to access the current value of the state variable from outside of the contract. 
	// minter ==> state variable (minter: para basan kişi)
	
	// mapping ==> Mappings can be seen as "hash tables" which are virtually initialized 
	// such that every possible key exists and is mapped to a value whose byte-representation is all zeros. 
	
	address public minter;
	mapping (address => uint) public balances;

	// event ==> the listener will also receive the arguments from, to and amount, 
	// which makes it easy to track transactions.
	event Sent(address from, address to, uint amount);

	
	// This is the constructor whose code is
    // run only when the contract is created.
	function Coin() public {
		// msg ==> It permanently stores the address of the person creating the contract: 
		// msg (together with tx and block) is a magic global variable that contains some properties 
		// which allow access to the blockchain. msg.sender is always the address 
		// where the current (external) function call came from.
		minter = msg.sender;
	}

	// (mint: para basmak)
	function mint(address receiver, uint amount) public {
		if (msg.sender != minter) return;
		balances[receiver] += amount;
	}

	function send(address receiver, uint amount) public	{
		if (balances[msg.sender] < amount) return;
		balances[msg.sender] -= amount;
		balances[receiver] += amount;
		emit Sent(msg.sender, receiver, amount);
	}

}
