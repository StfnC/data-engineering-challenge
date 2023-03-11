import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet
from pandas import DataFrame


# Inspired by: https://www.freecodecamp.org/news/scraping-wikipedia-articles-with-python/
class MuseumScraper:
    MUSEUMS_URL = "https://en.wikipedia.org/wiki/List_of_most-visited_museums"

    def __init__(self) -> None:
        self.__get_page_data()

    def __get_page_data(self):
        response = requests.get(url=MuseumScraper.MUSEUMS_URL)

        self.soup: BeautifulSoup = BeautifulSoup(
            response.content, "html.parser")

    def create_museums_list(self, year: int = 2019):
        table = self.__find_year_table(year)

        table_data = []

        for row in table:
            table_data.append(self.__extract_relevant_data_from_row(row))

        df = DataFrame(table_data)

        print(df)

        return df

    # FIXME: Add type hinting
    def __extract_relevant_data_from_row(self, row):
        # TODO: Extract the data from the row
        return {"a": "b"}

    def __find_year_table(self, year: int = 2019) -> ResultSet:
        year_span = self.soup.find(id=str(year))

        if not year_span:
            return None

        return year_span.parent.next_sibling.next_sibling.find_all("tr")


if __name__ == "__main__":
    scraper = MuseumScraper()

    scraper.create_museums_list()
