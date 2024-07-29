import get_in_theatre_movie_reviews as movie_service
import connect_database as db_service
import asyncio


async def run_async(movie_titles):
    movie_dict = {key: {} for key in movie_titles}
    tasks = [movie_service.get_scores(movie, movie_dict) for movie in movie_titles]
    await asyncio.gather(*tasks)
    return movie_dict


def main():
    movie_titles = movie_service.get_movie_titles()
    movie_dict = asyncio.run(run_async(movie_titles))
    df = movie_service.transform_data(movie_dict)
    db_service.insert_df_to_table(df)
    print("done")


if __name__ == "__main__":
    main()