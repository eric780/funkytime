from bs4 import BeautifulSoup
import requests

#url = raw_input("Please enter a URL from billboardtop100of.com: ")
url = "billboardtop100of.com/2010-2/"
r = requests.get("http://" + url)
data = r.text
soup = BeautifulSoup(data, "html.parser") # use default parser

# Container
top100 = []

mainTableRows = soup.findAll('tr')
for mainTableRow in mainTableRows:
    row = mainTableRow.findAll('td')
    rank = row[0].getText()
    artist = row[1].getText()
    title = row[2].getText()
    top100.append((rank, artist, title))

print top100[:10]