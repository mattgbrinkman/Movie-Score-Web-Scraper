from asyncio import run
from pipeline_utils import Extract, Transform, Load
from logging_config import SingletonLogger

logger = SingletonLogger.get_instance().get_logger()

if __name__ == "__main__":
    try:
        logger.info("Starting Program")
        ex = Extract()
        movie_dict = Extract.movie_titles(ex)
        result = run(ex.get_scores_tasks(movie_dict))
        
        tf = Transform()
        df = Transform.transform_data(tf, movie_dict)

        ld = Load()
        Load.insert_to_db(ld, df)

    except Exception as e:
        logger.debug("Error: ", e)