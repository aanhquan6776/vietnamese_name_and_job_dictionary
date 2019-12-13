import requests
from bs4 import BeautifulSoup

root = "https://thongtinthuebao.com"
def saveData(url, records):
    datafile = "crawled/" + url.replace('/', '_') + ".txt"
    with open(datafile, "w") as file:
        output = "\n".join(records)
        file.write(output)

        
def checkHistory(url):
    """
    return True if the url is already exist
    """
    logfile = "crawled/history.txt"
    with open(logfile, "r") as records:
        return ((url+"\n") in records)
    
def updateHistory(url):
    logfile = "crawled/history.txt"
    with open(logfile, "a") as file:
        file.write(url+"\n")
        

def getNextPage(full_url):
    # Collect and parse first page
    page = requests.get(full_url)
    soup = BeautifulSoup(page.text, 'html.parser')

    pagination = soup.find(class_="pagination")
    
    if pagination:
        next_urls = pagination.find_all('a', href=True)

        current_reached = False
        for next_url in next_urls:
            if current_reached:
                return root + next_url['href']
            if (next_url['href'].strip() == "javascript:")  and (next_url.contents[0].strip()!='500'):
                current_reached = True
    return ""


def getData(full_url):
    result = []
    # Collect and parse first page
    page = requests.get(full_url)
    soup = BeautifulSoup(page.text, 'html.parser')

    blocks = soup.find_all(class_='text-uppercase push-10')

    for block in blocks:
        record = block.find('a')
        info = record.contents[0]
        result.append(info)
        
    return result


def getAllData(url):
    result = []
    if checkHistory(url):
        return result
    tmp_url = root + url
    while True:
#         print(tmp_url)
        result.extend(getData(tmp_url))
        tmp_url = getNextPage(tmp_url)
        if len(tmp_url)==0:
            break
        
    saveData(url, result)
    updateHistory(url)
    print(url, ': ', len(result))
    return result
    
    
def isElemental(url):
    if url=="":
        return False
    
    # Collect and parse first page
    full_url = root + url
    page = requests.get(full_url)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    right_column = soup.find_all(class_="block-content block-content-full")
    return len(right_column)==1
    
    
def getSubURLs(full_url):
    result = []
    # Collect and parse first page
    page = requests.get(full_url)
    soup = BeautifulSoup(page.text, 'html.parser')

    sub_urls_part = soup.find(class_="block-content block-content-full")

    if sub_urls_part:
        records = sub_urls_part.find_all('a', href=True)

    for record in records:
        sub_url = record['href']
        result.append(sub_url)
        
    return result


def dfs(url):
#     print(url)
    if isElemental(url):
        return getAllData(url)
    
    result = []
    full_url = root + url
    sub_urls = getSubURLs(full_url)
    for sub_url in sub_urls:
        result.extend(dfs(sub_url))
        
    return result

records = dfs("")
print(len(records))
