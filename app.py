from flask import Flask, app, render_template, request, redirect, url_for
from bs4 import BeautifulSoup
import requests
import random

app = Flask(__name__)

ROTTEN_TOMATO_TOP_URL = "https://editorial.rottentomatoes.com/guide/best-movies-of-all-time/"

user_agents_list = [
    'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    genre = request.form['genre']
    min_year = request.form['minYear']
    max_year = request.form['maxYear']

    if genre == 'none':
        return redirect(url_for('scrape_rotten_tomato', page=1, _method='POST'))
    else:
        return redirect(url_for('scrape_metacritic', genre=genre, min_year=min_year, max_year=max_year, page=1, _method='POST'))


@app.route('/randomize', methods=['POST'])
def randomize():
    genre = request.form['genre']
    min_year = request.form['minYear']
    max_year = request.form['maxYear']

    page = 1
    if genre == 'none':
        response = requests.get(ROTTEN_TOMATO_TOP_URL, headers={'User-Agent': random.choice(user_agents_list)})
        soup = BeautifulSoup(response.content, 'html.parser')
        results = soup.find(id="article_main_body")
        titles = results.find_all("a", class_="title")
        years = results.find_all("span", class_="year")
        scores = results.find_all("span", class_="score")
        movies = [{'title': title.get_text(strip=True), 'score': score.get_text(strip=True), 'year': year.get_text(strip=True)}
                  for title, score, year in zip(titles, scores, years)]
    else:
        METACRITIC_GENRE_URL = f"https://www.metacritic.com/browse/movie/all/{genre}/all-time/metascore/?releaseYearMin={min_year}&releaseYearMax={max_year}&genre={genre}&page={page}"
        headers = {'User-Agent': random.choice(user_agents_list)}
        response = requests.get(METACRITIC_GENRE_URL, headers=headers)
        soups = BeautifulSoup(response.content, 'html.parser')
        result = soups.find(id="__layout")
        metaTitles = result.find_all("div", class_="c-finderProductCard_title")
        metaScores = result.find_all("div", class_="c-siteReviewScore u-flexbox-column u-flexbox-alignCenter u-flexbox-justifyCenter g-text-bold c-siteReviewScore_green g-color-gray90 c-siteReviewScore_xsmall")
        metaYears = result.find_all("span", class_="u-text-uppercase")
        movies = [{'title': metaTitle.text.strip(), 'score': metaScore.text.strip(), 'year': metaYear.text.strip()}
                  for metaTitle, metaScore, metaYear in zip(metaTitles, metaScores, metaYears)]

    random_movie = random.choice(movies) if movies else None

    return render_template('random_results.html', movie=random_movie)

@app.route('/metacritic', methods=['GET', 'POST'])
def scrape_metacritic():
    genre = request.args.get('genre')
    min_year = request.args.get('min_year')
    max_year = request.args.get('max_year')
    page = int(request.args.get('page', 1))

    METACRITIC_GENRE_URL = f"https://www.metacritic.com/browse/movie/all/{genre}/all-time/metascore/?releaseYearMin={min_year}&releaseYearMax={max_year}&genre={genre}&page={page}"

    response = requests.get(METACRITIC_GENRE_URL, headers={'User-Agent': random.choice(user_agents_list)})
    soup = BeautifulSoup(response.content, 'html.parser')

    results = soup.find(id="__layout")

    if results:
        metaTitles = results.find_all("div", class_="c-finderProductCard_title")
        metaScores = results.find_all("div", class_="c-siteReviewScore u-flexbox-column u-flexbox-alignCenter u-flexbox-justifyCenter g-text-bold c-siteReviewScore_green g-color-gray90 c-siteReviewScore_xsmall")
        metaYears = results.find_all("span", class_="u-text-uppercase")

        if len(metaTitles) == len(metaScores) == len(metaYears):
            movies = [{'title': metaTitle.text.strip(), 'score': metaScore.text.strip(), 'year': metaYear.text.strip()}
                      for metaTitle, metaScore, metaYear in zip(metaTitles, metaScores, metaYears)]
        else:
            print("Mismatch in number of titles, scores, and years.")
            return "Mismatch in the number of movies, scores, and years scraped."

        if not movies:
            return "No movies found or incorrect selectors used. Please check the HTML structure."

        next_page = page + 1 if len(movies) == 24 else None  
        prev_page = page - 1 if page > 1 else None

        return render_template('metacritic_results.html', movies=movies, next_page=next_page, prev_page=prev_page, genre=genre, min_year=min_year, max_year=max_year)
    else:
        return "Failed to parse Metacritic page structure or no data found."

@app.route('/rotten-tomato', methods=['GET', 'POST'])
def scrape_rotten_tomato():
    page = int(request.args.get('page', 1))  
    response = requests.get(ROTTEN_TOMATO_TOP_URL, headers={'User-Agent': random.choice(user_agents_list)})
    soup = BeautifulSoup(response.content, 'html.parser')

    results = soup.find(id="article_main_body")

    if results:
        titles = results.find_all("a", class_="title")
        scores = results.find_all("span", class_="score")
        years = results.find_all("span", class_="year")

        all_movies = [{'title': title.text.strip(), 'score': score.text.strip(), 'year': year.text.strip()}
                      for title, score, year in zip(titles, scores, years)]

        per_page = 20
        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        paginated_movies = all_movies[start_index:end_index]

        next_page = page + 1 if end_index < len(all_movies) else None
        prev_page = page - 1 if start_index > 0 else None

        return render_template('rotten_results.html', movies=paginated_movies, next_page=next_page, prev_page=prev_page)
    else:
        return "No results found or an error occurred while scraping."

if __name__ == "__main__":
    app.run(debug=True)
