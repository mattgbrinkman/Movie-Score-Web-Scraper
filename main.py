import get_in_theatre_movie_reviews as movie_service
import asyncio
from pipeline_utils import Extract, Transform, Load



async def get_scores_tasks(movie_titles):
    movie_dict = {key: {} for key in movie_titles}
    tasks = [movie_service.get_scores(movie, movie_dict) for movie in movie_titles]
    await asyncio.gather(*tasks)
    return movie_dict


if __name__ == "__main__":
    # Extract, transform and load data
    try:
        ex = Extract()
        tf = Transform()
        ld = Load()
        titles = Extract.movie_titles(ex)
        movie_dict = asyncio.run(get_scores_tasks(titles))
        df = Transform.transform_data(ld, movie_dict)
        Load.insert_df_to_table(ld, df)

    except Exception as e:
        print('error', e)