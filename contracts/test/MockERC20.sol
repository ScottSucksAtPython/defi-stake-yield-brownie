// SPDX-License-Identifier: MIT
// ------------------------------ Documentation ------------------------------ //
// Module:  MockERC20.sol
// A Mock Token used for testing.
//
//
// Modification History
// 04-22-2022 SRK Contract Created.

// -------------------------------- Tasks --------------------------------- //

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

// ------------------------------- Resources ------------------------------ //
pragma solidity ^0.8.0;

// -------------------------------- Contract------------------------------- //
contract MockERC20 is ERC20 {
    constructor() ERC20("Mock ERC20", "mERC") {
        _mint(msg.sender, 1000000000000000000000);
    }
    // ---------------------------- Variables ----------------------------- //

    // ----------------------------- Mappings ----------------------------- //

    // ------------------------------ Events ------------------------------ //

    // ---------------------------- Contructor ---------------------------- //

    // ---------------------------- Functions ----------------------------- //
}
