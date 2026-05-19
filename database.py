from pymongo import MongoClient
from configs import cfg

client = MongoClient(cfg.MONGO_URI)

users = client['main']['users']
groups = client['main']['groups']

def already_db(user_id):
        user = users.find_one({"user_id" : str(user_id)})
        if not user:
            return False
        return True

def already_dbg(chat_id):
        group = groups.find_one({"chat_id" : str(chat_id)})
        if not group:
            return False
        return True

def add_user(user_id):
    in_db = already_db(user_id)
    if in_db:
        return
    return users.insert_one({"user_id": str(user_id)}) 

def remove_user(user_id):
    in_db = already_db(user_id)
    if not in_db:
        return 
    return users.delete_one({"user_id": str(user_id)})
    
def add_group(chat_id, title=None, username=None, invite_link=None, chat_type=None):
    update_fields = {"chat_id": str(chat_id)}
    if title is not None:
        update_fields["title"] = title
    if username is not None:
        update_fields["username"] = username
    if invite_link is not None:
        update_fields["invite_link"] = invite_link
    if chat_type is not None:
        update_fields["chat_type"] = chat_type
        
    return groups.update_one(
        {"chat_id": str(chat_id)},
        {"$set": update_fields},
        upsert=True
    )

def all_users():
    user = users.find({})
    usrs = len(list(user))
    return usrs

def all_groups():
    group = groups.find({})
    grps = len(list(group))
    return grps

def get_all_groups_details():
    return list(groups.find({}))


sudoers = client['main']['sudoers']

def add_sudo(user_id):
    sudoers.update_one({"user_id": int(user_id)}, {"$set": {"user_id": int(user_id)}}, upsert=True)

def remove_sudo(user_id):
    sudoers.delete_one({"user_id": int(user_id)})

def get_sudolist():
    return [doc["user_id"] for doc in sudoers.find()]

