// SPDX-License-Identifier: MIT

// ------------------------------ Documentation ------------------------------ //
// Module:  TokenFarm.sol
//
// This smart contract simulates yield farming by allowing users to store an
// amount of their own tokens and receive rewards based on the value of those
// tokens. This is only simulated because the contract does not do anything
// with the stored tokens and the owner of the farm chooses when rewards are
// distributed. Users are able to withdraw the stored tokens within this
// contract at any time.
//
//
// Modification History
// 04-20-2022 SRK Project Created and completed.
// 04-22-2022 SRK Documentation updated.

// -------------------------------- Tasks --------------------------------- //
// Completed!

// ------------------------------- Resources ------------------------------ //
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

// -------------------------------- Contract------------------------------- //
contract TokenFarm is Ownable {
    // ---------------------------- Variables ----------------------------- //
    // This array is initialized and will store a list of tokens which can be staked to the
    // Token Farm.
    address[] public allowedTokens;

    // This array is initiallized and will store a list of everyone (by wallet address) who has
    // coins currently staked in the Token Farm.
    address[] public stakers;

    // This variable is initialized and will represent the DappTokens.
    IERC20 public dappToken;

    // ----------------------------- Mappings ----------------------------- //

    // This mapping stores the amount of each token a user has stored within
    // the Token Farm.
    mapping(address => mapping(address => uint256)) public stakingBalance;

    // This mapping associates a user's wallet address with the number of
    // unique tokens they have stored inside the TokenFarm.
    mapping(address => uint256) public uniqueTokensStaked;

    // This mapping associates a token to the contract address where it's
    // price feed information can be found.
    mapping(address => address) public tokenPriceFeedMapping;

    // ------------------------------ Events ------------------------------ //

    // ---------------------------- Contructor ---------------------------- //
    // Upon contract deployment this constructor stores the contract address
    // of the DappToken contract to the dappToken variable. This address must
    // be passed to the contract during deployment.
    constructor(address _dappTokenAddress) {
        dappToken = IERC20(_dappTokenAddress);
    }

    // ---------------------------- Functions ----------------------------- //

    /** 
    This function allows users to stake tokens to the TokenFarm. It
    requires that the tokens be in the allowedTokens array and that the user 
    sends at least 1 token. Once the token's are transferred 
    updateUniqueTokensStaked() is called to check if the user needs to be 
    added to the stakers array.
    
    Arguments: 
        _amount (uint256) - amount of tokens to be transferred into the 
        contract.
        _token (address) - the token being sent to this contract.
    */
    function stakeTokens(uint256 _amount, address _token) public {
        require(_amount > 0, "Must take more than 0 tokens.");
        require(tokenIsAllowed(_token), "Token is currently not allowed.");
        IERC20(_token).transferFrom(msg.sender, address(this), _amount);
        updateUniqueTokensStaked(msg.sender, _token);
        stakingBalance[_token][msg.sender] =
            stakingBalance[_token][msg.sender] +
            _amount;
        if (uniqueTokensStaked[msg.sender] == 1) {
            stakers.push(msg.sender);
        }
    }

    /** 
    This function withdraws all of a user's specified tokens from the 
    Token Farm. It requires that the user has atleast 1 of that token stored 
    within the cotract. It then remove's all of that user's token from the 
    stakingBalance and subtracts 1 from the uniquedTokensStaked for that user.
    
    Arguments: 
        _token (address) - the token which the user wishes to withdraw from 
        the Token Farm.
    */
    function unstakeTokens(address _token) public {
        uint256 balance = stakingBalance[_token][msg.sender];
        require(balance > 0, "Staking balance cannot be zero.");
        IERC20(_token).transfer(msg.sender, balance);
        stakingBalance[_token][msg.sender] = 0;
        uniqueTokensStaked[msg.sender] -= 1;
    }

    /** 
    This function checks to see if a specific token is on the allowedTokens list.
    
    Arguments: 
        _token (address) - the token being checked.

    Returns:
        True - if token is on the list.
        False - if the token is not on the list.
    */
    function tokenIsAllowed(address _token) public view returns (bool) {
        for (
            uint256 allowedTokensIndex = 0;
            allowedTokensIndex < allowedTokens.length;
            allowedTokensIndex++
        ) {
            if (allowedTokens[allowedTokensIndex] == _token) {
                return true;
            }
        }
        return false;
    }

    /** 
    This function adds a specified token to the allowedTokens list.
    
    Arguments: 
        _token (address) - the token being sent to this contract.
    */
    function addAllowedToken(address _token) public onlyOwner {
        allowedTokens.push(_token);
    }

    /** 
    This function pays out Dapp Tokens to users based on the total value of 
    all their tokens.
    */
    function issueTokens() public onlyOwner {
        for (
            uint256 stakersIndex = 0;
            stakersIndex < stakers.length;
            stakersIndex++
        ) {
            address recipient = stakers[stakersIndex];
            uint256 userTotalValue = getUserTotalValue(recipient);
            dappToken.transfer(recipient, userTotalValue);
        }
    }

    /** 
    This function will check the stakingBalance to see if this user has any of
    _token currently staked in the Token Farm. If not then it will update the 
    uniqueTokensStaked list.
    
    Arguments:
        _user (address) - Wallet address of the user.
        _token (address) - The token which has been staked.
    */
    function updateUniqueTokensStaked(address _user, address _token) internal {
        if (stakingBalance[_token][_user] <= 0) {
            uniqueTokensStaked[_user] += 1;
        }
    }

    /** 
    This function returns the total value (in USD) a specific user has 
    currently staked in the Token Farm.
    
    Arguments: 
        _user (address) - Wallet address of the user.

    Returns:
        totalValue (uint256) - the total value (in USD) of the _user's staked 
        tokens.
    */
    function getUserTotalValue(address _user) public view returns (uint256) {
        uint256 totalValue = 0;
        require(uniqueTokensStaked[_user] > 0, "No tokens staked.");
        for (
            uint256 allowedTokensIndex = 0;
            allowedTokensIndex < allowedTokens.length;
            allowedTokensIndex++
        ) {
            totalValue =
                totalValue +
                getUserSingleTokenValue(
                    _user,
                    allowedTokens[allowedTokensIndex]
                );
        }
        return totalValue;
    }

    /** 
    This function returns the total value a user has of the specified token.
    
    Arguments: 
        _user (address) - the wallet address of the user.
        _token (address) - the token which is having it's value calculated.

    Returns:
        (uint256) - the total value of the _user's _tokens.
    */
    function getUserSingleTokenValue(address _user, address _token)
        public
        view
        returns (uint256)
    {
        if (uniqueTokensStaked[_user] <= 0) {
            return 0;
        }
        (uint256 price, uint256 decimals) = getTokenValue(_token);
        return ((stakingBalance[_token][_user] * price) / (10**decimals));
    }

    /** 
    This function returns the current value (in USD) of a specified token as 
    well as that token's decimals value.
    
    Arguments: 
        _token (address) - the wallet address of the token being checked.

    Returns:
        price (uint256) - the value of this token in USD.
        decimals (uint256) - the number of decimal places for this token.
    */
    function getTokenValue(address _token)
        public
        view
        returns (uint256, uint256)
    {
        // Need a priceFeedAddress for each token.
        address priceFeedAddress = tokenPriceFeedMapping[_token];
        AggregatorV3Interface priceFeed = AggregatorV3Interface(
            priceFeedAddress
        );
        (, int256 price, , , ) = priceFeed.latestRoundData();
        uint256 decimals = priceFeed.decimals();
        return (uint256(price), uint256(decimals));
    }

    /** 
    This function stores the contract address for the ChainLink PriceFeed of a
    specfic token in the tokenPriceFeedMapping. This is required for the 
    getTokenValue() function to work.
    
    Arguments: 
        _token (address) - the specific token.
        _priceFeed (address) - The contract address where the ChainLink Price 
        feed is located.
    */
    function setPriceFeedContract(address _token, address _priceFeed)
        public
        onlyOwner
    {
        tokenPriceFeedMapping[_token] = _priceFeed;
    }
}
