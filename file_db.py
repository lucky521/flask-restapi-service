import gridfs
import pymongo
import hashlib

dbclient = pymongo.MongoClient("localhost", 27017)
db = dbclient.test
#fs = gridfs.GridFS(db)
#fsb = gridfs.GridFSBucket(db)


def get_file(fid):

    return "get_file OK"

def put_file(filepointer):
    filehash = hashlib.md5()
    filehash.update(filepointer.read())
    hash_id = filehash.hexdigest()
    filepointer.save("./db/temp_name.file")
    file_id = "XXX"


    return hash_id

def del_file(fid):

    return "del_file OK"
