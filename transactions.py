import datetime
import hashlib
import random
import sqlite3
import string


difficulty = 4

class Transaction:
    def generate(self,Value,Sender,Receiver):
        conn = sqlite3.connect("bc.db", check_same_thread=False)
        print("generating transaction")
        cur = conn.cursor()
        q = "insert into transactions(hash_id,value,sender,receiver,age,pow,diff) values "

        last_hash = cur.execute("select hash_id from transactions order by rowid desc limit 1;").fetchone()
        proof = ''.join(random.choices(string.ascii_uppercase + string.digits, k=difficulty))
        pow = hashlib.sha256((str(last_hash[0])+str(proof)).encode()).hexdigest()
        hash_id = pow
        value = Value
        age = datetime.datetime.now()
        q1 = "('{0}','{1}','{2}','{3}','{4}','{5}','{6}');".format(hash_id, value, Sender, Receiver, age, "not_proved",
                                                                   difficulty)
        q = q + q1
        cur.execute(q)
        conn.commit()
        conn.close()
        return 1
    def reward(self,Value,Sender,Receiver):
        conn = sqlite3.connect("bc.db", check_same_thread=False)
        print("giving reward")
        cur = conn.cursor()
        q = "insert into transactions(hash_id,value,sender,receiver,age,pow,diff) values "
        last_hash = cur.execute("select hash_id from transactions order by rowid desc limit 1;").fetchone()
        proof = ''.join(random.choices(string.ascii_uppercase + string.digits, k=difficulty))
        hash_id = hashlib.sha256((str(last_hash[0])+str(proof)).encode()).hexdigest()
        value = Value
        age = datetime.datetime.now()
        q1 = "('{0}','{1}','{2}','{3}','{4}','{5}','{6}');".format(hash_id, value, Sender, Receiver, age, proof,
                                                                   difficulty)
        q = q + q1
        cur.execute(q)
        conn.commit()
        conn.close()
        return 1

    def validateNetwork(self, hp):
        for i in range(len(hp) -1 ):
            hashid = ''
            pow = ''
            try:
                hashid = hp[i + 1][0]
                pow = hp[i + 2][1]
            except:
                pass
            confirmation = hashlib.sha256(str(hashid).encode() + str(pow).encode()).hexdigest()
            try:
                if confirmation != hp[i + 2][0]:
                    print("Error at block: ", hp[i + 2][0])
                    break
                else:
                    print("Block ", hashid, " Validated")
            except:
                pass


class Wallet:
    def create(self):
        conn = sqlite3.connect("bc.db", check_same_thread=False)
        cur = conn.cursor()
        acc_no = random.randint(2,20000000)
        public = ''.join(random.choices(string.ascii_uppercase + string.digits, k=24))
        private = ''.join(random.choices(string.ascii_uppercase + string.digits, k=63))
        cur.execute("insert into wallets(public , private, balance) values ('{0}','{1}',0)".format(public,private))
        conn.commit()
        conn.close()
        return {'public':public, 'private':private}


#[generate a transaction]
# A = Transaction()
# A.generate(1,"mamad","pooria")
# #
# # B = Wallet()
# # print(B.create())

# while(True):
#     x = input("Generate transaction[1] or Validate network[2]? ")
#     if x == "1":
#         value = input("Enter Value: ")
#         sender = "Genesis"
#         receiver = input("Enter Receiver: ")
#         A.generate(value,sender,receiver)
#     elif x=="2":
#         conn = sqlite3.connect("bc.db", check_same_thread=False)
#         cur = conn.cursor()
#         cur.execute("select hash_id,pow from transactions")
#         network = cur.fetchall()
#         A.validateNetwork(network)

# for i in range(15):
# #     A.generate(38,"Genesis","pooria")
