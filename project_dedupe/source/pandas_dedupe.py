import numpy as np
import pandas as pd

from sklearn.impute import SimpleImputer


def handle_missing_values(
    df, method="mean", fill_value=None, numeric_columns=None
) -> pd.DataFrame:
    """
    Reusable function to handle missing values`
    """
    if method == "drop":
        return df.dropna()
    elif method == "fill":
        return df.fillna(fill_value)
    elif method == "mean":
        categorical_columns = []
        for c in df.columns:
            if c not in numeric_columns:
                categorical_columns.append(c)

        # create two DataFrames, one for each data type
        data_numeric = df[numeric_columns]
        print(data_numeric)
        data_categorical = pd.DataFrame(df[categorical_columns])

        imp = SimpleImputer(missing_values=np.nan, strategy="mean")
        data_numeric = pd.DataFrame(
            imp.fit_transform(data_numeric),
            columns=data_numeric.columns,
            index=data_numeric.index,
        )  # only apply imputer to numeric columns

        # join the two masked dataframes back together
        data_joined = pd.concat([data_numeric, data_categorical], axis=1)

        # Imputing the data
        print(data_joined)
        return data_joined
    else:
        raise ValueError("Invalid method provided")


def remove_duplicates(df, subset=None) -> pd.DataFrame:
    """
    Remove duplicates based on specific columns
    """
    return df.drop_duplicates(subset=subset)


def transform_data_types(df, col_types) -> pd.DataFrame:
    """
    Define a function to transform data types
    """
    print(df)
    print(col_types)
    for col, dtype in col_types.items():
        df[col] = df[col].astype(dtype)
    return df


def data_cleaning_pipeline(
    df, missing_values_method="mean", fill_value=None, subset=None, col_types=None
):
    """
    Build a complete data cleaning pipeline
    """
    # Handle missing values
    df = handle_missing_values(
        df,
        method=missing_values_method,
        fill_value=fill_value,
        numeric_columns=["Age", "Salary"],
    )

    # Remove duplicates
    df = remove_duplicates(df, subset=subset)

    # Transform data types
    if col_types:
        df = transform_data_types(df, col_types)

    return df


def main() -> None:
    # Example dataset with various issues
    data = {
        "Name": ["Alice", "Bob", None, "Alice"],
        "Age": ["25", None, "30", "22"],
        "Salary": [50000, 60000, None, 50000],
    }

    df = pd.DataFrame(data)

    # Define data types and run the pipeline
    col_types = {"Age": "int", "Salary": "float"}

    cleaned_df = data_cleaning_pipeline(
        df, missing_values_method="mean", subset=["Name"], col_types=col_types
    )
    print(cleaned_df)


if __name__ == "__main__":
    main()
