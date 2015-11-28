import unirest
import json
import csv

def unvisitedUrlF(filetxt):
    unvisitedUrl = []
    isbnset = set()
    with open(filetxt, 'rb') as fi:
        rows = fi.readlines()
        #print len(rows), rows[0]
        for line in rows:
            row = line.split(',')
            isbn = row[0]
            # d = {}
            # d['spider'] = '6w'
            # d['url'] = 'http://book.douban.com/isbn/' + isbn + '/'
            # unvisitedUrl.append(d)
            isbnset.add(isbn)
    fi.close()
    return list(isbnset)
    # unvisitedUrldict = {}
    # unvisitedUrldict['urls'] = unvisitedUrl
    # return unvisitedUrldict


def dataUrlF(filecsv):
    dataurls = []
    isbnset = set()

    with open(filecsv, 'rb') as fi:
        reader = csv.reader(fi)
        i = 0
        cnt = 0
        for line in reader:
            if (i != 0) and (line != []):
                # d = {}
                # d['spider'] = '6w'
                # d['url'] = 'http://book.douban.com/isbn/' + line[0] + '/'
                # dataurls.append(d)
                isbnset.add(line[0])
            else:
                cnt += 1
                pass
            i = 1
        print cnt
    fi.close()
    return list(isbnset)
    # dataurlsdict = {}
    # dataurlsdict['urls'] = dataurls
    # return dataurlsdict

if (__name__=='__main__'):
    # 1. !< All unvisitedurls 65499 Done!!! --> 62792
    unvisitedISBN = unvisitedUrlF('./stdkaijuan.txt')

    # 2. !< All deadurls (duplicate)        --> 58164
    #{"urls": [{'url':'', 'spider':'6w'}, {}..{}]}
    with open('./deadurls.json', 'rb') as f2:
        deadurlsdict = json.load(f2)
    f2.close()
    deadurls = deadurlsdict['urls']
    deadisbn = [d['url'][d['url'].find('isbn/')+5:-1] for d in deadurls]
    deadISBN = list(set(deadisbn))

    # 3. !< All dataurls59075               --> 4449
    # mongoexport --host=192.168.100.3 --port=27019 --db=master --collection=data --query='{"spider":"6w"}' --fields="data.ISBN" --type=csv --out=dataISBN.csv
    dataISBN = dataUrlF('./dataISBN.csv')

    # 4. !< Gain UpdateUnvisitedUrls.json   --> 62613
    usedISBN = deadISBN + dataISBN
    #print unvisitedISBN[0], usedISBN[0], dataISBN[0], deadISBN[0]
    #print len(unvisitedISBN),  len(usedISBN), len(dataISBN),  len(deadISBN)
    #print len(unvisitedISBN) - len(usedISBN)   # --> 179

    unvisitedlist = [d for d in unvisitedISBN if (d not in usedISBN)]
    with open('./unvisitedlist.json', 'wb') as f4:
        json.dump(unvisitedlist,f4)
    f4.close()
    #print len(unvisitedlist), unvisitedlist[0] # --> 213

    #!< for amazon spider
    amazonISBN = unvisitedlist + deadISBN
    amazondlist = []
    #deadISBN include "://book.douban.com/subject/6963723" like string.
    for isbn in amazonISBN:
        if ('subject' not in isbn):
            amazondlist.append(isbn)
        else:
            pass
    with open('./amazonISBN.json', 'wb') as fa:
        json.dump(amazondlist, fa)
    fa.close()
    print len(amazondlist), amazondlist[0]       # --> 4632

    # 5. !< UpdateUnvisitedUrls.json
    # with open('./unvisitedlist.json', 'rb') as f5:
    #     uvlist = json.load(f5)
    # f5.close()
    # print len(uvlist), uvlist[0]
    #
    # dlist = []
    # for isbn in uvlist:
    #     d = {}
    #     d['spider'] = '6w'
    #     d['url'] = 'http://book.douban.com/isbn/' + isbn + '/'
    #     dlist.append(d)

    # uvdict = {}
    # uvdict['urls'] = dlist
    #
    # unirest.timeout(180)
    # resunvisitedurl = unirest.put(
    #                 "http://192.168.100.3:5000/unvisitedurls",
    #                 headers={ "Accept": "application/json", "Content-Type": "application/json" },
    #                 params=json.dumps(uvdict)
    #             )
