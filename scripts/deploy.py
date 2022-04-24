# ------------------------------ Documentation ------------------------------ #
# Module:  deploy.py
# will deploy the TokenFarm and DappToken contracts.
#
#
# Modification History
# 04-20-2022 SRK Project Created.
# 04-22-2022 SRK Documentation Updated.
# 04-24-2022 SRK Added update_frontend function.

# -------------------------------- Tasks ----------------------------------- #

# ------------------------------- Resources -------------------------------- #
from turtle import update
from scripts.helpful_scripts import (
    get_account,
    get_contract,
    deploy_mocks,
    fund_with_link,
)
from brownie import config, network, DappToken, TokenFarm
from web3 import Web3
import yaml, json, os, shutil

# ------------------------------- Variables -------------------------------- #
KEPT_BALANCE = Web3.toWei(100, "ether")

# ------------------------------ Functions --------------------------------- #
def deploy_token_farm_and_dapp_token(update_front_end=False):
    """
    This function deploys the TokenFarm, DappToken and other associated
    contracts to the blockchain. Dapp tokens are transferred into the Token
    Farm contract. Dapp, Weth and Fau tokens are added to the list of tokens
    which can be staked to the Token Farm.

    Arguments:
        update_front_end (bool) - Set as true if you want the frontend files to be
        updated during deployment.

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
    if update_front_end:
        update_frontend()
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


def update_frontend():
    copy_folders_to_front_end("./build", "./front_end/src/chain-info")
    with open("brownie-config.yaml", "r") as brownie_config:
        config_dict = yaml.load(brownie_config, Loader=yaml.FullLoader)
    with open("./front_end/src/brownie-config.json", "w") as brownie_config_json:
        json.dump(config_dict, brownie_config_json)
    print("Frontend Updated!")


def copy_folders_to_front_end(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    shutil.copytree(source, destination)


# ----------------------------- Main Function ------------------------------ #
def main():
    """
    This function will be automatically excecuted by brownie when this script is run.
    """
    deploy_token_farm_and_dapp_token(update_front_end=True)
