import pprint, requests, json, os
import pandas as pd
import itertools


class PureAPI(object):
    def __init__(self):
        config = open('pure_config.json')
        self.apikey = json.load(config)['apikey']
        self.headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8','Accept': 'application/json'}
        config.close()


    def count_all(self,save='save'):
        baseurl='https://pennstate.pure.elsevier.com/ws/api/510/'
        endpoints = open('endpoints.json')
        self.endpoints = json.load(endpoints)['endpoints']
        self.countTotals = dict()
        for endpoint in self.endpoints:
            category = list(endpoint.keys())[0]
            url = baseurl+'/'+category+'?'+'apiKey='+self.apikey
            data = requests.get(url, headers=self.headers)
            if 'count' in data.json().keys():
                self.count = data.json()['count']
                self.countTotals[category]=self.count
            else:
                self.countTotals[category]=None
        if save=='save':
            with open('count_totals.json','w') as f:
                f.write(json.dumps(self.countTotals))
            f.close()
        return self.countTotals

    def download_all(self,save='save'):
        file = open('count_totals.json')
        endpoint_counts = json.load(file)
        file.close()
        baseurl='https://pennstate.pure.elsevier.com/ws/api/510/'
        endpoint_counts = {k:endpoint_counts[k] for k in endpoint_counts if endpoint_counts[k]}
        sorted_endpoints = [(k, endpoint_counts[k]) for k in sorted(endpoint_counts, key=endpoint_counts.get, reverse=False) ]
        print(sorted_endpoints)
        for endpoint,count in sorted_endpoints:
            #print(endpoint_counts[endpoint])
            if endpoint_counts[endpoint]:
                if endpoint:
                    if not os.path.exists('database'):
                        os.mkdir('database')
                    savedir = os.path.join('database',endpoint)
                    if not os.path.exists(savedir):
                        os.mkdir(savedir)
                    saveiter = 0
                    filesize = "1000"
                    url = baseurl + endpoint + '?' + 'apiKey=' + self.apikey+'&size='+filesize
                    result = {'navigationLink':[{'ref':'next','href':url}]}
                    while url:
                        savename = endpoint+"_"+str(saveiter).zfill(5)+".json"
                        print(savename,url)

                        data = requests.get(url, headers=self.headers)
                        with open(os.path.join(savedir,savename), 'w') as f:
                            f.write(json.dumps(data.json()['items']))
                        f.close()
                        if 'navigationLink' in data.json().keys():
                            #print(data.json()['navigationLink'])
                            if len(data.json()['navigationLink'])==1:
                                if saveiter==0:
                                    url = data.json()['navigationLink'][0]['href']
                                else:
                                    url = None
                            else:
                                url = data.json()['navigationLink'][1]['href']
                        else:
                            url=None
                        saveiter+=1
if __name__ == "__main__":
    total = PureAPI().count_all(save='save')
    print(total)
    PureAPI().download_all()