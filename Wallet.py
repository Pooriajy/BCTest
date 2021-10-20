import requests
import json

class Wallet:
    server = "http://127.0.0.1:8080/"
    def GetBalance(self,public,private):
        balance = requests.post(self.server+"wallet/getbalance/",data=str({'public':public,'private':private})).text
        return balance


wallet = Wallet()
wallet.GetBalance('pooria','pooria')