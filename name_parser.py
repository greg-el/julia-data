import fitz
import re

out = []

doc = fitz.open("ARB.pdf")
page = doc.loadPage(2)
text = page.getText("text")
#newlineRemove = re.sub("\n", " ", text)
pageSplitRemove = re.sub("\xad", "", text)
x = re.split(r'0\d{5}[A-Z]', text)
del x[0]
test = re.findall(r'0\d{5}[A-Z]', text)
count = 0
for item in x:
    #print(repr(item))
    
    tempDict = {}
    item = item.lstrip()
    item = re.sub("\xad", "-", item)
    #print(item)

    tempDict["code"] = test[count]

    name = item.split("\n")[0:1]
    tempDict["name"] = name[0]
    item = item.replace(name[0], "")

    item = item.replace("Â-", "-")
    

    tel = re.search(r't:.*?,', item)
    if tel:
        tel = tel.group().replace(" ", "")
        tempDict["tel"] = tel[2:-1]
        
    else:
        tel = re.search(r't:.*?$\n', item)
        if tel:
            tel = tel.group().replace(" ", "")
            tempDict["tel"] = tel[2:-1]

    email = re.search(r'e:.*?,', item)
    if email:
        tempDict["email"] = email.group()[2:-1]
    else:
        email = re.search(r'e:.*?$\n', item)
        if email:
            tempDict["email"] = email.group()[2:-1]


    #item = re.sub("\n", "", item)

    fax = re.search(r'f:.*?,', item)
    if fax:
        tempDict["fax"] = fax.group()[2:-1]
    else:
        fax = re.search(r'f:.*?$\n', item)
        if fax:
            tempDict["fax"] = fax.group()[2:-1]
    
    web = re.search(r'w:.*?,', item)

    if web:
        tempDict["web"] = web.group()[2:-1]
    else:
        web = re.search(r'w:.*?\n', item)
        if web:
            if web.group()[-2:-1] == "-":   
                web = re.split(r'w:', item) 
                web = re.sub("\n", "", web[1])
                
                tempDict["web"] = web
            else:
                web = web.group()[2:-1]
                tempDict["web"] = web


    count+=1

    item = item.strip()
    address = ""
    for i in range(0, len(item)-1):
        testCase = item[i]+item[i+1]
        exitCondition = ["t:", "f:", "e:", "w:"]
        if testCase in exitCondition:
            break
        else:
            address += item[i]
    address = re.sub("\n", "", address)
    address = address.strip()
    if address[-1] == ",":
        address = address[0:-1]
    tempDict["address"] = address



    out.append(tempDict)

for item in out:
    print(item)
