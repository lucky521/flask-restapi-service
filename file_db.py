import gridfs
import pymongo
import bson
import hashlib

dbclient = pymongo.MongoClient("localhost", 27017)
db = dbclient.test
#fs = gridfs.GridFS(db)
#fsb = gridfs.GridFSBucket(db)


def get_file(fid):
    
    f_out = file("./db/cache_file.jpg", "wb")
    find_data = db.posts.find_one({'_id':fid})
    if find_data:
        f_out.write(find_data['data'])
    else:
        print "no image_id exist!"
        f_out.close()
        return -1

    f_out.close()
    print "get file " + fid
    return 1


def put_file():
    f1 = file("./db/cache_file.jpg", "rb")
    filehash = hashlib.md5()
    filehash.update(f1.read())
    hash_id = filehash.hexdigest()
    f1.close()

    if db.posts.find_one({'_id':hash_id}):
        print "duplicate image id " + hash_id
        return hash_id + " is a duplicate image id."

    f1 = file("./db/cache_file.jpg", "rb")
    bson_data = bson.Binary(f1.read())
    db.posts.insert({ '_id': hash_id, 'data': bson_data})
    f1.close()

    return hash_id


def del_file(fid):

    return "del_file OK"
