import traceback
from lanews.utils import create_folders
from loggers import logger
from robocorp.tasks import task
from config import search_phrase, no_of_months
from lanews.scrapper import LANewsExtractor
from constants import FOLDER_NAME, IMAGES_FOLDER_NAME
from selenium.common.exceptions import WebDriverException, NoSuchFrameException, StaleElementReferenceException


@task
def execute_task():
    """
    Executes a news extraction task using the LANewsExtractor class with the provided parameters.

    The function attempts to create an instance of LANewsExtractor with the given search phrase,
    stop period, and topic. It then executes the task. If an exception occurs, it logs an error message
    and prints the traceback. Finally, it logs a success message.

    """
    try:
        create_folders(FOLDER_NAME, IMAGES_FOLDER_NAME)
        news = LANewsExtractor(search_string=search_phrase, stop_period=no_of_months)
        news.execute_task()
    except (WebDriverException, NoSuchFrameException, StaleElementReferenceException) as e:
        logger.error("exception raised")
        traceback.print_exc()
    except Exception as e:
        logger.error("Exception raised")
        traceback.print_exc()
    finally:
        logger.info("Executed successfully")
