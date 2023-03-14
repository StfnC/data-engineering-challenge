from constants import DEFAULT_MIN_VISITORS, DEFAULT_YEAR


class DataPreprocessor:
    def __init__(self, year: int = DEFAULT_YEAR, min_visits: int = DEFAULT_MIN_VISITORS) -> None:
        self.__year = year
        self.__min_visits = min_visits

    # TODO: Create an Abstract GroupingStrategy class to be able
    #  to add new strategies and change them on the fly without changing DataPreprocessor
    def get_population_and_visits(self, grouping_strategy: str):
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
        pass
