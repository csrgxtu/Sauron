import unirest
import json

if (__name__=='__main__'):

    url =  'http://192.168.100.3:5000/deadurls?start=0&offset=4574&spider=6w'
    unirest.timeout(180)
    req = unirest.get(url, headers={"Accept":"application/json"})
    deadurls = [{'url':data['url'],'spider':data['spider']} for data in req.body['data']]
    print len(deadurls), deadurls[0:5], type(deadurls)

    deadurlsdict = {}
    deadurlsdict['urls'] = deadurls

    with open('./deadurls.json', 'wb') as f:
        json.dump(deadurlsdict,f)
    f.close()
    print 'Done!'

    #!< PUT deadurls to unvisitedurls
    # # {"urls": [{'url':'', 'spider':'6w'}, {}..{}]}
    # with open('./deadurls.json', 'rb') as f:
    #     deadurls = json.load(f)
    #
    # unirest.timeout(180)
    # resunvisitedurl = unirest.put(
    #                 "http://192.168.100.3:5000/unvisitedurls",
    #                 headers={ "Accept": "application/json", "Content-Type": "application/json" },
    #                 params=json.dumps(deadurls)
    #             )
