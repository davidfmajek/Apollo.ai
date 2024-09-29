import openai
import config  # import your config module
from flask import Flask, render_template, request, jsonify

# set your OpenAI API key from the config file
openai.api_key = config.api_key
app = Flask(__name__)


# function to generate song recommendations based on user input
def generate_SongRecommendations(artist_name, song_name):
    prompt = f"Based on the song '{song_name}' by {artist_name}, recommend five similar songs based on genre and instrumentals. output only song name and artist name"
    
    response = openai.chat.completions.create(
        model="gpt-4", 
        messages=[{"role": "user", "content": prompt}]
    )
    recommendations = response.choices[0].message.content
    return recommendations


def generate_AlbumRecommendations(album_name, artist_name):
    prompt = f"Based on the album '{album_name}' by {artist_name}, recommend five similar albums based on genre and instrumentals. output only album name and artist name"
    
    response = openai.chat.completions.create(
        model="gpt-4", 
        messages=[{"role": "user", "content": prompt}]
    )
    recommendations = response.choices[0].message.content
    return recommendations 

# Flask route for the homepage
@app.route
def index():
    return render_template('index.html')

# Handle recommendations request
@app.route('/recommendations', methods=['POST'])
def get_recommendations():
    # Get form data
    artist_name = request.form['artist']
    song_name = request.form['song']
    
    # Get recommendations
    recommendations = generate_SongRecommendations(artist_name, song_name)
    

    # Pass recommendations to the HTML page
    return render_template('index.html', recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
