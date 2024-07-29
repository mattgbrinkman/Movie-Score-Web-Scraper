import requests
from bs4 import BeautifulSoup
import pandas as pd
import aiohttp
import asyncio

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

async def get_scores(movie_title, movie_dict):
    text = movie_title.replace(" ", "+")
    link = f"https://www.google.com/search?q={text}+review"
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, link)
        soup = BeautifulSoup(html, "html.parser")
        scores = soup.find_all('span', {'class': 'oqSTJd'})
        for score in scores:
            if (scores.index(score) > 3):
                continue
            elif (get_score_type(score.text) == "RT"):
                movie_dict[movie_title]['RTscore'] = float(score.text.replace('%', '').strip())
                print(score.text)
            elif (get_score_type(score.text) == "IMDB"):
                result = score.text.split("/")
                score = (float(result[0])/int(result[1])) * 100
                movie_dict[movie_title]['IMDBscore'] = round(score, 1) 


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

    
async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()