import pandas as pd

# Load the dataset
songs_df = pd.read_csv('songs.csv')

# Function to recommend songs by genre
def recommend_songs(song_title):
    # Find the genre of the input song
    song_info = songs_df[songs_df['title'] == song_title]
    
    if song_info.empty:
        return "Song not found."

    genre = song_info['genre'].values[0]
    
    # Recommend songs of the same genre, excluding the original song
    recommendations = songs_df[songs_df['genre'] == genre]
    recommendations = recommendations[recommendations['title'] != song_title]

    return recommendations[['title', 'artist']]

# Example usage
if __name__ == "__main__":
    user_song = input("Enter a song title to get recommendations: ")
    recommended_songs = recommend_songs(user_song)
    
    if isinstance(recommended_songs, str):
        print(recommended_songs)
    else:
        print("Recommended Songs:")
        for index, row in recommended_songs.iterrows():
            print(f"{row['title']} by {row['artist']}")
