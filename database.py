from pymongo import MongoClient
from configs import cfg

client = MongoClient(cfg.MONGO_URI)

users = client['main']['users']
groups = client['main']['groups']

def already_db(user_id):
        user = users.find_one({"user_id" : str(user_id)})
        return bool(user)

def already_dbg(chat_id):
        group = groups.find_one({"chat_id" : str(chat_id)})
        return bool(group)

def add_user(user_id):
        if in_db := already_db(user_id):
                return
        return users.insert_one({"user_id": str(user_id)}) 

def remove_user(user_id):
        if in_db := already_db(user_id):
                return users.delete_one({"user_id": str(user_id)})
        else:
                return
    
def add_group(chat_id):
        if in_db := already_dbg(chat_id):
                return
        return groups.insert_one({"chat_id": str(chat_id)})

def all_users():
        user = users.find({})
        return len(list(user))

def all_groups():
        group = groups.find({})
        return len(list(group))
