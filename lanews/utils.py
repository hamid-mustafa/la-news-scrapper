import re
import os
import shutil
from typing import Optional

import requests
from urllib.parse import urlparse, parse_qs
from datetime import datetime, timedelta
from dateutil import parser
from dateutil.relativedelta import relativedelta
from constants import IMAGES_FOLDER_NAME
from loggers import logger


def date_parser(date: str) -> Optional[str]:
    """
        Parses a date string into ISO format.

        Args:
            date (str): The date string to parse.

        Returns:
            str: The parsed date in ISO format, or None if parsing fails.
    """
    now = datetime.now()
    if 'min' in date:
        mint = int(date.split(' ')[0])
        return (now - timedelta(minutes=mint)).date().isoformat()
    if 'hour' in date:
        hr = int(date.split(' ')[0])
        return (now - timedelta(hours=hr)).date().isoformat()
    if date.lower() == 'yesterday':
        return (now - timedelta(days=1)).date().isoformat()
    try:
        return parser.parse(date).date().isoformat()
    except (ValueError, OverflowError, TypeError):
        return None


def amount_exist(text: str) -> bool:
    """
        Checks if an amount of money exists in the given text.

        Args:
            text (str): The text to check.

        Returns:
            bool: True if an amount is found, False otherwise.
    """
    # Combine all patterns into a single pattern using alternation (|)
    combined_pattern = r'\$\d+(?:,\d+)*(?:\.\d)?|\d+ dollars|\d+ USD'

    # Search for the combined pattern
    return True if re.search(combined_pattern, text, re.IGNORECASE) else False


def is_date_reached(date: Optional[str], months: int) -> bool:
    """
       Checks if the given date is older than a specified number of months.

       Args:
           date (str): The date to check.
           months (int): The number of months to compare against.

       Returns:
           bool: True if the date is older than the specified number of months, False otherwise.
    """
    if date:
        months = 1 if months == 0 else months
        till_date = datetime.now() - relativedelta(months=months)
        return parser.parse(date) < till_date
    return False


def archive_and_remove_folder() -> None:
    """
        Archives a folder into a zip file and then removes the original folder.
        """
    try:
        shutil.make_archive(IMAGES_FOLDER_NAME, 'zip', IMAGES_FOLDER_NAME)
        logger.info("folder archived")
    except Exception as e:
        logger.warning("folder not archived")
    try:
        shutil.rmtree(IMAGES_FOLDER_NAME)
    except Exception as e:
        logger.warning("folder not removed")


def download_image_by_url(url: str, image_count: int) -> str:
    """
        Downloads an image from a URL and saves it to a specified folder.

        Args:
            url (str): The URL of the image to download.
            image_count (int): A counter to name the downloaded image file.
            folder_name (str): The name of the folder to save the downloaded image.

        Returns:
            str: The path of the downloaded image file.
    """
    try:
        file_name = f"image_{image_count}.jpg"
        response = requests.get(url)
        if response.status_code == 200:
            filename = os.path.join(IMAGES_FOLDER_NAME, file_name)
            with open(filename, "wb") as file:
                file.write(response.content)
            return filename
    except Exception as e:
        logger.warning(f"No file downloaded with {e}")


def string_count(title: str, description: str, search_string: str) -> int:
    """
        Count the occurrences of a search string in both the title and description.

        Args:
            title (str): The title in which to search for the string.
            description (str): The description in which to search for the string.
            search_string (str): The string to search for within the title and description.

        Returns:
            int: The total number of occurrences of the search string in both the title and description.
    """
    return title.count(search_string) + description.count(search_string)


def create_folders(output_folder: str, image_folder: str) -> None:
    """
        Create specified folders if they do not already exist.

        Args:
            output_folder (str): The name of the output folder to be created.
            image_folder (str): The name of the image folder to be created.

        Returns:
            None
    """
    folder = f'{os.getcwd()}/{output_folder}'
    image_folder = f'{os.getcwd()}/{image_folder}'
    if not os.path.exists(folder):
        os.makedirs(folder)
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)
