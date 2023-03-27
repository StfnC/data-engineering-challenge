import os

import pandas as pd

from constants import CITIES_FOLDER, DEFAULT_MIN_VISITORS, DEFAULT_YEAR, MUSEUMS_FOLDER
from grouping_strategy import GroupingStrategy
from museum_scraper import MuseumScraper


class DataPreprocessor:
    def __init__(self, year: int = DEFAULT_YEAR, min_visits: int = DEFAULT_MIN_VISITORS) -> None:
        self.__year = year
        self.__min_visits = min_visits

    def get_population_and_visits(self, grouping_strategy: GroupingStrategy = GroupingStrategy.AVERAGE) -> pd.DataFrame:
        self.__grouping_strategy = grouping_strategy

        museums_df = self.__get_museums_dataframe()

        museums_df = museums_df.loc[museums_df["visits"] > self.__min_visits]

        museums_grouped_by_city = self.__group_by_city(museums_df)

        city_populations = self.__get_city_populations()

        city_populations = city_populations.rename(
            columns={'City': 'city', 'Country': 'country', 'Population': 'population'})

        museums_grouped_by_city['city'] = museums_grouped_by_city['city'].apply(
            lambda city: city.lower())

        grouped_data = pd.merge(museums_grouped_by_city,
                                city_populations, on=['city', 'country'])

        return grouped_data[['city', 'country', 'visits', 'population']]

    def __get_museums_dataframe(self) -> pd.DataFrame:
        museums_file_path = f"{MUSEUMS_FOLDER}{self.__year}.csv"

        museums_df = None

        if os.path.isfile(museums_file_path):
            museums_df = pd.read_csv(museums_file_path)
        else:
            scraper = MuseumScraper()
            museums_df = scraper.create_museums_list(self.__year)

        return museums_df

    # TODO: Create an Abstract GroupingStrategy class to be able
    #  to add new strategies and change them on the fly without changing DataPreprocessor
    def __group_by_city(self, museums: pd.DataFrame) -> pd.DataFrame:
        museums_grouped_by_city = museums.groupby(
            ["country", "city"], as_index=False)

        if self.__grouping_strategy == GroupingStrategy.AVERAGE:
            museums_grouped_by_city = museums_grouped_by_city.mean()
        elif self.__grouping_strategy == GroupingStrategy.SUM:
            museums_grouped_by_city = museums_grouped_by_city.sum()

        return museums_grouped_by_city

    def __get_city_populations(self) -> pd.DataFrame:
        world_cities_path = f"{CITIES_FOLDER}worldcitiespop.csv"

        if not os.path.isfile(world_cities_path):
            # FIXME: Maybe raise an exception?
            print("Please download the world cities population dataset at https://www.kaggle.com/max-mind/world-cities-database")
            return None

        dtypes = {
            "Country": "string",
            "City": "string",
            "AccentCity": "string",
            "Population": float
        }

        city_populations = pd.read_csv(world_cities_path, dtype=dtypes, usecols=[
                                       "Country", "City", "AccentCity", "Population"])

        city_populations = city_populations[city_populations["Population"].notna(
        )]

        return city_populations


if __name__ == "__main__":
    data_preprocessor = DataPreprocessor()

    data_preprocessor.get_population_and_visits()
