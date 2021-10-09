/*
    reference:
        1) https://www.ethereum.org/token
        2) https://github.com/ethereum/EIPs/blob/master/EIPS/eip-20.md
        3) https://theethereum.wiki/w/index.php/ERC20_Token_Standard

        for sample tokens:
         -- https://github.com/ConsenSys/Tokens/blob/master/contracts/eip20/EIP20.sol
         -- https://github.com/OpenZeppelin/openzeppelin-solidity/blob/master/contracts/token/ERC20/ERC20.sol
*/

pragma solidity ^0.5.2;

contract MyToken {

    // Public variables of the token
    string public name;
    string public symbol;
    uint8 public decimals = 18;   // 18 decimals is the strongly suggested default, avoid changing it
    uint256 public totalSupply;

    // This creates an array with all balances
    mapping (address => uint256) public balanceOf;
    //mapping (address => mapping (address => uint256)) public allowance;

    // This generates a public event on the blockchain that will notify clients
    event Transfer(address indexed _from, address indexed _to, uint256 _value);


    /* Initializes contract with initial supply tokens to the creator of the contract */
    constructor(uint256 initialSupply, string memory tokenName, string memory tokenSymbol) public {
        totalSupply = initialSupply * 10 ** uint256(18);
        balanceOf[msg.sender] = totalSupply;              // Give the creator all initial tokens
        name = tokenName;
        symbol = tokenSymbol;
    }


    /**
     * Internal transfer, only can be called by this contract
     */
    function _transfer(address _from, address _to, uint256 _value) internal {
        // Prevent transfer to 0x0 address. Use burn() instead
        require(_to != address(0x0));

        // Check if the sender has enough
        require(balanceOf[_from] >= _value);

        // Check for overflows
        require(balanceOf[_to] + _value > balanceOf[_to]);

        // Save this for an assertion in the future
        uint previousBalances = balanceOf[_from] + balanceOf[_to];

        // Subtract from the sender
        balanceOf[_from] -= _value;

        // Add the same to the recipient
        balanceOf[_to] += _value;

        emit Transfer(_from, _to, _value);
    }

    /**
     * Transfer tokens
     */
    function transfer(address payable _to, uint256 _value) public payable returns (bool success) {
        _to.transfer(msg.value);
        _transfer(msg.sender, _to, _value);
        return true;
    }

    function getBalanceOf(address _useraddr) public view returns(uint256) {
        return balanceOf[_useraddr];
    }




}
