import spotifyutil
import pprint
import pdb
import random

def main():
    for i in xrange(100):
        year = random.randint(2000, 2016)
        result = spotifyutil.getRandomSongByYear(year)
        if result == None:
            print "NOOOOOOOOOOOOOO"
            break

if __name__ == '__main__':
     main() 