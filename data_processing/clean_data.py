#data_preprocessing/clean_data.py
import pandas as pd
import numpy as np


def clean_data(df: pd.DataFrame) -> dict:
    """
    Cleans dataset and returns cleaned dataframe + cleaning summary
    """

    df = df.copy()
    original_shape = df.shape
    summary = {}

    # 1️⃣ Standardize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # 2️⃣ Remove duplicates
    duplicates = df.duplicated().sum()
    df = df.drop_duplicates().reset_index(drop=True)
    summary["duplicates_removed"] = int(duplicates)

    # 3️⃣ Handle missing values
    missing_before = df.isnull().sum().sum()

    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            median_value = df[col].median()
            if pd.isna(median_value):
                median_value = 0
            df[col] = df[col].fillna(median_value)
        else:
            df[col] = df[col].fillna("unknown")

    missing_after = df.isnull().sum().sum()
    summary["missing_values_filled"] = int(missing_before - missing_after)

    # 4️⃣ Outlier handling (IQR - combined mask)
    outliers_removed = 0
    numeric_cols = df.select_dtypes(include=np.number).columns

    mask = pd.Series(True, index=df.index)

    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        col_mask = (df[col] >= lower) & (df[col] <= upper)
        removed = (~col_mask).sum()
        outliers_removed += removed

        mask &= col_mask

    df = df.loc[mask].reset_index(drop=True)

    summary["outliers_removed"] = int(outliers_removed)
    summary["original_shape"] = original_shape
    summary["final_shape"] = df.shape

    return {
        "status": "success",
        "cleaned_df": df,
        "summary": summary
    }
