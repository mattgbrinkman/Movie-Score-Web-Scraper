import get_in_theatre_movie_reviews as movie_service
import connect_database as db_service
import asyncio





def main():
    movie_dict = movie_service.get_movie_titles()
    movie_dict2 = asyncio.run(movie_service.run_async(movie_dict))
    df = movie_service.transform_data(movie_dict2)
    db_service.insert_df_to_table(df)
    print("done")


if __name__ == "__main__":
    main()