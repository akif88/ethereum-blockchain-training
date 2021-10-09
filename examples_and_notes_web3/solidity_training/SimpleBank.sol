pragma solidity ^0.4.19;


// First, a simple Bank contract
// Allows deposits, withdrawals, and balance checks
contract SimpleBank {

	// dictionary(hash table) that maps addresses to balances.
	// "private" means that other contracts can't directly query balances
    // but data is still viewable to other parties on blockchain.
	mapping (address => uint) private balances;
	
	// 'public' makes externally readable (not writeable) by users or contracts
	address public owner;
	
	// Events - publicize actions to external listeners
	event LogDepositeMade(address accountAddress, uint amount);

	// Constructor, can receive one or many variables here; only one allowed
	function SimpleBank() public {
		// msg provides details about the message that's sent to the contract
        // msg.sender is contract caller (address of contract creator)
		owner = msg.sender;
	}


	/// @notice Deposit ether into bank
    /// @return The balance of the user after the deposit is made
	function deposit() public payable returns (uint) {
		// Use 'require' to test user inputs, 'assert' for internal invariants
        // Here we are making sure that there isn't an overflow issue
		require( (balances[msg.sender] + msg.value) >= balances[msg.sender]); 

		// all values set to data type's initial value by default
		balances[msg.sender] += msg.value;
		
		// fire event
		LogDepositeMade(msg.sender, msg.value);

		return balances[msg.sender];
	}

	
	/// @notice Withdraw ether from bank
    /// @dev This does not return any excess(fazlalık) ether sent to it
    /// @param withdrawAmount amount you want to withdraw
    /// @return The balance remaining for the user
	function withdraw(uint withdrawAmount) public returns (uint remainingBal) {
		require(withdrawAmount <= balances[msg.semder]);
		
		// Note the way we deduct the balance right away, before sending
        // Every .transfer/.send from this contract can call an external function
        // This may allow the caller to request an amount greater
        // than their balance using a recursive call
        // Aim to commit state before calling external functions, including .transfer/.send
		balances[msg.sender] -= withdrawAmount;
		
		// this automatically throws on a failure, which means the updated balance is reverted
		msg.sender.transfer(withdrawAmount);

		return balances[msg.sender];
	}

	
	
	/// @notice Get balance
    /// @return The balance of the user
    // 'constant' prevents function from editing state variables;
    // allows function to run locally/off blockchain
	function balance() constant public returns (uint) {
		return balances[msg.sender];
	}	
	


}






















