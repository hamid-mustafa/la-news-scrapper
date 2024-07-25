from dataclasses import fields
from typing import List, Optional

from RPA.Excel.Files import Files
from selenium.common import NoSuchElementException, TimeoutException, NoSuchFrameException
from selenium.webdriver.common.keys import Keys
from RPA.Browser.Selenium import Selenium, By
from selenium.webdriver.remote.webelement import WebElement

from constants import BASE_URL, FOLDER_NAME
from lanews.decorators import retry
from lanews.exceptions import StopExtraction
from lanews.utils import date_parser
from lanews.xpath import xpaths
from lanews.models import News
from lanews.utils import amount_exist, string_count, download_image_by_url, archive_and_remove_folder, is_date_reached
from loggers import logger


class LANewsExtractor:
    """
    A class to extract news from the LA Times website based on a search string and a specified topic.

    Attributes:
        search_string (str): The search term used to find relevant news articles.
        stop_period (int): The period (in days) at which the extraction process will stop.
    """

    def __init__(self, search_string: str, stop_period: int) -> None:
        self.browser: Selenium = Selenium()
        self.stop_extracting: bool = False
        self.search_string: str = search_string
        self.stop_period: int = stop_period
        self.records: List = []
        self.excel_file: Files = Files()

    def open_browser_and_search_news(self) -> None:
        """
        Opens the LA Times website and searches for news articles using the search string.
        """
        try:
            self.browser.open_available_browser(BASE_URL)
            logger.info("Browser opened")

            self.browser.wait_until_element_is_visible(xpaths["SEARCH_BUTTON_LOCATOR"])
            self.browser.click_button_when_visible(xpaths["SEARCH_BUTTON_LOCATOR"])
            logger.info("Search button clicked")

            self.browser.wait_until_element_is_visible(
                xpaths["SEARCH_FIELD_LOCATOR"], timeout=30
            )
            logger.info("Search field is visible now")

            self.browser.input_text(xpaths["SEARCH_FIELD_LOCATOR"], self.search_string)
            self.browser.press_key(xpaths["SEARCH_FIELD_LOCATOR"], Keys.ENTER)
            logger.info("Search string searched")

        except (AssertionError, NoSuchElementException, TimeoutException) as e:
            logger.error(f"Unable to open browser and search string due to {e}")

    def select_category_and_sort_recent_news(self) -> None:
        """
        Selects the specified category and sorts news articles by the most recent.
        """
        try:
            self.browser.click_element(xpaths["CHOOSE_CATEGORY_LOCATOR"])
            logger.info("Category selected")

            self.browser.wait_until_element_is_visible(xpaths["SORT_NEWS_LOCATOR"], timeout=20)
            self.browser.click_element(xpaths["SORT_NEWS_LOCATOR"])
            self.browser.click_element(xpaths["CHOOSE_NEWEST_LOCATOR"])
            logger.info("Most recent news selected")

            self.browser.wait_until_element_is_visible(xpaths['LOADING_LOCATOR'], timeout=20)
            logger.info("Loading locator found.")

        except (AssertionError, NoSuchElementException, TimeoutException) as e:
            logger.error(f"Unable to select category and sort due to {e}")

    def get_news_date(self, element: WebElement) -> Optional[str]:
        """
        Retrieves and parses the date of a news article from a web element.
        :return: it returns date of the news objects
        """
        try:
            news_date = element.find_element(By.XPATH, xpaths["DATE_LOCATOR"])
        except NoSuchElementException:
            return None

        story_date = date_parser(self.browser.get_text(news_date))
        return story_date

    def get_news_image_src(self, element: WebElement) -> Optional[str]:
        """
        Retrieves the image source URL of a news article from a web element.
        :return: it returns image of the news objects
        """
        try:
            news_image = element.find_element(By.XPATH, xpaths["IMAGE_LOCATOR"])
        except NoSuchElementException:
            return None

        image_src = self.browser.get_element_attribute(news_image, 'src')
        return image_src

    def get_news_elements(self) -> List[WebElement]:
        """
        Retrieves a list of web elements representing news articles.
        :return: returns all the news objects available on the current page
        """
        self.browser.wait_until_element_is_visible(xpaths["ELEMENTS_LOCATOR"], timeout=30)
        return self.browser.find_elements(xpaths["ELEMENTS_LOCATOR"])

    def get_last_page(self) -> int:
        """
        Retrieves the number of the last page of search results.
        :return: returns total pages for the news
        """
        page_text = self.browser.get_text(xpaths["LAST_PAGE_LOCATOR"])
        last_page = page_text.split(" of ")[-1]
        return int(last_page.replace(',', ''))

    def extract_news_from_elements(self, elements: List[WebElement]) -> None:
        """
        Extracts news data from a list of web elements.
        :param elements: News object elements
        """
        for element_index, element in enumerate(elements, start=1):
            news_story_date = self.get_news_date(element)
            stop_extracting = is_date_reached(news_story_date, self.stop_period)
            if stop_extracting:
                # Stopping the process because date limit reached.
                raise StopExtraction
            news_title = element.find_element(By.XPATH, xpaths["TITLE_LOCATOR"])
            news_description = element.find_element(By.XPATH, xpaths["DESCRIPTION_LOCATOR"])
            image_src = self.get_news_image_src(element)
            title = self.browser.get_text(news_title)
            description = self.browser.get_text(news_description)
            exist_amount = any([amount_exist(title), amount_exist(description)])

            self.records.append(
                News(
                    title=title,
                    description=description,
                    date=news_story_date,
                    contains_money=exist_amount,
                    image=image_src,
                    string_count=string_count(title, description, self.search_string),
                )
            )
        logger.info("Extracted Successfully")

    def log_entries_in_excel(
            self,
            file_name: str = "extracted_data.xlsx",
            sheet_name: str = "Election News Data"
    ) -> None:
        """
        Logs the extracted news data into an Excel file.
        :param file_name: Name of Excel file
        :param sheet_name: Name of sheet in the Excel file
        """
        self.excel_file.create_workbook(f'{FOLDER_NAME}/{file_name}')
        self.excel_file.create_worksheet(sheet_name)
        headers = [str(field.name).title().replace("_", " ") for field in fields(News)]
        self.excel_file.append_rows_to_worksheet([headers], name=sheet_name)

        results = self.records
        rows = News.news_rows(results)
        self.excel_file.append_rows_to_worksheet(rows)
        self.excel_file.save_workbook()
        logger.info("Excel file created successfully")

    def download_images(self) -> None:
        """
        Downloads images from the extracted news articles.
        :return:
        """
        for obj_index, obj in enumerate(self.records, start=0):
            url_image = obj.image
            if url_image:
                obj.image = download_image_by_url(url_image, obj_index)
        archive_and_remove_folder()
        logger.info("Images are downloaded successfully")

    @retry(retries=2)
    def extract_news_from_all_pages(self) -> None:
        """
        Extracts news data from subsequent pages until the specified last page.
        :return:
        """
        try:
            elements = self.get_news_elements()
            logger.info("Got news elements")

            self.extract_news_from_elements(elements)
            logger.info("News has been extracted")

            self.browser.wait_until_element_is_visible(xpaths["NEXT_PAGE_LOCATOR"], timeout=10)
            self.browser.click_element(xpaths["NEXT_PAGE_LOCATOR"])

            self.extract_news_from_all_pages()

        except StopExtraction:
            logger.info("Stopping to scrap because date limit reached.")
        except NoSuchFrameException as e:
            logger.info(f"Elements not found {e}")

    def execute_task(self) -> None:
        """
        Executes the entire news extraction process, from opening the browser to logging data in an Excel file.
        """
        self.open_browser_and_search_news()
        logger.info("Browser open and searched begin")

        self.select_category_and_sort_recent_news()
        logger.info("Category selected and news are sorted")

        self.extract_news_from_all_pages()
        logger.info("get news from all pages")

        self.download_images()
        logger.info("download images")

        self.log_entries_in_excel()
        logger.info("log entries in the excel file")
