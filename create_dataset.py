import json
import random

!curl https://s3-us-west-2.amazonaws.com/pinafore-us-west-2/qanta-jmlr-datasets/qanta.train.2018.04.18.json > quanta.train.json
!curl https://s3-us-west-2.amazonaws.com/pinafore-us-west-2/qanta-jmlr-datasets/wikipedia/wiki_lookup.json > wiki_lookup.json

f = open('quanta.train.json')
data = json.load(f)['questions']
random.shuffle(data)

f = open('wiki_lookup.json')
wiki = json.load(f)
wiki = dict((k.lower(),v) for k,v in wiki.items())

wiki_psgs = {'data' : []}

for i in range(0, 500):
    title = data[i]['page'].lower()
    
    if title in wiki.keys():
        splitted_text = wiki[title]['text'].replace("\n", " ").split()
        for j in range(0, len(splitted_text), 200):
            wiki_psgs['data'].append(wiki[title].copy())
            wiki_psgs['data'][len(wiki_psgs['data']) - 1]['text'] = ' '.join(splitted_text[j:min(j+200, len(splitted_text))]) 

with open('quanta_psgs.json', 'w') as outfile:
    json.dump(wiki_psgs, outfile)
