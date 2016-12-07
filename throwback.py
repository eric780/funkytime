import billboard
import spotipy
import random
import re
from flask import Flask
from flask import render_template, url_for, request, jsonify

CHARTNAME = 'hot-100'
DEFAULT_YEAR = 2012

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['DEFAULT_YEAR'] = str(DEFAULT_YEAR)
spotify = spotipy.Spotify()


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
        song = chart[random.randint(0,15)]
        if song.artist == 'Taylor Swift':
            continue
        if len(song.spotifyID) > 0:
            track = spotify.track(song.spotifyID)
            if track['preview_url'] != None:
                break

    # ----------------------------------------------------------------------

    return song

@app.route("/play", defaults={'year': 2000})
@app.route("/play/<year>")
def getSongByYear(year):
    print year
    #TODO validate year
    song = getRandomSongByYear(year)
    track = spotify.track(song.spotifyID)
    return render_template('play.html', song = song, track = track, year = year)

@app.route("/_getSong")
def getRandomSong():
    #TODO return spotify URL for a random song between years
    MIN_YEAR = 2000 #TODO allow user to change
    MAX_YEAR = 2015
    year = random.randint(MIN_YEAR, MAX_YEAR)
    song = getRandomSongByYear(year)
    track = spotify.track(song.spotifyID)
    return jsonify(uri = track['preview_url'], year=year, name=track['name'], artist=track['artists'])

@app.route("/game")
def game():
    return render_template('game.html')

@app.route("/")
@app.route("/index")
def main():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
