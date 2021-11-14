import sqlite3 as sl
import hashlib
con = sl.connect('database.db',check_same_thread=False)


# with con:
con.execute("""CREATE TABLE IF NOT EXISTS users(name TEXT UNIQUE, pinHash TEXT ,secret TEXT);""")

def create_user(name:str, pin:str,secret:str):
    digest = hashlib.sha512(pin.encode()).hexdigest()
    try:
        con.execute("""INSERT INTO users VALUES(?,?,?);""", (name, digest,secret))
    except:
        print("user already exists")

def get_user(name: str, pin:str):
    digest = hashlib.sha512(pin.encode()).hexdigest()
    cur = con.execute("""SELECT * FROM users WHERE name=?;""", (name,))
    for row in cur:
        user_data = row
        print(user_data)
        break

    (name, pinHash, secret) = user_data
    if (pinHash == digest):
        return {
            "name": name,
            "secret": secret,
            "pinHash": pinHash
        }
    else:
        raise Exception("Wrong pin or user not found")


def update_secret(user,newSecret:str):
    con.execute("""UPDATE users SET secret=? WHERE name=?;""", (newSecret,user["name"]))
# create_user("Vaibhav", "166700","This is my secret")
# get_user("Vaibhav", "166700")
# get_user("Vaibhava", "166701")