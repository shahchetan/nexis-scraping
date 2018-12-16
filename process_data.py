import os
import pandas as pd
from bs4 import BeautifulSoup
from pprint import pprint

def checkIsInRange(str):
    for x in str:
        if ord(x) >= 65 and ord(x) <= 91:
            return True
    return False

mainDf = pd.DataFrame(columns=('Full Name', 'Address', 'County', 'Phone', 'SSN', 'DOB', 'Gender', 'LexID(sm)', 'Email'))
mainAddressDf = pd.DataFrame(columns=('LexID(sm)', 'Address', 'Dates', 'Phone No'))
mainRelativeDf = pd.DataFrame(columns=('LexID(sm)', 'Name', 'AlterName', 'SSN', 'DOB'))

idList = []
for root,dirs, fileNames in os.walk('html',topdown=False):
    for file_ in fileNames:
        idList.append(os.path.join(root,file_))

for idpath in idList:
    #with open(idpath,'r') as outfile:
    #    html_info = outfile.read()
    #soup = BeautifulSoup(html_info, features="html.parser")

    table_dict = {}
    tables = pd.read_html(idpath,flavor='bs4') # Returns list of all tables on page
    c = 0
    # for table in tables:
    #     print ("Index: ",c)
    #     print (table)
    #     c+=1
    #     print ("*********************************************************")
    # break
    tlen = len(tables)
    index = 3
    while index < tlen:
        if not pd.isna(tables[index][0][0]):
            # print (tables[index][0][0])
            if " 0 records found" in tables[index][0][0]:
                index+=1
            else:
                if "Address Summary" in tables[index][0][0]:
                    table_dict["Address Details"] = index+2
                    index+=3
                else:
                    table_dict[tables[index][0][0].split(" - ")[0].strip()] = index + 1
                    index+=2
        else:
            index+=1

    # print ("*******************************************************")

    # pprint(table_dict)

# Table 1: Contains Name, Address, County, Phone
    addressDf = pd.DataFrame(columns=('LexID(sm)', 'Address', 'Dates', 'Phone No'))
    relativeDf = pd.DataFrame(columns=('LexID(sm)', 'Name', 'AlterName', 'SSN', 'DOB'))
    tables[1] = tables[1].reindex(tables[1].index.drop(0))
    tables[1] = tables[1].reset_index(drop=True)
    ceo_info = pd.concat([tables[0], tables[1]], axis=1, ignore_index=True)
    ceo_info.columns = ceo_info.iloc[0]
    # ceo_info = ceo_info.reindex(ceo_info.index.drop(0))

    mainDf = mainDf.append(ceo_info.reindex(ceo_info.index.drop(0)),ignore_index=True)

    #Table 8: Contains different addresses of a person
    # print (cfo_info.shape)
    c =0
    if 'Address Details' in table_dict:
        address = tables[table_dict['Address Details']]
        # print (address)
        for index, row in address.iterrows():
            if "Address" == row[0] and "Dates" == row[1] and "Phone" == row[2]:
                addr = address.iloc[index+1,:]
                # print(addr)
                r = [ceo_info['LexID(sm)'][1]]
                r.extend(list(addr[0:-1]))
                addressDf.loc[c] = r
                c+=1
        # print ("Address Details")
        # print (addressDf.head())
        mainAddressDf = mainAddressDf.append(addressDf,ignore_index=True)
        # print(mainAddressDf.head())

    if 'Potential Relatives' in table_dict:
        pr = tables[table_dict['Potential Relatives']][1:]

        rel_id = 0
        for index,row in pr.iterrows():
            if not pd.isna(row[1]) and checkIsInRange(row[1]):
                dob,ssn = None,None
                if "DOB:" in row[1]:
                    dob = row[1].split("DOB:")[-1].strip()
                if "SSN:" in row[1]:
                    ssn = row[1].split("DOB:")[0].split("SSN:")[-1].strip()
                names = row[1].split("DOB:")[0].split("SSN:")[0].split('•')
                for i, aka in enumerate(names):
                    names[i] = names[i].replace('\xa0',' ').strip()
                r = [ceo_info['LexID(sm)'][1]]
                r.append(names[0])
                r.append(names[1:])

                r.extend([ssn,dob])
                # print (r)
                relativeDf.loc[rel_id] = r
                rel_id+=1
        # print ("Relative Details")
        # print(relativeDf)
        # print(type(relativeDf))
        mainRelativeDf = mainRelativeDf.append(relativeDf,ignore_index=True)
        # print ("\n***************************************************\n")

mainDf.to_csv('main.csv')
mainAddressDf.to_csv('address.csv')
mainRelativeDf.to_csv('relative.csv')


