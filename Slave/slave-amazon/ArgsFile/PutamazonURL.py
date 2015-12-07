import unirest
import json

if (__name__=='__main__'):

    #!< amazonURL.json
    with open('./amazonURL.json', 'rb') as f5:
        uvdict = json.load(f5)
    f5.close()

    uvlist = uvdict['urls']
    print len(uvlist), uvlist[0]

    unirest.timeout(180)
    resunvisitedurl = unirest.put(
                    "http://192.168.100.3:5000/unvisitedurls",
                    headers={ "Accept": "application/json", "Content-Type": "application/json" },
                    params=json.dumps(uvdict)
                )
