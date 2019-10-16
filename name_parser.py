import fitz
import re

out = []

doc = fitz.open("ARB.pdf")
page = doc.loadPage(2) #loop this for all your pages, should be a getNumPages function you can use i think?
text = page.getText("text")
#newlineRemove = re.sub("\n", " ", text)
pageSplitRemove = re.sub("\xad", "", text)
pageData = re.split(r'0\d{5}[A-Z]', text)
del pageData[0] #the zeroth index of pageData is empty due to how ive implemented split so i got rid of it
code = re.findall(r'0\d{5}[A-Z]', text) # regex for getting all the code things on the page
count = 0 #count is used to add the code thing to the final dictionary they all have since the split function above consumes that
for item in pageData:
    tempDict = {}
    item = item.lstrip()
    item = re.sub("\xad", "-", item)
    tempDict["code"] = test[code]

    name = item.split("\n")[0:1]
    tempDict["name"] = name[0]
    item = item.replace(name[0], "")    #removes the name from the current "item" to make getting the address later easy

    tel = re.search(r't:.*?,', item)    #regex for telephone numbers with comma endings
    if tel:
        tel = tel.group().replace(" ", "")
        tempDict["tel"] = tel[2:-1]
        
    else:
        tel = re.search(r't:.*?$\n', item) #regex for telephone numbers with newline endings
        if tel:
            tel = tel.group().replace(" ", "")
            tempDict["tel"] = tel[2:-1]

    email = re.search(r'e:.*?,', item)  # same as telephone
    if email:
        tempDict["email"] = email.group()[2:-1]
    else:
        email = re.search(r'e:.*?$\n', item) # same as telephone
        if email:
            tempDict["email"] = email.group()[2:-1]


    fax = re.search(r'f:.*?,', item) # same as telephone
    if fax:
        tempDict["fax"] = fax.group()[2:-1]
    else:
        fax = re.search(r'f:.*?$\n', item) # same as telephone
        if fax:
            tempDict["fax"] = fax.group()[2:-1]
    
    web = re.search(r'w:.*?,', item) #websites with comma endings

    if web:
        tempDict["web"] = web.group()[2:-1]
    else:
        web = re.search(r'w:.*?\n', item)
        if web:
            if web.group()[-2:-1] == "-":   #sometimes it splits websites on hypens for some reason, this captures them
                web = re.split(r'w:', item) 
                web = re.sub("\n", "", web[1]) #removes any newline characters from the found url
                tempDict["web"] = web
            else:
                web = web.group()[2:-1]
                tempDict["web"] = web


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

    count+=1
    out.append(tempDict)

for item in out:
    print(item)
