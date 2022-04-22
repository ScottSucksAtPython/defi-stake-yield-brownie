# ------------------------------ Documentation ------------------------------ #
# Module:  deploy.py
# will deploy the TokenFarm and DappToken contracts.
#
#
# Modification History
# 04-20-2022 SRK Project Created.
# 04-22-2022 SRK Documentation Updated.

# -------------------------------- Tasks ----------------------------------- #

# ------------------------------- Resources -------------------------------- #
from scripts.helpful_scripts import (
    get_account,
    get_contract,
    deploy_mocks,
    fund_with_link,
)
from brownie import config, network, DappToken, TokenFarm
from web3 import Web3

# ------------------------------- Variables -------------------------------- #
KEPT_BALANCE = Web3.toWei(100, "ether")

# ------------------------------ Functions --------------------------------- #
def deploy_token_farm_and_dapp_token():
    """
    This function deploys the TokenFarm, DappToken and other associated
    contracts to the blockchain. Dapp tokens are transferred into the Token
    Farm contract. Dapp, Weth and Fau tokens are added to the list of tokens
    which can be staked to the Token Farm.

    Returns:
        token_farm - The Token Farm contract object.
        dapp_token - The Dapp Token contract object.
    """
    account = get_account()
    dapp_token = DappToken.deploy({"from": account})
    token_farm = TokenFarm.deploy(
        dapp_token.address,
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    tx = dapp_token.transfer(
        token_farm.address, dapp_token.totalSupply() - KEPT_BALANCE, {"from": account}
    )
    tx.wait(1)
    weth_token = get_contract("weth_token")
    fau_token = get_contract("fau_token")
    dict_of_allowed_tokens = {
        dapp_token: get_contract("dai_usd_price_feed"),
        fau_token: get_contract("dai_usd_price_feed"),
        weth_token: get_contract("eth_usd_price_feed"),
    }
    add_allowed_tokens(token_farm, dict_of_allowed_tokens, account)
    return token_farm, dapp_token


def add_allowed_tokens(token_farm, dict_of_allowed_tokens, account):
    """
    This function adds tokens to the Token Farm's allowedTokens list.

    Arguments:
        token_farm - address of the deployed Token Farm contract.
        dict_of_allowed_tokens - addresses of a token's price feed keyed to the address of that token's contract.
        account - the account of the user interacting with the Token Farm contact.

    Returns:
        token_farm - The object for the TokenFarm contract.
    """
    for token in dict_of_allowed_tokens:
        add_tx = token_farm.addAllowedToken(token.address, {"from": account})
        add_tx.wait(1)
        set_tx = token_farm.setPriceFeedContract(
            token.address, dict_of_allowed_tokens[token], {"from": account}
        )
        set_tx.wait(1)
    return token_farm


# ----------------------------- Main Function ------------------------------ #
def main():
    """
    This function will be automatically excecuted by brownie when this script is run.
    """
    deploy_token_farm_and_dapp_token()
