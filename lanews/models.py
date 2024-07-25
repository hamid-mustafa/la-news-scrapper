from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Optional

from loggers import logger


@dataclass
class News:
    """
    A class to represent news data.

    Attributes:
        title (str): The title of the news article.
        description (str): The description or content of the news article.
        date (str | None): The publication date of the news article.
        contains_money (bool): A flag indicating whether a certain amount of data exists.
        string_count (int): The count of a specific string within the title and description.
        image (str | None): The file path to the saved image, or None if not available.
    """
    title: str
    description: str
    date: Optional[str]
    contains_money: bool
    string_count: int
    image: Optional[str]

    @staticmethod
    def news_rows(results: list) -> list:
        """
        Transforms a list of News objects into a list of lists containing selected attributes.

        Args:
            results (list): A list of News objects.

        Returns:
            list: A list of lists, where each inner list contains the title, description, date,
                  image_path, amount_exist, and string_count attributes of a News object.
        """
        try:
            return list(map(lambda row: [v for k, v in asdict(row).items()], results))
        except Exception as e:
            logger.error(f"Failed to transform news rows: {e}")
            return []
