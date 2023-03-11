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

        clean_table_data = []

        for row in table:
            clean_table_data.append(self.__extract_relevant_data_from_row(row))

        df = DataFrame(clean_table_data)

        df.to_csv(f"museum_visits/{year}.csv", index=False)

        return df

    # FIXME: Add type hinting
    def __extract_relevant_data_from_row(self, row):
        row_data = {}

        museum_name_table_data = row.td

        row_data["name"] = museum_name_table_data.a.text

        location_table_data = museum_name_table_data.next_sibling.next_sibling

        row_data["country"] = location_table_data.span.a["title"]

        row_data["city"] = location_table_data.find_all("a")[-1].text

        visits_table_data = location_table_data.next_sibling.next_sibling

        visits_text = visits_table_data.text.split("[")[0]

        visits = int("".join(visits_text.split(",")))

        row_data["visits"] = visits

        return row_data

    # FIXME: Add comment explaining the way the page is structured
    def __find_year_table(self, year: int = 2019) -> ResultSet:
        year_span = self.soup.find(id=str(year))

        if not year_span:
            return None

        return year_span.parent.next_sibling.next_sibling.find_all("tr")[1:]


if __name__ == "__main__":
    scraper = MuseumScraper()

    scraper.create_museums_list()
