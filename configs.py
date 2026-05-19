from os import path, getenv

class Config:
    API_ID = int(getenv("API_ID", "0112234"))
    API_HASH = getenv("API_HASH", "abcdefg")
    BOT_TOKEN = getenv("BOT_TOKEN", "1234567891:AdDfgFRFVVfDEhdhyjjvjjftSEW")
    FSUB = getenv("FSUB", "rs_bro")
    CHID = int(getenv("CHID", "-1000112234"))
    OWNER_ID = int(getenv("OWNER_ID", "1252750011"))
    SUDO = list(map(int, getenv("SUDO", "").split()))
    MONGO_URI = getenv("MONGO_URI", "")
    
cfg = Config()
