import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_movie_titles():
    link = "https://www.fandango.com/movies-in-theaters"
    r = requests.get(link)
    soup = BeautifulSoup(r.text, "html.parser")
    poster_cards = soup.findAll('li', {'class': 'poster-card poster-card__fluid browse-movielist--item dark__section'})
    movie_titles = []
    for card in poster_cards:
        title_spans = card.find('span', {'class': 'sr-only'})
        movie_titles.append(title_spans.text.split('(')[0].strip())

    return movie_titles

def get_scores(movie_titles):
    movie_dict = {key: {} for key in movie_titles}
    for movie in movie_titles:
        text = movie.replace(" ", "+")
        link = f"https://www.google.com/search?q={text}+review"
        r = requests.get(link)
        soup = BeautifulSoup(r.text, "html.parser")
        scores = soup.find_all('span', {'class': 'oqSTJd'})
        for score in scores:
            if (scores.index(score) > 3):
                continue
            elif (get_score_type(score.text) == "RT"):
                movie_dict[movie]['RTscore'] = float(score.text.replace('%', '').strip())
                print(score.text)
            elif (get_score_type(score.text) == "IMDB"):
                result = score.text.split("/")
                score = (float(result[0])/int(result[1])) * 100
                movie_dict[movie]['IMDBscore'] = round(score, 1)

    return movie_dict  


def transform_data(movie_dict):
    df_reset = pd.DataFrame.from_dict(movie_dict, orient='index').reset_index()
    df_reset.dropna(subset=['RTscore', 'IMDBscore'])
    df_reset.rename(columns={'index': 'MovieTitle'}, inplace=True)

    return df_reset
        
def get_score_type(score):
    if '%' in score:
        return "RT"
    elif ('/10' in score):
        return "IMDB"