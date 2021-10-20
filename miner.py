import hashlib
import itertools
import time
import requests
import json



## configs
difficulty = 4
server = "http://127.0.0.1:8080/"
genesis = requests.get(server+"getgenesis/").text
##########

class Mine:
    def mine(self, data):
        upper_a = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                   'U', 'V', 'W', 'X', 'Y', 'Z']
        num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        all = upper_a + num
        print("\n\n--------------------** MINING **--------------------")
        for r in range(int(data['difficulty']), int(data['difficulty']) + 1):
            for s in itertools.product(all, repeat=r):
                test_proof = ''.join(s)
                test_hash = hashlib.sha256(str(data['last_hash']).encode() + str(test_proof).encode()).hexdigest()
                if test_hash == data['hash_id']:
                    print("--** BLOCK **--")
                    print("----HashID: ", test_hash)
                    print("----Sender: ",data['sender'])
                    print("----Receiver: ",data['receiver'])
                    print("----Value: ",data['value'])
                    print("----Proof: ", test_proof)
                    return test_proof
            return "not_proved"

class Wallet:
    public = ""
    private = ""
    balance = None
    def Create(self):
        try:
            r = requests.get(server + "wallet/create/").text
            js = json.loads(r)
            self.public = js['public']
            self.private = js['private']
            self.GetBalance(self.public,self.private)
            return 1
        except Exception as e:
            raise e


    def GetBalance(self,public,private):
        r = requests.post(server+"wallet/getbalance/",data=str({'public': self.public,'private':self.private})).text
        self.balance = int(r)
        return r


while(True):
    r = requests.get(server+"getblock/").text.replace("'",'"')
    wallet = Wallet()
    wallet.public = "pooria"
    wallet.private = "pooria"
    # wallet.GetBalance()
    if r == "{}":
        print("No Blocks Found.")
        time.sleep(5)
    else:
        data = json.loads(r)
        miner = Mine()
        a = miner.mine(data)
        if a != "not_proved":
            post_data = {'wallet':wallet.public,'hash_id': data['hash_id'], 'last_hash': data['last_hash'], 'proof': a}
            requests.post(server + "sendproof/", data=str(post_data))
