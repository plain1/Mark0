import requests
from bs4 import BeautifulSoup



def nft_data():
    req = requests.get('https://thirdweb.com/mumbai/0xFF1362E47355FC3d21ba383E501474eB7c40BfC4/events')
    html = req.text
    soup = BeautifulSoup(html,'html.parser')








