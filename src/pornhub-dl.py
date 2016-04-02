import sys, urllib2, argparse, os
from porn import PornHub
parser = argparse.ArgumentParser()
parser.add_argument('-u/-url', action='store', dest='url', help='Porn-Hub URL')
parser.add_argument('--version', action='version', version='version 1.0.1 an open book project (C) 2016')
results = parser.parse_args()

if not results.url:
    if not os.path.exists("%s\TBD_PH.list" %(os.getenv('APPDATA'))):    
        #must pass something to fetch first
        print("please Provide an URL to Fetch !!! ")
    else:
        #simple download porn from saved file list
        newPorn = PornHub()
        newPorn.__prepare__()
else:
    #simple download porn from link provided
    newPorn = PornHub()
    resp=urllib2.urlopen(str(results.url)).read()
    newPorn._fetch_CDN_(resp)
    newPorn.PH_extractor_(resp)
    del resp
    newPorn.__prepare__()