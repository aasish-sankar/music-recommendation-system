import random
from collections import defaultdict
import logging

class BanditAgent:
    def __init__(self, song_data, epsilon=0.3):
        self.song_data = song_data.reset_index(drop=True)  # Ensure continuous indexing
        self.epsilon = epsilon  # Exploration rate
        self.song_indices = list(self.song_data.index)  # Track song indices
        self.song_rewards = [0] * len(self.song_indices)  # Store rewards for each song
        self.recommendations = set()  # Keep track of recommended songs as a set to avoid repetition
        self.composer_likes = defaultdict(int)  # Track likes for each composer
        self.penalized_composers = defaultdict(int)  # Track penalized composers

    def recommend_song(self):
        available_songs = [i for i in self.song_indices if i not in self.recommendations]
        if not available_songs:
            logging.warning("No available songs for recommendation.")
            return None, None

        # Explore or exploit
        if random.uniform(0, 1) < self.epsilon:
            song_index = random.choice(available_songs)  # Explore
        else:
            # Exploit the best song based on rewards minus penalties
            song_index = max(available_songs, key=lambda i: self.song_rewards[i] - self.penalized_composers[self.song_data.loc[i]['song_music']])

        # Add the recommended song to the recommendations set
        self.recommendations.add(song_index)

        logging.info(f"Song index {song_index} recommended.")
        return song_index, self.song_data.loc[song_index]

    def update_rewards(self, song_index, feedback):
        song_info = self.song_data.loc[song_index]
        composer = song_info['song_music']
        singers = song_info['song_singers']

        if feedback == 1:
            self.song_rewards[song_index] += 1
            self.composer_likes[composer] += 1
            logging.info(f"Positive feedback for song {song_index}.")
        else:
            self.song_rewards[song_index] -= 1
            self.penalized_composers[composer] += 1
            logging.info(f"Negative feedback for song {song_index}.")

            # Penalize all songs by the same composer and singers
            for i, song in self.song_data.iterrows():
                if song['song_music'] == composer:
                    self.song_rewards[i] -= 0.5
                if song['song_singers'] == singers:
                    self.song_rewards[i] -= 0.2

    def get_favorite_composer(self):
        if self.composer_likes:
            return max(self.composer_likes, key=self.composer_likes.get)
        return None

    def recommend_additional_songs(self, composer, count=10):
        """Recommends additional songs by the favorite composer."""
        composer_songs = self.song_data[self.song_data['song_music'] == composer]
        return composer_songs.head(count).to_dict(orient='records')
