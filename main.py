from asyncio import run
from pipeline_utils import Extract, Transform, Load

if __name__ == "__main__":
    # Extract, transform and load data
    try:
        ex = Extract()
        tf = Transform()
        ld = Load()
        movie_dict = Extract.movie_titles(ex)
        result = run(ex.get_scores_tasks(movie_dict))
        df = Transform.transform_data(ld, movie_dict)
        Load.insert_to_db(ld, df)

    except Exception as e:
        print('error', e)