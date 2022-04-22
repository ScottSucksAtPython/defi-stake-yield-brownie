// SPDX-License-Identifier: MIT
// ------------------------------ Documentation ------------------------------ //
// Module:  MockDAI.sol
// This smart contract will create 1 million Dapp Tokens and send them to the
// creator.
//
//
// Modification History
// 4-20-2022 SRK Project Created.

// -------------------------------- Tasks --------------------------------- //
/*
1. 
2. 
3. 
*/

// ------------------------------- Resources ------------------------------ //
pragma solidity ^0.8.0;
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

// -------------------------------- Contract------------------------------- //
contract MockDAI is ERC20 {
    // ---------------------------- Variables ----------------------------- //
    // ----------------------------- Mappings ----------------------------- //
    // ------------------------------ Events ------------------------------ //
    // ---------------------------- Contructor ---------------------------- //
    constructor() ERC20("Mock DAI", "DAI") {}
    // ---------------------------- Functions ----------------------------- //
}
