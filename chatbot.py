import recommend
import openai
import config
openai.api_key = config.api_key

choice = input("Do you want to get recommendations for a song or an album? (Enter 'song' or 'album'): ").strip().lower()
if choice == 'song':
    # Getting song recommendations
    artist = input("Enter artist name: ")
    song = input("Enter song name: ")
    song_recommendations = recommend.generate_SongRecommendations(artist, song)
    print("\nSong Recommendations:")
    print(song_recommendations)

elif choice == 'album':
    # Getting album recommendations
    artist = input("Enter artist name: ")
    album = input("Enter album name: ")
    album_recommendations = recommend.generate_AlbumRecommendations(artist, album)
    print("\nAlbum Recommendations: ")
    print(album_recommendations)

else:
    print("Invalid input. Please enter 'song' or 'album'.")
