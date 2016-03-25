import pymongo
from urlnorm import urlnorm

db_client = pymongo.MongoClient()
db = db_client['alipi']

posts = db['post']

print "Total posts: %s" % str(posts.count())

for i in posts.find():
    print 'Post:: %s' % str(i['_id'])
    if not i['about']:
        print "No URL. Skipping.."
        continue

    print "Not normalized URL: %s" % i['about']
    print "Normalized URL: %s" % urlnorm(i['about'])
    #print "..Updating about field.."
    #posts.update({'_id': i['_id']}, {'$set': {'about': urlnorm(i['about'])}})
