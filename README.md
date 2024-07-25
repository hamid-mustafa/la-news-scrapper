# README

## Overview

The code provides an implementation for extracting news articles from the LA Times website based on a search string. The extracted news data, including titles, descriptions, dates, image URLs, and other attributes, are stored and processed. The final data is logged into an Excel file, and associated images are downloaded and archived.

## Features

- **News Extraction**: Extracts news articles from the LA Times based on a specified search string.
- **Data Logging**: Logs extracted data into an Excel file.
- **Image Downloading**: Downloads and archives images associated with the news articles.
- **Date Filtering**: Filters news articles based on a stop period.

## Components

### Classes

#### News
A data class that represents a news article with attributes such as title, description, date, etc.

**Attributes**:
- `title`: The title of the news article.
- `description`: The description or content of the news article.
- `date`: The publication date of the news article.
- `amount_exist`: A flag indicating whether a certain amount of data exists.
- `image_src`: The source URL of the news article's image.
- `string_count`: The count of a specific string within the title and description.
- `image_path`: The file path to the saved image, or None if not available.

#### LANewsExtractor
A class to extract news from the LA Times website based on a search string and a specified topic.

**Attributes**:
- `search_string`: The search term used to find relevant news articles.
- `stop_period`: The period (in days) at which the extraction process will stop.
- `browser`: An instance of the Selenium web browser automation tool.
- `stop_extracting`: A flag to indicate whether the extraction process should stop.
- `folder_name`: The name of the folder where output files will be saved.
- `images_folder_name`: The name of the folder where images will be saved.
- `records`: A list to store extracted news data.
- `excel_file`: An instance of the RPA Excel Files library to handle Excel operations.

### Methods

#### LANewsExtractor Methods
- `open_browser_and_search_news`: Opens the LA Times website and searches for news articles using the search string.
- `select_category_and_sort_recent_news`: Selects the specified category and sorts news articles by the most recent.
- `get_news_title`, `get_news_description`, `get_news_date`, `get_news_image_src`: Retrieve respective attributes of a news article from a web element.
- `get_objects`, `get_next_page_objects`: Retrieves a list of web elements representing news articles.
- `get_last_page`: Retrieves the number of the last page of search results.
- `extract_news_from_elements`: Extracts news data from a list of web elements.
- `log_entries_in_excel`: Logs the extracted news data into an Excel file.
- `download_images`: Downloads images from the extracted news articles.
- `extract_news_from_next_pages`: Extracts news data from subsequent pages until the specified last page.
- `execute_task`: Executes the entire news extraction process.

### Utility Functions
- `url_parser`: Parses the query parameters from a URL.
- `date_parser`: Parses a date string into ISO format.
- `amount_exist`: Checks if an amount of money exists in the given text.
- `is_date_reached`: Checks if the given date is older than a specified number of months.
- `archive_and_remove_folder`: Archives a folder into a zip file and then removes the original folder.
- `download_image_by_url`: Downloads an image from a URL and saves it to a specified folder.
- `string_count`: Counts the occurrences of a search string in both the title and description.
- `create_folders`: Creates specified folders if they do not already exist.

### Configuration

- **XPaths**: Various XPaths used to locate elements on the LA Times website.
- **Logger**: Configures the logging format and level for the application.

### Execution

- The `execute_task` function initializes the `LANewsExtractor` with the provided parameters and executes the task. It handles exceptions and logs relevant messages.

## Requirements

- `rpaframework==28.6.0`
- `robocorp==1.4.0`
- `Selenium`
- `dateutil`
- `requests`

## Usage

1. **Setup**: Ensure all dependencies are installed.
2. **Configuration**: Configure the search string and stop period in the `config` module.
3. **Execution**: Run the `execute_task` function to start the news extraction process.

## Logging

The application logs messages at various stages of execution to provide insights and track the progress and any issues encountered.
