var GameType = {
  SONG: "song",
  YEAR: "year",
  ARTIST: "artist",
};

$(document).ready(function() {
  var score = 0;
  var gametype = GameType.YEAR;
  var correctAnswer = null;

  // Set change game type handlers
  $('#menuYearButton').click(function() {
    updateScore(0);
    gameType = GameType.YEAR;

    $('#gamescreen').show();
    $('#warningsection').hide();
    loadNextSong();
  });
  $('#menuArtistButton').click(function() {
    
  });

  $('#gamescreen').hide();


  // Main loop function.
  function loadNextSong(callback) {
    console.log(gametype);
    updateScore(score);
    document.getElementById("songElement").pause(); // Pause current music

    clearPreviousRound();

    $.getJSON($SCRIPT_ROOT + '/_getSong', function(data) { // $SCRIPT_ROOT is set in game.html
      correctAnswer = data;
      setAudioSource(data.uri);

      var answerButtons = generateAnswerChoices(data.year);

      for (var i = 0; i < answerButtons.length; i++) {
        $('#userinput').append(answerButtons[i]);
      }
    });
  }

  function clearPreviousRound() {
    $('#userinput').empty();
  }

  function setAudioSource(uri) {
    var audioObject = document.getElementById("songElement");
    audioObject.src = uri;

    if(!audioObject.hasAttribute("controls")) {
      audioObject.setAttribute("controls", "controls");
    }

    audioObject.volume = 0.3;

    audioObject.load();
    audioObject.play();
  }

  // Generates a list of four buttons, one of which is the right answer
  function generateAnswerChoices(year) {
    // Generate years
    var arr = [year]
    while(arr.length < 4) {
      var randomnumber = Math.floor(Math.random() * 16) + 2000;
      if (arr.indexOf(randomnumber) > -1) continue;
      arr[arr.length] = randomnumber;
    }

    for (var i = 0; i < arr.length; i++) {
      var button = $('<button />', {
        text: arr[i],
      });

      if (i == 0) {// answer
        button.click(correctAnswerClick);
      } else {
        button.click(wrongAnswerClick);
      }

      arr[i] = button;
    }    

    // shuffle first element (answer)
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
    $('#result').text("Sorry, the right answer was " + correctAnswer.year);
    loadNextSong();
  }

  function updateScore(s) {
    score = s;
    $('#score').text(score);
  }

});