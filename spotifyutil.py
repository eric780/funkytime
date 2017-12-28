import json
import pprint
import os
import pdb
import re
import random
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from settings import APP_STATIC

RANKING_CUTOFF = 25 

client_credentials_manager = SpotifyClientCredentials(
    client_id = '63ab4c7c7abe45ba8a1e87a2306b0632', 
    client_secret = 'd9fb47cfdbab4402ba3727262ff966de'
)
token = client_credentials_manager.get_access_token()
spotify = spotipy.Spotify(auth=token)

"""
    Takes a year and returns a song object from database
"""
def getRandomSongByYear(year):
    randomSong = getRandomSongByYearFromDatabase(year)
    spotifyRandomSong = getSongFromSpotify(randomSong)
    return spotifyRandomSong

def getRandomSongByYearFromDatabase(year):
    yearData = getYearDataFromDatabase(year)
    databaseSongData = yearData[random.randint(0, RANKING_CUTOFF)]
    songData = convertUnicodeDictToString(databaseSongData)
    cleanedSongData = cleanupSongData(songData)
    return cleanedSongData

def getYearDataFromDatabase(year):
    filename = os.path.join(APP_STATIC, 'output/' + str(year) + '.json')
    yearData = json.load(open(filename))
    return yearData

def getSongFromSpotify(songData):
    queryString = buildSpotifyQuery(songData)
    results = spotify.search(queryString, type='track')
    tracks = results['tracks']
    items = tracks['items']

    print "SEARCH RESULTS: "
    for item in items:
        artists = ""
        for artist in item['artists']:
            artists += artist['name']
        print item['name'] + artists
    print "QUERY STRING: "
    print queryString
    print "SONG DATA: "
    pprint.pprint(songData)

    #TODO check if empty, handle case
    return pickBestSearchResult(songData, items)


def buildSpotifyQuery(songData):
    return songData['title'].replace(" ", "+")

def convertUnicodeDictToString(dict):
    return {k.encode('utf-8') : v.encode('utf-8') for k,v in dict.items()}

def cleanupSongData(songData):
    # split string by the following delimiters:
    # "feat.", ",", "&"
    artists = re.split('feat.|,|&', songData['artist'])
    # strip out whitespace
    for index, artist in enumerate(artists):
        artists[index] = artist.strip()
    songData['artist'] = artists

    #strip rank and title as well
    songData['rank'] = songData['rank'].strip()
    songData['title'] = songData['title'].strip()
    return songData

# Picks the best search result from searchResults, given songData
# Currently that matches based on if the primary artist in songData
# is an artist listed in searchResults
def pickBestSearchResult(songData, searchResults):
    # pdb.set_trace()

    bestResult = searchResults[0]
    artists = songData['artist']
    for result in searchResults:
        if artists[0] in [item['name'] for item in result['artists']]:
            bestResult = result
            break

    print "CHOSEN RESULT: "
    artistString = ""
    for artist in bestResult['artists']:
        artistString += artist['name']

    print bestResult['name'] + " by " + artistString
    return bestResult