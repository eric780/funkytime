from bs4 import BeautifulSoup
import requests
import json
import os
import re
import unidecode
import errno

OUTPUT_DIR = '/static/output/'

def main():
    # for year in xrange(2000, 2017):
    #     writeYearToJson(year)
    writeYearToJson(2013)

def writeYearToJson(year):
    assert type(year) is int

    url = buildURLFromYear(year)
    r = requests.get("http://" + url)
    data = r.text
    soup = BeautifulSoup(data, "html.parser") # use default parser

    top100 = []
    if year == 2013:
        # handle special case for 2013
        top100string = soup.findAll('p')[2].getText()
        top100lines = top100string.split('\n')
        top100 = list(map(processIndividualLine, top100lines))
        print top100

    else:
        mainTableRows = soup.findAll('tr')
        for mainTableRow in mainTableRows:
            row = mainTableRow.findAll('td')
            rank = unidecode.unidecode(row[0].getText())
            artist = unidecode.unidecode(row[1].getText())
            title = unidecode.unidecode(row[2].getText())
            entry = {'rank': rank, 'artist': artist, 'title': title}
            top100.append(entry)

    writeOutput(top100, year)

# Helper for 2013 which for some reason is just one giant string
def processIndividualLine(line):
    line = unidecode.unidecode(line)
    # split by period and dash
    info = re.split('\.|-', line)
    rank = info[0].strip()
    artist = info[1].strip()
    title = info[2].strip()
    return {'rank': rank, 'artist': artist,'title': title}


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