import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet
from pandas import DataFrame
from typing import Callable

from constants import DEFAULT_YEAR, MUSEUMS_FOLDER

# FIXME: Add error handling
# Inspired by: https://www.freecodecamp.org/news/scraping-wikipedia-articles-with-python/


class MuseumScraper:
    WIKI_BASE_URL = "https://en.wikipedia.org"
    MUSEUMS_PATH = "/wiki/List_of_most-visited_museums"

    def __init__(self) -> None:
        self.__country_codes = {}

        self.__get_museum_page_data()

    def __get_museum_page_data(self) -> None:
        response = requests.get(
            url=MuseumScraper.WIKI_BASE_URL + MuseumScraper.MUSEUMS_PATH)

        self.soup: BeautifulSoup = BeautifulSoup(
            response.content, "html.parser")

    def create_museums_list(self, year: int = DEFAULT_YEAR) -> DataFrame:
        table = self.__find_year_table(year)

        clean_table_data = []

        for row in table:
            clean_table_data.append(self.__extract_relevant_data_from_row(row))

        df = DataFrame(clean_table_data)

        df.to_csv(f"{MUSEUMS_FOLDER}{year}.csv", index=False)

        return df

    # FIXME: Add type hinting
    def __extract_relevant_data_from_row(self, row):
        row_data = {}

        museum_name_table_data = row.td

        row_data["name"] = museum_name_table_data.a.text

        location_table_data = museum_name_table_data.next_sibling.next_sibling

        country_name = location_table_data.span.a["title"]

        row_data["country_name"] = country_name

        row_data["country"] = self.__get_country_code(country_name)

        row_data["city"] = location_table_data.find_all("a")[-1].text

        visits_table_data = location_table_data.next_sibling.next_sibling

        visits_text = visits_table_data.text.split("[")[0]

        visits = int("".join(visits_text.split(",")))

        row_data["visits"] = visits

        return row_data

    def __get_country_code(self, country: str) -> str:
        if country in self.__country_codes:
            return self.__country_codes[country]

        country_slug = country.replace(" ", "_")

        response = requests.get(
            url=f"{MuseumScraper.WIKI_BASE_URL}/wiki/{country_slug}")

        soup = BeautifulSoup(response.content, "html.parser")

        string_contains_iso_norm: Callable[[
            str], bool] = lambda s: s and s.startswith("ISO 3166-2:")

        country_code = soup.find(
            name="a", attrs={"title": string_contains_iso_norm}).text.lower()

        self.__country_codes[country] = country_code

        return self.__country_codes[country]

    # FIXME: Add comment explaining the way the page is structured
    def __find_year_table(self, year: int = DEFAULT_YEAR) -> ResultSet:
        year_span = self.soup.find(id=str(year))

        if not year_span:
            return None

        return year_span.parent.next_sibling.next_sibling.find_all("tr")[1:]


if __name__ == "__main__":
    scraper = MuseumScraper()

    scraper.create_museums_list()
