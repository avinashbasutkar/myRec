from flask import Flask, render_template, request
import requests
import os
import logging
from dotenv import load_dotenv

# Load the .env file from the current directory
load_dotenv()

logging.basicConfig(level=logging.DEBUG)

api_key = os.getenv('TMDB_API_READ_ACCESS_TOKEN')

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
@app.route('/')
def home():
    if request.method =='POST':
        search_query = request.form['search_query']

        movie_details_api_url = "https://api.themoviedb.org/3/search/movie?query={search_query}"
        configuration_api_url = "https://api.themoviedb.org/3/configuration"

        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        params = {
            "query": search_query
        }

        movie_details_api_response = requests.get(movie_details_api_url, headers=headers, params=params)
        configuration_api_response = requests.get(configuration_api_url, headers=headers, params=params)

        if movie_details_api_response.status_code and configuration_api_response.status_code == 200:
            movie_data = movie_details_api_response.json()
            configuration_data = configuration_api_response.json()

            # Update this line to retrieve all movie posters
            movie_poster_path = movie_data['results'][0]['poster_path']
            image_base_url = configuration_data['images']['base_url']

            if 'w185' in configuration_data['images']['poster_sizes']:
                movie_poster_size =  'w185'
            else:
                movie_poster_size = configuration_data['images']['poster_sizes'][-1]

            movie_poster_full_url = image_base_url + movie_poster_size + movie_poster_path

            return render_template('search_results.html', movie_poster=movie_poster_full_url, title='Search Results', search_query=search_query)
        else:
            movie_details_api_response_status_code = movie_details_api_response.status_code
            logging.error(f"Movie Details API Request Failed: {movie_details_api_response_status_code}")
            return render_template('error.html', response_status_code=movie_details_api_response_status_code)
    else:
        return render_template('home.html')

@app.route("/search_results")
def search_results():
    data = request.args.get('data')
    return render_template('search_results.html', data=data, title='Search Results')

if __name__ == '__main__':
    app.run(debug=True)