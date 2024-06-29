import os
from flask import Flask, render_template, request, jsonify
import pandas as pd
from sentiment_analysis import preprocess_lyrics, analyze_sentiment

# Initialize Flask app
app = Flask(__name__)

# Load song data
df = pd.read_csv('required.csv')
top_20_songs = df.nlargest(20, 'popularity')

# Route for home page
@app.route('/', methods=['GET'])
def homePage():
    # Select 5 random songs from the top 20 most popular
    random_songs = top_20_songs.sample(5).to_dict('records')
    return render_template("index.html", afrobeats_songs=random_songs)

# Route to fetch lyrics and analyze sentiment
@app.route('/lyrics', methods=['GET'])
def lyrics():
    artist = request.args.get('artist')
    title = request.args.get('title')

    if not artist or not title:
        return jsonify({'error': 'Artist and title are required.'})

    try:
        import azapi
        API = azapi.AZlyrics('google', accuracy=0.5)
        API.artist = artist
        API.title = title
        API.getLyrics(save=False, ext='lrc')
    except Exception as e:
        return jsonify({'error': f'Failed to fetch lyrics: {str(e)}. Kindly refresh.'})

    song_lyrics = API.lyrics
    if song_lyrics:
        preprocessed_lyrics = preprocess_lyrics(song_lyrics)
        compound_score, sentiment = analyze_sentiment(preprocessed_lyrics)
        return jsonify({
            'title': API.title,
            'artist': API.artist,
            'lyrics': song_lyrics,
            'sentiment': sentiment,
            'compound_score': compound_score
        })
    else:
        return jsonify({'error': 'Lyrics not found.'})

if __name__ == "__main__":
    app.run()
