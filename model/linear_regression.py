import matplotlib.pyplot as plt

from data_preprocessor import DataPreprocessor
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.metrics import r2_score

from grouping_strategy import GroupingStrategy


class VisitorInfluxLinearModel:
    # Based on https://scikit-learn.org/stable/auto_examples/linear_model/plot_ols.html
    def perform_linear_regression(self, year: int = 2019):
        data_preprocessor = DataPreprocessor(year=year)

        data = data_preprocessor.get_population_and_visits(grouping_strategy=GroupingStrategy.SUM)

        population = data["population"].values

        visits = data["visits"].values

        X_train, X_test = train_test_split(population, test_size=0.5)

        Y_train, Y_test = train_test_split(visits, test_size=0.5)

        model = linear_model.LinearRegression()

        model.fit(X_train.reshape(-1, 1), Y_train)

        predictions = model.predict(X_test.reshape(-1, 1))

        print(f"R^2: {r2_score(Y_test, predictions)}")

        plt.scatter(population, visits, color="green")

        plt.scatter(X_test, Y_test, color="black")
        plt.plot(X_test, predictions, color="red")

        plt.xticks(())
        plt.yticks(())

        plt.show()


if __name__ == "__main__":
    model = VisitorInfluxLinearModel()

    model.perform_linear_regression()
