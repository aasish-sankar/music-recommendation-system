let currentSong = null;

function displaySong(song) {
  $("#song-info").html(`
    <h2>Now Playing: ${song.song_title}</h2>
    <p>Movie: ${song.movie_name_tamil} (${song.year})</p>
    <p>Actors: ${song.actors}</p>
    <p>Singers: ${song.song_singers}</p>
    <p>Music by: ${song.song_music}</p>
  `);
}

function getNextSong() {
  $.get("/get-next-song", function (response) {
    if (response.song) {
      currentSong = response.song;
      displaySong(currentSong);
    }
  }).fail(function () {
    alert("No more songs available.");
  });
}

function sendFeedback(feedback) {
  if (currentSong) {
    $.ajax({
      url: "/send-feedback",
      type: "POST",
      data: { feedback: feedback },
      success: function (response) {
        currentSong = null; // Reset after sending feedback
        alert("Feedback sent successfully!");
      },
      error: function () {
        alert("Error sending feedback.");
      },
    });
  } else {
    alert("No song is selected.");
  }
}

function stopRecommendation() {
  $.post("/stop-recommendations", function (response) {
    $("#song-info").hide();
    $("#results").show();
    $("#total-likes").text(
      `Total liked songs: ${response.total_likes} out of ${response.recommendation_count}`
    );
    $("#favorite-composer").text(
      `Favorite Composer: ${response.favorite_composer || "None"}`
    );

    let additionalSongsHtml =
      "<h3>Additional Songs by Favorite Composer:</h3><ul>";
    response.additional_songs.forEach(function (song, index) {
      additionalSongsHtml += `<li>${song.song_title} from ${song.movie_name_tamil} (${song.year})</li>`;
    });
    additionalSongsHtml += "</ul>";
    $("#additional-songs").html(additionalSongsHtml);
  });
}

$(document).ready(function () {
  $("#next-song-button").click(getNextSong);
  $("#like-button").click(function () {
    sendFeedback(1); // Like
  });
  $("#dislike-button").click(function () {
    sendFeedback(0); // Dislike
  });
  $("#stop-recommendation-button").click(stopRecommendation);
});
