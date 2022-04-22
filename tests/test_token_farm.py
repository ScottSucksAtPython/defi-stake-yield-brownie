# ------------------------------ Documentation ------------------------------ #
# Module:  NAME.py
# DESCRIPTION
#
#
# Modification History
# DATE INITIAL UPDATE.

# -------------------------------- Tasks ----------------------------------- #

# ------------------------------- Resources -------------------------------- #
from brownie import network, exceptions
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    get_contract,
)
import pytest
from scripts.deploy import deploy_token_farm_and_dapp_token

# ------------------------------- Variables -------------------------------- #

# ------------------------------ Functions --------------------------------- #
def test_set_price_feed_contract():
    '''This function tests the setPriceFeedContract function in the TokenFarm contract. '''
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing.")
    account = get_account()
    non_owner = get_account(index=1)
    token_farm, dapp_token = deploy_token_farm_and_dapp_token()
    # Act
    price_feed_address = get_contract("eth_usd_price_feed")
    token_farm.setPriceFeedContract(
        dapp_token.address, price_feed_address, {"from": account}
    )
    # Assert
    print(
        f"DAPP Token Address Is:    {token_farm.tokenPriceFeedMapping(dapp_token.address)}\nExpected Address Feed Is: {get_contract('eth_usd_price_feed')}"
    )
    assert token_farm.tokenPriceFeedMapping(dapp_token.address) == get_contract(
        "eth_usd_price_feed"
    )
    with pytest.raises(exceptions.VirtualMachineError):
        token_farm.setPriceFeedContract(
            dapp_token.address, price_feed_address, {"from": non_owner}
        )

def test_issues_tokens():
    # Arrange
    # Act
    # Assert


# ----------------------------- Main Function ------------------------------ #
def main():
    pass
