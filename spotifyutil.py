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

    while spotifyRandomSong == None:
        randomSong = getRandomSongByYearFromDatabase(year)
        spotifyRandomSong = getSongFromSpotify(randomSong)

    return spotifyRandomSong

def getRandomSongByYearFromDatabase(year):
    return getSongByYearFromDatabase(year, random.randint(0, RANKING_CUTOFF))

"""
    Helper function that pulls a specific song given a year and index within the year
    Handles conversion to unicode and cleaning. Use this for all accesses.
"""
def getSongByYearFromDatabase(year, index):
    yearData = getYearDataFromDatabase(year)
    databaseSongData = yearData[index]
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

    # TODO CASES:
    # Beyonce with accent on e
    # Songs that are not on first page (ie. Sunshine by Lil' Flip 2004)

    bestSearchResult = pickBestSearchResult(songData, items)
    if bestSearchResult == None:
        print 'GOT NONE'
    return bestSearchResult


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
# returns None if none found
def pickBestSearchResult(songData, searchResults):
    # pdb.set_trace()

    artists = songData['artist']
    for result in searchResults:
        if artists[0] in [item['name'] for item in result['artists']]:

            print "CHOSEN RESULT: "
            artistString = ""
            for artist in result['artists']:
                artistString += artist['name']
            print result['name'] + " by " + artistString

            return result
    return None