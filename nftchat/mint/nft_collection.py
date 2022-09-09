from thirdweb import ThirdwebSDK
from eth_account import Account
from web3 import Web3
from dotenv import load_dotenv
import os

load_dotenv()

PRIVATE_KEY = os.environ.get("PRIVATE_KEY")

#RPC_URL = "https://rpc-mumbai.maticvigil.com/"

#provider = Web3(Web3.HTTPProvider(RPC_URL))

signer = Account.from_key(PRIVATE_KEY)

sdk = ThirdwebSDK("mumbai",signer)

nft_collection = sdk.get_nft_collection("0xFF1362E47355FC3d21ba383E501474eB7c40BfC4")


 