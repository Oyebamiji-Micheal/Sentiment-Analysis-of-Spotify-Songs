import os
from flask import Flask, render_template, request, jsonify
import pandas as pd
from sentiment_analysis import preprocess_lyrics, analyze_sentiment

# Initialize Flask app
app = Flask(__name__)

# Load song data
df = pd.read_csv('required.csv')
top_20_songs = df.nlargest(20, 'popularity')

def truncate_lyrics(lyrics, word_limit=100):
    words = lyrics.split()
    truncated = ' '.join(words[:word_limit])
    return truncated.capitalize() + '...'

# Route for home page
@app.route('/', methods=['GET'])
def homePage():
    # Select 5 random songs from the top 20 most popular
    random_songs = top_20_songs.sample(5).to_dict('records')
    return render_template("index.html", popular_songs=random_songs)

# Route to fetch lyrics and analyze sentiment
@app.route('/lyrics', methods=['GET', 'POST'])
def lyrics():
    if request.method == 'POST':
        artist = request.form.get('artist')
        title = request.form.get('title')
        lyrics_input = request.form.get('lyrics-search')
    else:
        artist = request.args.get('artist')
        title = request.args.get('title')
        lyrics_input = request.args.get('lyrics-search')

    print(artist, title, lyrics_input)

    if lyrics_input:
        song_lyrics = lyrics_input
    else:
        # Fetch lyrics from the dataframe
        song = df[(df['cleaned_artists'] == artist) & (df['song_name'] == title)].iloc[0]
        song_lyrics = song['cleaned_lyrics']
    
    if song_lyrics:
        preprocessed_lyrics = preprocess_lyrics(song_lyrics)
        compound_score, sentiment = analyze_sentiment(preprocessed_lyrics)
        return jsonify({
            'title': title if title else 'N/A',
            'artist': artist if artist else 'N/A',
            'lyrics': preprocessed_lyrics,
            'sentiment': sentiment,
            'compound_score': compound_score
        })
    else:
        return jsonify({'error': 'Lyrics not found.'})

if __name__ == "__main__":
    app.run(debug=True)
