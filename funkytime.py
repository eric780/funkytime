import billboard
import spotipy
import random
import re
import os
from flask import Flask
from flask import render_template, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku

CHARTNAME = 'hot-100'
DEFAULT_YEAR = 2012
MIN_YEAR = 2000 #TODO allow user to specify range
MAX_YEAR = 2016

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['DEFAULT_YEAR'] = str(DEFAULT_YEAR)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/funky-time-scores'
heroku = Heroku(app)
db = SQLAlchemy(app)
spotify = spotipy.Spotify()

GAME_TYPE_YEAR = 'year'
GAME_TYPE_ARTIST = 'artist'
GAME_TYPE_SONG = 'song'

MAX_LENGTH_USERNAME = 100
LEADERBOARD_SIZE = 20


class InvalidGameTypeException(Exception):
    pass

"""
    Database Model
"""
class LeaderboardEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(MAX_LENGTH_USERNAME))
    score = db.Column(db.Integer)

    def __init__(self, username, score):
        self.username = username
        self.score = score

    def __repr__(self):
        return self.username + ', ' + str(self.score)

    def serialize(self):
        return {'username' : self.username, 'score' : self.score}

"""
    Saves a score into the DB
"""
@app.route('/savescore', methods=['POST'])
def savescore():
    username = request.form['username'] # TODO SANITIZE
    score = request.form['score']
    new_score = LeaderboardEntry(username, score)

    db.session.add(new_score)
    db.session.commit()
    return jsonify(success=True, error=None)

"""
    Returns the top k scores in the DB
"""
@app.route('/getscores', methods=['GET'])
def getHighScores():
    high_scores = LeaderboardEntry.query.order_by(LeaderboardEntry.score.desc()).limit(LEADERBOARD_SIZE).all()
    high_scores_serializable = [entry.serialize() for entry in high_scores]
    return jsonify(scores=high_scores_serializable)

"""
    Takes a year and returns a song object from billboard
"""
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
        chart = billboard.ChartData(CHARTNAME, date=date)
        
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
    #TODO validate year
    song = getRandomSongByYear(year)
    track = spotify.track(song.spotifyID)
    return render_template('play.html', song = song, track = track, year = year)

@app.route("/_getSong", methods=['POST'])
def getSongAndAnswers():
    # Returns json of the URI and a list of answers, first one being correct. JS will shuffle the list.

    gametype = request.form['gametype']
    year = random.randint(MIN_YEAR, MAX_YEAR)
    song = getRandomSongByYear(year)
    track = spotify.track(song.spotifyID)
    artist = track['artists'][0]

    if gametype == GAME_TYPE_YEAR:
        answers = getAnswerChoicesForYear(year)
    elif gametype == GAME_TYPE_ARTIST:
        answers = getAnswerChoicesForArtist(artist)
    elif gametype == GAME_TYPE_SONG:
        answers = []
    else:
        raise InvalidGameTypeException()

    return jsonify(uri = track['preview_url'], answers = answers)

def getAnswerChoicesForYear(year):
    arr = [year]
    while len(arr) < 4:
        rand = random.randint(MIN_YEAR, MAX_YEAR)
        if rand in arr:
            continue
        arr.append(rand)
    return arr

def getAnswerChoicesForArtist(artist):
    related_artists = spotify.artist_related_artists(artist['id'])['artists']
    related_artists = [artist] + related_artists[0:3]

    return [a['name'] for a in related_artists]

@app.route("/game")
def game():
    return render_template('game.html')

@app.route("/")
@app.route("/index")
def main():
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
