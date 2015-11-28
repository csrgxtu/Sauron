#-*- encoding:utf-8 -*-
from pymongo import MongoClient

if __name__=='__main__':

    client = MongoClient(host='192.168.100.3', port=27019)
    # database
    master = client.master
    # collection
    visited = master.visited
    data = master.data

    #用户总数
    #sumOfusers = visited.find({'spider':'Shaishufang'}).count()

    #藏书总数
    res = data.aggregate(
            [
                {
                    '$group':
                        {
                            '_id' : '$data.TotalBooks',
                            'uid' : {'$addToSet': '$data.UID'},
                            'isbn': {'$addToSet': '$data.ISBN'}
                        }
                },
                {
                    '$sort':
                        {
                            '_id' : 1
                        }
                }
            ]
        )

    userNullBooknum, userZeroBooknum, userNotZeronum = 0, 0, 0
    booksnum , isbnnum = 0, 0

    for d in res:
        bookid = d['_id']
        userid = d['uid']
        isbn = d['isbn']
        if (isbn != []):
            isbnnum += len(isbn)

        if (bookid==None):
            userNullBooknum += len(userid)
        elif (bookid==0):
            userZeroBooknum += len(userid)
        else:
            userNotZeronum += len(userid)
            booksnum += (bookid*len(userid))

    sumusers = userNullBooknum + userZeroBooknum + userNotZeronum

    print '用户总数           ', sumusers
    print '没有藏书字段的用户数 ', userNullBooknum
    print '0藏书的用户数       ', userZeroBooknum
    print '非0藏书的用户数     ', userNotZeronum
    print '藏书总数           ',  booksnum

    print '藏书总数/非0藏书用户数', 1.0*booksnum/userNotZeronum
    print '藏书总数/用户总数    ', 1.0*booksnum/sumusers

    print 'ISBN去重后总数      ', isbnnum
