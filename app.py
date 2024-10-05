from flask import Flask, jsonify, render_template, request, redirect, url_for
from bandit_agent import BanditAgent
from music_data import MusicData
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load song data
music_data = MusicData('tamil_songs.csv')
song_data = music_data.get_songs()

# Initialize Bandit Agent
bandit_agent = BanditAgent(song_data, epsilon=0.3)
current_song_index = None
total_likes = 0
recommendation_count = 0

@app.route('/')
def index():
    """Render introduction page."""
    return render_template('index.html')

@app.route('/start-recommendation')
def start_recommendation():
    """Render recommendation page."""
    return render_template('recommendation.html')

@app.route('/get-next-song', methods=['GET'])
def get_next_song():
    global current_song_index, recommendation_count
    song_index, song_info = bandit_agent.recommend_song()

    if song_info is not None:
        current_song_index = song_index
        song_dict = song_info.to_dict()
        recommendation_count += 1
        return jsonify({'song': song_dict})
    else:
        return jsonify({'error': 'No more songs available'}), 400

@app.route('/send-feedback', methods=['POST'])
def send_feedback():
    global current_song_index, total_likes
    feedback = request.form.get('feedback')  # Retrieve form data from frontend

    if feedback is None or current_song_index is None:
        return jsonify({'error': 'Invalid feedback or no song'}), 400

    feedback = int(feedback)  # Convert feedback to integer
    bandit_agent.update_rewards(current_song_index, feedback)
    total_likes += feedback

    current_song_index = None  # Reset the current song after feedback
    return jsonify({'success': True})

@app.route('/stop-recommendations', methods=['POST'])
def stop_recommendations():
    """Handle end of recommendation session and redirect to results page."""
    return redirect(url_for('results'))

@app.route('/results')
def results():
    """Render the results page with favorite composer and additional song recommendations."""
    global total_likes, recommendation_count
    favorite_composer = bandit_agent.get_favorite_composer()

    if favorite_composer:
        additional_songs = bandit_agent.recommend_additional_songs(favorite_composer, 10)
    else:
        additional_songs = []

    response_data = {
        'total_likes': total_likes,
        'recommendation_count': recommendation_count,
        'favorite_composer': favorite_composer,
        'additional_songs': additional_songs
    }

    total_likes = 0  # Reset for next session
    recommendation_count = 0  # Reset for next session

    return render_template('results.html', **response_data)

if __name__ == "__main__":
    app.run(debug=True)
