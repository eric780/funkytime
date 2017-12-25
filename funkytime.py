import random
import re
import os
import json
import pprint
from flask import Flask
from flask import render_template, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
from spotifyutil import getRandomSongByYear

CHARTNAME = 'hot-100'
MIN_YEAR = 2000 #TODO allow user to specify range
MAX_YEAR = 2016

app = Flask(__name__)
app.config['DEBUG'] = True
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/funky-time-scores'
heroku = Heroku(app)
db = SQLAlchemy(app)
GAME_TYPE_YEAR = 'year'

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
    Endpoint for generating a playlist
"""
@app.route("/play", defaults={'year': 2000})
@app.route("/play/<year>")
def getSongByYear(year):
    #TODO validate year
    song = getRandomSongByYear(year)
    track = spotify.track(song.spotifyID)
    return render_template('play.html', song = song, track = track, year = year)

"""
    Endpoint for getting a song for Game
"""
@app.route("/_getSong", methods=['POST'])
def getSongAndAnswers():
    # Returns json of the URI and a list of answers, first one being correct. JS will shuffle the list.

    gametype = request.form['gametype']
    year = random.randint(MIN_YEAR, MAX_YEAR)
    song = getRandomSongByYear(year)

    if gametype == GAME_TYPE_YEAR:
        answers = getAnswerChoicesForYear(year)
    else:
        raise InvalidGameTypeException()

    return jsonify(uri = song[u'preview_url'], answers = answers)

"""
    Given a year, return arr where the first element is the given year
    and the other 3 are unique and not year
"""
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
    app.run(host='0.0.0.0', port=port, debug=True)
    # getRandomSongByYear(2014)
