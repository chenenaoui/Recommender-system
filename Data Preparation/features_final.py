from pymongo import MongoClient
import json
import pickle
import numpy as np
import os
import re 
from collections import Counter

client = MongoClient()
db = client.get_database('pi')
coll = db.get_collection('data')
data = list(coll.find())

#************************************************************************
scrapped = []
for file_path in list(filter(lambda x: "scrapping" in x, os.listdir())):
    with open(file_path, 'r') as file:
        for item in json.load(file):
            scrapped.append(item)

#treating companies :
with open('all_companies.pckl', 'rb') as file :
    comp = pickle.load(file)


def get_followers(company): 
    result = re.findall(r'\d+',company['foll'].replace('\u202f','')) 
    if result ==[]:
        return 0
    return int(result[-1]) 

def get_emp(company):
    res = company['info'].split('\n') 
    try : 
        return int(re.findall(r'\d+', re.sub(r'\s+','', res[res.index('Taille de l’entreprise')+1] ))[-1]) 
    except : 
        return 0         

def get_lkd_emp(company):
    res = company['info'].split('\n') 
    try : 
        return int(re.findall(r'\d+', re.sub(r'\s+','', res[res.index('Taille de l’entreprise')+2] ))[-1]) 
    except : 
        return 0         

def get_type(company):
    res = company['info'].split('\n') 
    try : 
        return res[res.index('Type')+1]
    except : 
        return None         


def find_comp(company):
    for item in comp:
        if item['name'].strip().lower() == company.strip().lower():
            return {'name':company, 'foll': get_followers(item), 'emp': get_emp(item), 'lk_emp':get_lkd_emp(item), 'type': get_type(item)}
    return {'name':company, 'foll':0, 'emp':0, 'lk_emp':0, 'type':None}        

def bind_comp (row):
    tmp_companies = {'foll':[], 'emp':[], 'lk_emp':[]}
    tmp_type =[]
    for item in row['experiences']['companies']:
        res = find_comp(item)
        tmp_companies['foll'].append(res['foll'])
        tmp_companies['emp'].append( res['emp'])
        tmp_companies['lk_emp'].append(res['lk_emp'])
        tmp_type.append(res['type'])
    tmp_type = dict(Counter(list(filter(lambda x: x is not None, tmp_type))))    
    if tmp_companies['foll'] == []:
        return  {'foll_mean':0,'foll_sd':0 , 'emp_mean':0, 'emp_sd':0, 'lk_emp_mean':0,'lk_emp_sd':0 }, tmp_type   
    return {'foll_mean':np.mean(tmp_companies['foll']), 'foll_sd':np.std(tmp_companies['foll']) ,
            'emp_mean':np.mean(tmp_companies['emp']), 'emp_sd':np.std(tmp_companies['emp']),
            'lk_emp_mean':np.mean(tmp_companies['lk_emp']),'lk_emp_sd':np.std(tmp_companies['lk_emp']) }, tmp_type


#**************************************************************************

final_data = []

for i in range(len(data)):
    for  j in scrapped:
        if data[i]['id']==j['id']:
            tmp = data[i]
            tmp['certifs'] = len(j['certifs']) 
            tmp['recommendations'] = len(j['recomendations'])
            tmp['experiences']['companies'],tmp['experiences']['companies_type'] = bind_comp(tmp)
            final_data.append(tmp)
            scrapped.remove(j)
            break   


# saving dat :

try:
    db.drop_collection('final')
except:
    pass

col_final = db.create_collection('final')

col_final.insert_many(final_data)

# testing 
print(len(final_data))
t=1
print(final_data[t-1:t])
