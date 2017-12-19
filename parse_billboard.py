from bs4 import BeautifulSoup
import requests
import json
import os
import errno

OUTPUT_DIR = '/static/output/'

def main():
    for year in xrange(2000, 2017):
        writeYearToJson(year)

def writeYearToJson(year):
    assert type(year) is int

    url = buildURLFromYear(year)
    r = requests.get("http://" + url)
    data = r.text
    soup = BeautifulSoup(data, "html.parser") # use default parser

    top100 = []
    mainTableRows = soup.findAll('tr')
    for mainTableRow in mainTableRows:
        row = mainTableRow.findAll('td')
        rank = row[0].getText()
        artist = row[1].getText()
        title = row[2].getText()
        entry = {'rank': rank, 'artist': artist, 'title': title}
        top100.append(entry)

    writeOutput(top100, year)

def buildURLFromYear(year):
    return "billboardtop100of.com/" + str(year) + "-2/"

def writeOutput(data, year):
    filename = os.getcwd() + OUTPUT_DIR + str(year) + '.json'
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: #guard race condition
            if exc.errno != errno.EEXIST:
                raise
    with open(filename, 'w') as f:
        json.dump(data, f)

if __name__ == "__main__":
    main()