let currentSong = null;
let songNotFoundTimer = null;

function displaySong(song) {
  clearTimeout(songNotFoundTimer); // Clear any pending timer for no song found
  $("#spinner").hide(); // Hide spinner when the song is loaded
  $("#song-info").html(`
    <h2>Now Playing: ${song.song_title}</h2>
    <p>Movie: ${song.movie_name_tamil} (${song.year})</p>
    <p>Actors: ${song.actors}</p>
    <p>Singers: ${song.song_singers}</p>
    <p>Music by: ${song.song_music}</p>
  `);
  enableButtons(); // Enable feedback buttons when a song is ready
}

function getNextSong() {
  disableButtons(); // Disable buttons while fetching the next song
  $("#spinner").show(); // Show spinner while waiting for the next song

  // Start a timer for 1 minute to check if no song is found
  songNotFoundTimer = setTimeout(function() {
    alert("No song recommendation found after 1 minute.");
  }, 60000); // 60 seconds

  $.get("/get-next-song", function (response) {
    if (response.song) {
      currentSong = response.song;
      displaySong(currentSong);
    } else {
      retrySongFetch(); // Retry if no song is found
    }
  }).fail(function () {
    retrySongFetch(); // Retry if there is an error
  });
}

function retrySongFetch() {
  setTimeout(function() {
    getNextSong(); // Retry fetching after a delay of 2 seconds
  }, 2000);
}

function sendFeedback(feedback) {
  if (currentSong) {
    disableButtons();
    $.ajax({
      url: "/send-feedback",
      type: "POST",
      data: { feedback: feedback },
      success: function () {
        currentSong = null; // Reset after sending feedback
        setTimeout(() => {
          getNextSong(); // Automatically fetch the next song
        }, 300); // Short delay for smoother experience
      },
      error: function () {
        alert("Error sending feedback.");
        retrySongFetch(); // Retry fetching the next song
      },
    });
  } else {
    retrySongFetch(); // Retry if no song is selected
  }
}

function disableButtons() {
  $("#like-button").prop('disabled', true);
  $("#dislike-button").prop('disabled', true);
  $("#next-song-button").prop('disabled', true);
}

function enableButtons() {
  $("#like-button").prop('disabled', false);
  $("#dislike-button").prop('disabled', false);
  $("#next-song-button").prop('disabled', false);
}

$(document).ready(function () {
  getNextSong(); // Load the first song when the page loads

  // Set up click handlers for the feedback buttons
  $("#like-button").click(function () {
    sendFeedback(1);
  });

  $("#dislike-button").click(function () {
    sendFeedback(0);
  });

  // Set up click handler for manually fetching the next song
  $("#next-song-button").click(function () {
    getNextSong();
  });
});
