from flask import Flask, render_template, url_for, request, jsonify
import requests
import os

api_key = os.getenv('TMDB_API_KEY')
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
@app.route('/')
def home():
    if request.method =='POST':
        search_query = request.form['search_query']

        url = "https://api.themoviedb.org/3/search/movie?query={search_query}"

        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        params = {
            "query": search_query
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            return render_template('search_results.html', data=data, title='Search Results', search_query=search_query)
        else:
            return render_template('error.html')
    else:
        return render_template('home.html')
    # return render_template('home.html')

@app.route("/search_results")
def search_results():
    data = request.args.get('data')
    return render_template('search_results.html', data=data, title='Search Results')

# @app.route("/search")
# def search():
#     query = request.args.get('query')
#     return render_template('search_results.html', data=data, title='Search Results')

@app.route("/about")
def about():
    return render_template('about.html', title='About Us')

if __name__ == '__main__':
    app.run(debug=True)