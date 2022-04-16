import uuid

def generateUUID():
    uid = str(uuid.uuid1()).replace('-','')
    return uid