import get_in_theatre_movie_reviews as movie_service
import connect_database as db_service

movie_titles = movie_service.get_movie_titles()
movie_dict = movie_service.get_scores(movie_titles)
df = movie_service.transform_data(movie_dict)
db_service.insert_df_to_table(df)
