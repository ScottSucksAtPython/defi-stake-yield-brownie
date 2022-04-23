# ------------------------------ Documentation ------------------------------ #
# Module:  conftest.py
# DESCRIPTION
#
#
# Modification History
# 04-22-2022 SRK Project Created.

# -------------------------------- Tasks ----------------------------------- #

# ------------------------------- Resources -------------------------------- #
import pytest
from web3 import Web3
from scripts.helpful_scripts import get_account
from brownie import MockERC20

# ------------------------------- Variables -------------------------------- #

# ------------------------------ Functions --------------------------------- #
@pytest.fixture
def amount_staked():
    return Web3.toWei(1, "ether")


@pytest.fixture
def random_erc20():
    account = get_account()
    erc20 = MockERC20.deploy({"from": account})
    return erc20


# ----------------------------- Main Function ------------------------------ #
