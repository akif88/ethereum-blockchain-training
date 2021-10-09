pragma solidity ^0.4.0;

contract SimpleStorage{
	uint storedData;
	// uint => unsigned int of 256 bits
	// storedData => state variable

	function set(uint x) public {
		storedData = x;
	}

	function get() public view returns (uint) {
		return storedData;
	}

}
