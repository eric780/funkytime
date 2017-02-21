var GameType = {
  SONG: "song",
  YEAR: "year",
  ARTIST: "artist",
};

var partyParrots = [
  "http://cultofthepartyparrot.com/parrots/dealwithitparrot.gif",
  "http://cultofthepartyparrot.com/parrots/parrotdad.gif",
  "http://cultofthepartyparrot.com/parrots/rightparrot.gif",
  "http://cultofthepartyparrot.com/parrots/aussieparrot.gif",
  "http://cultofthepartyparrot.com/parrots/parrotmustache.gif",
  "http://cultofthepartyparrot.com/parrots/partyparrot.gif",
];

$(document).ready(function() {
  var score = 0;
  var best_score = 0;
  var gametype = GameType.YEAR;
  var correctAnswer = null; // Stores correct answer

  // Hide game screen until user clicks a button
  $('#game-screen').hide();

  // Set change game type handlers
  $('#menu-year-button').click(function() {
    gametype = GameType.YEAR;

    $('#game-screen').show();
    $('#warning-section').hide();
    loadNextSong();

    $('#menu').hide();
  });

  $('#menu-artist-button').click(function() {
    gametype = GameType.ARTIST;

    $('#game-screen').show();
    $('#warning-section').hide();
    loadNextSong();

    $('#menu').hide();
  });

  $('#menu-song-button').click(function() {
    // TODO
  });

  $('#savebutton').click(function() {
    var username = window.prompt("Enter your username: ");
    // TODO SANITIZE
    $.post($SCRIPT_ROOT + '/savescore',
      {'username' : username, 'score' : best_score},
      function(data) {
        console.log(data);
      });
  });
  $('#viewscorebutton').click(function() {
    $.get($SCRIPT_ROOT + '/getscores',
      function(data) {
        var scores = data.scores;
        var displayString = "";
        for (var i = 0; i < scores.length; i++) {
          displayString += scores[i].username + "\t" + scores[i].score + "\n";
        }

        alert(displayString);
      });
  });

  // Set spacebar to pause/play song
  window.addEventListener("keydown", function(event) {
    switch (event.keyCode) {
      case 32: // Spacebar
        var audioObject = document.getElementById('song-element');
        if (audioObject.paused) {
          audioObject.play();
        } else {
          audioObject.pause();
        }
    }

    return false;
  }, false);


  // Main loop function.
  function loadNextSong(callback) {
    updateScore(score);
    document.getElementById("song-element").pause(); // Pause current music

    clearPreviousRound();

    $.post($SCRIPT_ROOT + '/_getSong',  // $SCRIPT_ROOT is set in game.html
      {'gametype': gametype}, 
      function(data) {
        correctAnswer = data.answers[0];

        setAudioSource(data.uri);

        var answerButtons = generateAnswerButtons(data.answers);

        for (var i = 0; i < answerButtons.length; i++) {
          $('#answer-section').append(answerButtons[i]);
        }
      });
  }

  function clearPreviousRound() {
    $('#answer-section').empty();
  }

  function setAudioSource(uri) {
    var audioObject = document.getElementById("song-element");
    audioObject.src = uri;

    if(!audioObject.hasAttribute("controls")) {
      audioObject.setAttribute("controls", "controls");
    }

    audioObject.volume = 0.3;

    audioObject.load();
    audioObject.play();
  }

  // Takes a list of answers, generates buttons w/ handlers, and shuffles them.
  function generateAnswerButtons(answers) {
    var arr = []
    for (var i = 0; i < answers.length; i++) {
      var button = $('<button />', {
        class: "answerButton",
        text: answers[i],
      });

      if (i == 0) { // right answer
        button.click(correctAnswerClick);
      } else {
        button.click(wrongAnswerClick);
      }

      arr[i] = button;
    }

    // swap first element
    var randomindex = Math.floor(Math.random() * 4);
    var temp = arr[randomindex]
    arr[randomindex] = arr[0];
    arr[0] = temp;

    return arr;
  }

  function correctAnswerClick() {
    updateScore(score + 1);
    $('#result').empty();

    $('#result').text("You got it!");
    $('#result').append("<img src='" + getPartyParrot() + "'/>");
    loadNextSong();
  }

  function wrongAnswerClick() {
    updateScore(0);
    $('#result').empty();
    $('#result').text("Sorry, the right answer was " + correctAnswer);
    loadNextSong();
  }

  function updateScore(s) {
    score = s;
    $('#score').text(score);

    if (score > best_score) {
      best_score = score;
      $('#best-score').text(best_score);
    }
  }

  function getPartyParrot() {
    return partyParrots[Math.floor(Math.random() * partyParrots.length)];
  }

});


