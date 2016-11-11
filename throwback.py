import billboard
import argparse
import random
import re

parser = argparse.ArgumentParser(description = 'Throwbacks')
parser.add_argument('year')

CHARTNAME = 'hot-100'

def getRandomSongByYear(year):
    month = random.randint(1,12)
    day = random.randint(1,28)
    date = str(year) + '-' + str(month) + '-' + str(day)
    
    # SLOW AF
    # ---------------------------------------------------------------------
    while True:
        month = random.randint(1,12)
        day = random.randint(1,28)
        date = str(year) + '-' + str(month) + '-' + str(day)
        chart = billboard.ChartData(CHARTNAME, date=date) # TODO fetch=False to get data l8r

        if len(chart.entries) > 0:
            break
        
    while True:
        song = chart[random.randint(0,10)]
        if len(song.spotifyID) > 0:
            break
    # ----------------------------------------------------------------------

    return song

if __name__ == '__main__':
    args = parser.parse_args()

    # TODO make it so it doesn't repeat songs very often
    
    
    year = args.year # TODO regex check year
    for i in xrange(0,100):
        song = getRandomSongByYear(year)
        if len(song.spotifyID) == 0:
            print song
        print i
