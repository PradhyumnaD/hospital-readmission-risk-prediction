import numpy as np
import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_is_fitted


class RareCategoryGrouper(BaseEstimator, TransformerMixin):
    """
    Converts categorical values to strings and groups categories
    occurring fewer than min_frequency times into __RARE__.

    Categories not observed during fitting are also mapped to
    the rare-category label during transformation.
    """

    def __init__(
        self,
        min_frequency=10,
        rare_label="__RARE__",
    ):
        self.min_frequency = min_frequency
        self.rare_label = rare_label

    def fit(self, X, y=None):
        X_array = np.asarray(
            X,
            dtype=object,
        ).astype(str)

        if X_array.ndim != 2:
            raise ValueError(
                "RareCategoryGrouper expects a two-dimensional input."
            )

        self.n_features_in_ = X_array.shape[1]
        self.frequent_categories_ = []

        for column_index in range(self.n_features_in_):
            category_counts = pd.Series(
                X_array[:, column_index]
            ).value_counts(dropna=False)

            frequent_categories = set(
                category_counts[
                    category_counts >= self.min_frequency
                ].index.tolist()
            )

            self.frequent_categories_.append(
                frequent_categories
            )

        return self

    def transform(self, X):
        check_is_fitted(
            self,
            attributes=["frequent_categories_"],
        )

        X_array = np.asarray(
            X,
            dtype=object,
        ).astype(str)

        if X_array.ndim != 2:
            raise ValueError(
                "RareCategoryGrouper expects a two-dimensional input."
            )

        if X_array.shape[1] != self.n_features_in_:
            raise ValueError(
                "The number of categorical columns differs "
                "from the fitted data."
            )

        for column_index, frequent_categories in enumerate(
            self.frequent_categories_
        ):
            column_values = X_array[:, column_index]

            frequent_mask = np.fromiter(
                (
                    value in frequent_categories
                    for value in column_values
                ),
                dtype=bool,
                count=len(column_values),
            )

            column_values[~frequent_mask] = self.rare_label
            X_array[:, column_index] = column_values

        return X_array

    def get_feature_names_out(self, input_features=None):
        if input_features is None:
            return np.asarray(
                [
                    f"x{index}"
                    for index in range(self.n_features_in_)
                ],
                dtype=object,
            )

        return np.asarray(
            input_features,
            dtype=object,
        )
        