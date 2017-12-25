import json
import pprint
import os
import random
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from settings import APP_STATIC

RANKING_CUTOFF = 20

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
    filename = os.path.join(APP_STATIC, 'output/' + str(year) + '.json')
    yearData = json.load(open(filename))

    randomSong = convertUnicodeDictToString(yearData[random.randint(0, RANKING_CUTOFF)])
    return randomSong

def getSongFromSpotify(songData):
    #TODO call spotify endpoint and select track
    queryString = buildSpotifyQuery(songData)
    results = spotify.search(queryString, type='track')
    tracks = results['tracks']
    items = tracks['items']

    for item in items:
        artists = ""
        for artist in item['artists']:
            artists += artist['name']
        print item['name'] + artists
    print queryString
    pprint.pprint(songData)

    #TODO check if empty, handle case
    # return track[u'items'][0]

def buildSpotifyQuery(songData):
    # TODO create string query from song data using songData.title and songData.artist
    title = songData[u'title'].replace(" ", "+")
    queryString = title
    return queryString

def convertUnicodeDictToString(dict):
    return {str(k) : str(v) for k,v in dict.items()}

def cleanupSongData(songData):
    # TODO remove "feat." and split artists into an array
    return