var GameType = {
  SONG: "song",
  YEAR: "year",
  ARTIST: "artist",
};

$(document).ready(function() {
  var score = 0;
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
    $('#result').text("You got it!");
    loadNextSong();
  }

  function wrongAnswerClick() {
    updateScore(0);
    $('#result').text("Sorry, the right answer was " + correctAnswer);
    loadNextSong();
  }

  function updateScore(s) {
    score = s;
    $('#score').text(score);
  }

});