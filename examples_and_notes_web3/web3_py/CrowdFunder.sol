pragma solidity ^0.4.19;

contract CrowdFunder {
	
	address public creator;
	address public fundRecipient; // creator may be different than recipient
	uint public minimumToRaise; // required to tip, else everyone gets refund(geri ödeme / iade)
	string campaignUrl;
	byte constant version = 1;	
	
	// Fundraising(bağış) ,Raise(arttırmak), Fund(sermaye), Expire(süresi dolmak)
	enum State {
		Fundraising,
		ExpiredRefund,
		Successful
	}
	
	// Contribution(katkı, bağış, aidat)
	struct Contribution {
		uint amount;
		address contributor;
	}

	// State variables
	State public state = State.Fundraising;
	uint public totalRaised;
	uint public raiseBy;
	uint public completeAt;
	Contribution[] contributions;

    // access events from outside blockchain, events are notify external parties( web3.py or web3.js)
	event LogFundingReceived(address addr, uint amount, uint currentTotal);
	event LogWinnerPaid(address winnerAddress);

    // Modifiers validate inputs to functions such as minimal balance or user auth;
    // similar to guard clause in other languages
	modifier inState(State _state) {
		require(state == _state);
		_;
	}
	
	modifier isCreator() {
		require(msg.sender == creator);
		_;
	}
	
	modifier atEndOfLifecycle() {
		require(((state == State.ExpiredRefund || state == State.Successful) && completeAt + 24 weeks < now));
		_;
	}




	function CrowdFunder(uint timeInHoursForFundraising, string _campaingUrl, address _fundRecipient, uint _minimumRaise) public {
		creator = msg.sender;
		fundRecipient = _fundRecipient;
		campaignUrl = _campaingUrl;
		minimumToRaise = _minimumRaise;
		raiseBy = now + (timeInHoursForFundraising * 1 hours);
	}

	
	function contribute() public payable inState(State.Fundraising) returns(uint256 id) {
		contributions.push(Contribution({amount: msg.value, contributor:msg.sender}));
		totalRaised += msg.value;

		emit LogFundingReceived(msg.sender, msg.value, totalRaised);

		checkIfFundingCompleteOrExpired();
		return contributions.length - 1; //return id
	}

	function checkIfFundingCompleteOrExpired() public {
		if (totalRaised > minimumToRaise) {
			state = State.Successful;
			payOut();
		} 
		else if(now > raiseBy) { // could incentivize(teşvik etmek) sender who initiated state change here
			state = State.ExpiredRefund; // backers can now collect refunds by calling getRefund(id)
		}
		completeAt = now;
	}

	function payOut()
        public
        inState(State.Successful)
        {
       	 	fundRecipient.transfer(this.balance);
        	emit LogWinnerPaid(fundRecipient);
   	 }

  	function getRefund(uint256 id)
    inState(State.ExpiredRefund)
    public
    returns(bool)
    {
        require(contributions.length > id && id >= 0 && contributions[id].amount != 0 );

        uint256 amountToRefund = contributions[id].amount;
        contributions[id].amount = 0;

        contributions[id].contributor.transfer(amountToRefund);

        return true;
    }

    function removeContract()
    public
    isCreator()
    atEndOfLifecycle()
    {
        selfdestruct(msg.sender);
        // creator gets all money that hasn't be claimed
    }


}
