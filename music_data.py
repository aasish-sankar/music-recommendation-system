import pandas as pd
import logging

class MusicData:
    def __init__(self, file_name):
        self.file_name = file_name
        self.songs_df = self.load_songs()

    def load_songs(self):
        try:
            # Load the CSV file into a DataFrame
            data = pd.read_csv(self.file_name)
            logging.info("CSV file loaded successfully.")
            return data
        except Exception as e:
            logging.error(f"Error loading CSV file: {e}")
            return pd.DataFrame()  # Return an empty DataFrame on error

    def get_songs(self):
        return self.songs_df
