import os

import pandas as pd

from constants import DEFAULT_MIN_VISITORS, DEFAULT_YEAR, MUSEUMS_FOLDER
from museum_scraper import MuseumScraper


class DataPreprocessor:
    def __init__(self, year: int = DEFAULT_YEAR, min_visits: int = DEFAULT_MIN_VISITORS) -> None:
        self.__year = year
        self.__min_visits = min_visits

    # TODO: Create an Abstract GroupingStrategy class to be able
    #  to add new strategies and change them on the fly without changing DataPreprocessor
    def get_population_and_visits(self, grouping_strategy: str = "average") -> pd.DataFrame:
        '''
        Load museum data 
        Remove museums with less than min_visits
        Group museums in the same city by one of the following strategies:
            Average
                Take the average of the museum visits
            Sum
                Add all the museum visits
        Join the museum visits and the population based on the city and country
        Return only the columns required for the linear regression: ['population', 'visitors']
        '''
        museums_df = self.__get_museums_dataframe()

        museums_df = museums_df.loc[museums_df["visits"] > self.__min_visits]

        print(museums_df)

    def __get_museums_dataframe(self) -> pd.DataFrame:
        museums_file_path = f"{MUSEUMS_FOLDER}{self.__year}.csv"

        museums_df = None

        if os.path.isfile(museums_file_path):
            museums_df = pd.read_csv(museums_file_path)
        else:
            scraper = MuseumScraper()
            museums_df = scraper.create_museums_list(self.__year)

        return museums_df


if __name__ == "__main__":
    data_preprocessor = DataPreprocessor()

    data_preprocessor.get_population_and_visits()
