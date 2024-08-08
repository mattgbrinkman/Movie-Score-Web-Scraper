import requests
from bs4 import BeautifulSoup
import pandas as pd
from aiohttp import ClientSession
from db_secrets import secrets 
from sqlalchemy import create_engine
from asyncio import gather

class Extract:

    def movie_titles(self):
        link = "https://www.fandango.com/movies-in-theaters"
        r = requests.get(link)
        soup = BeautifulSoup(r.text, "html.parser")
        poster_cards = soup.findAll('li', {'class': 'poster-card poster-card__fluid browse-movielist--item dark__section'})
        movie_dict = {}
        for card in poster_cards:
            title_spans = card.find('span', {'class': 'sr-only'})
            title = title_spans.text.split('(')[0].strip()
            movie_dict[title] = {'IMDBscore' : 0, 'RTscore': 0}

        return movie_dict
    
    async def scores(self, movie_title, movie_dict):
        text = movie_title.replace(" ", "+")
        link = f"https://www.google.com/search?q={text}+review"
        async with ClientSession() as session:
            html = await self.fetch(session, link)
            soup = BeautifulSoup(html, "html.parser")
            scores = soup.find_all('span', {'class': 'oqSTJd'})
            for score in scores:
                if (scores.index(score) > 3):
                    continue
                elif (self.get_score_type(score.text) == "RT"):
                    movie_dict[movie_title]['RTscore'] = float(score.text.replace('%', '').strip())
                    print(score.text)
                elif (self.get_score_type(score.text) == "IMDB"):
                    result = score.text.split("/")
                    score = (float(result[0])/int(result[1])) * 100
                    movie_dict[movie_title]['IMDBscore'] = round(score, 1) 

    def get_score_type(self, score):
        if '%' in score:
            return "RT"
        elif ('/10' in score):
            return "IMDB"

    
    async def fetch(self, session, url):
        async with session.get(url) as response:
            return await response.text()
    
    async def get_scores_tasks(self, movie_dict):
        tasks = [self.scores(movie, movie_dict) for movie in movie_dict.keys()]
        await gather(*tasks)
        return movie_dict
        
class Transform:
    def transform_data(self, movie_dict):
        df_reset = pd.DataFrame.from_dict(movie_dict, orient='index').reset_index()
        df_reset.dropna(subset=['RTscore', 'IMDBscore'])
        df_reset.rename(columns={'index': 'MovieTitle'}, inplace=True)

        return df_reset
    
class Load:
    def insert_to_db(self, df):
        db_name = "MovieDB"
        db_user = secrets.get('DATABASE_USER')
        db_password = secrets.get('DATABASE_PASSWORD')
        db_port = secrets.get('DATABASE_PORT')
        db_host = 'localhost'
        engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
        df.to_sql('reviews', engine, if_exists='replace', index=False)
