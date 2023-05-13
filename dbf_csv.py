from dbfread import DBF
import os

DIRECTORY = '/Users/andrew/tmp/FF_MDTRMMIX_C_P_24M_202303_RERUN/FFFC_BRA_MDTRMMIX_Catalogs_830A_202303/'

headers = {}
# Go through each file and transform to DBF
headers = {}

def dbf_header(filename):
    tab = DBF(DIRECTORY+filename, load=True)
    idx = {}
    if tab.records:
        for row in tab.records[0].items():
            idx[row[0]] = row[1]
        headers[filename] = {"headers": list(tab.records[0].keys()), "value": idx}

for root, dirs, files in os.walk(DIRECTORY, topdown=True):
   for name in files:
      dbf_header(name)

headers = dict(sorted(headers.items(), key=lambda x: x[0]))

for k,v in headers.items():
    print(k)
    print(v['headers'])
    for k,v in v['value'].items():
        print(f"{k: <20} : {v.strip()}")
    print('------------------------------')
