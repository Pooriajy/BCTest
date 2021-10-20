import json
import hashlib
import web
import sqlite3
import random
import string
import transactions
conn = sqlite3.connect("bc.db", check_same_thread=False)
cur = conn.cursor()

genesis = "ba4aee24882ece1eec6b1b4bf9ee8b63"
reward = 6
urls = (
    '/', 'hello',
    '/getblock/','GetBlock',
    '/wallet/getbalance','GetBalance',
    '/getgenesis/','GetGenesis',
    '/sendproof/','SendProof',
    '/getnetworkvalidation/','GetNetworkValidation',
    '/wallet/create/', 'CreateWallet',
)
app = web.application(urls, globals())


class hello:
    def GET(self):
        return "<h1>Hello"


class GetNetworkValidation:
    def GET(self):
        cur.execute("select hash_id,pow from transactions")
        network = cur.fetchall()
        js = {'network':network}
        return js


class SendProof:
    def POST(self):
        t = transactions.Transaction()
        data = web.data()
        data = str(data.decode("utf-8")).replace("'",'"')
        print(data)
        js = json.loads(data)
        testing = hashlib.sha256(str(js['last_hash']).encode() + str(js['proof']).encode()).hexdigest()
        if testing == js['hash_id']:
            cur.execute("update transactions set pow='{0}' where hash_id='{1}'".format(js['proof'],js['hash_id']))
            conn.commit()
            t.reward(reward,"Genesis",js['wallet'])
            cur.execute("update wallets set balance=balance+{0} where public='{1}'".format(reward,js['wallet']))
            conn.commit()
        raise web.seeother("/")


class GetBalance:
    def POST(self):
        data= web.data()
        data = str(data.decode("utf-8")).replace("'",'"')
        print(data)
        js = json.loads(data)
        public = js['public']
        private = js['private']
        query = "select balance from wallets where public='{0}' and private='{1}'".format(public,private)
        balance = cur.execute(query).fetchone()
        return balance[0]


class GetGenesis:
    def GET(self):
        return "ba4aee24882ece1eec6b1b4bf9ee8b63"


class GetBlock:
    def GET(self):
        hash_id = cur.execute(
            "select hash_id,diff,sender,receiver,value,age from transactions where pow='not_proved' order by rowid asc limit 1;").fetchall()

        last_hash = ''
        try:
            rowid = cur.execute(
                "select rowid from transactions where pow='not_proved' order by rowid asc limit 1").fetchall()[
                0][0]
            if rowid == 1:
                return "{}"
            last_hash = cur.execute("select hash_id from transactions where rowid = {0}".format(rowid - 1)).fetchone()[
                0]
        except Exception as e:
            print(e)
            return "{}"
        if hash_id == genesis:
            print("All Blocks Are Mined.")
            return "{}"
        query = {'hash_id':hash_id[0][0],'difficulty':hash_id[0][1],'sender':hash_id[0][2],'receiver':hash_id[0][3],'value':hash_id[0][4],
                'age':hash_id[0][5], 'last_hash':last_hash}
        return query

class CreateWallet:
    def GET(self):
        acc_no = random.randint(2, 20000000)
        public = ''.join(random.choices(string.ascii_uppercase + string.digits, k=24))
        private = ''.join(random.choices(string.ascii_uppercase + string.digits, k=63))
        cur.execute("insert into wallets(public , private, balance) values ('{0}','{1}',0)".format(public, private))
        conn.commit()
        conn.close()
        return {'public': public, 'private': private}



if __name__ == "__main__":
    app.run()