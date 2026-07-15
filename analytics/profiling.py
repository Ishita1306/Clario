"""
Dataset profiling module.

Provides pure functions to profile datasets and extract structural metadata,
missing statistics, unique value counts, and descriptive summaries.
"""

from typing import Dict, Any
import numpy as np
import pandas as pd


def dataset_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Generate a high-level summary of the dataset's structural characteristics.

    Args:
        df (pd.DataFrame): Dataframe to analyze.

    Returns:
        Dict[str, Any]: Summary stats (rows, columns, duplicates, missing cells, data types).
    """
    # Exclude columns that are 100% missing (all NaN)
    df_valid = df.loc[:, ~df.isna().all()]

    total_cells = int(df_valid.size)
    missing_cells = int(df_valid.isnull().sum().sum())
    missing_pct = float(missing_cells / total_cells * 100) if total_cells > 0 else 0.0
    duplicate_rows = int(df_valid.duplicated().sum())

    # Count of data types
    num_cols = len(df_valid.select_dtypes(include=[np.number]).columns)
    date_cols = len(df_valid.select_dtypes(include=[np.datetime64, "datetime64[ns]"]).columns)
    cat_cols = len(df_valid.select_dtypes(include=["object", "category", "bool"]).columns)

    return {
        "rows": len(df),
        "columns": len(df_valid.columns),
        "total_cells": total_cells,
        "missing_cells": missing_cells,
        "missing_pct": missing_pct,
        "duplicate_rows": duplicate_rows,
        "numeric_cols": num_cols,
        "datetime_cols": date_cols,
        "categorical_cols": cat_cols,
        "memory_bytes": int(df_valid.memory_usage(deep=True).sum()),
    }


def column_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate summary statistics for every column in the dataset.

    Args:
        df (pd.DataFrame): Dataframe to analyze.

    Returns:
        pd.DataFrame: Table detailing data type, non-null counts, missing value percent, and unique counts.
    """
    records = []
    for col in df.columns:
        dtype = str(df[col].dtype)
        non_null_count = int(df[col].count())
        missing_count = int(df[col].isnull().sum())
        missing_pct = (
            float(missing_count / len(df) * 100) if len(df) > 0 else 0.0
        )
        unique_count = int(df[col].nunique())

        # Safely fetch sample value
        sample_series = df[col].dropna()
        sample_val = str(sample_series.iloc[0]) if not sample_series.empty else "N/A"

        records.append(
            {
                "Column Name": col,
                "Data Type": dtype,
                "Non-Null Count": non_null_count,
                "Missing Count": missing_count,
                "Missing %": f"{missing_pct:.2f}%",
                "Unique Values": unique_count,
                "Sample Value": sample_val,
            }
        )

    return pd.DataFrame(records)


def missing_report(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract a breakdown of missing values per column.

    Args:
        df (pd.DataFrame): Dataframe to analyze.

    Returns:
        pd.DataFrame: Columns with missing counts and percentages, sorted descending.
    """
    missing_count = df.isnull().sum()
    missing_pct = (df.isnull().sum() / len(df)) * 100
    report = pd.DataFrame(
        {
            "Missing Count": missing_count,
            "Missing %": missing_pct,
        }
    )
    return report[report["Missing Count"] > 0].sort_values(
        by="Missing Count", ascending=False
    )


def memory_usage(df: pd.DataFrame) -> float:
    """
    Calculate the total deep memory footprint of a DataFrame in megabytes (MB).

    Args:
        df (pd.DataFrame): Dataframe.

    Returns:
        float: Size in Megabytes.
    """
    bytes_size = df.memory_usage(deep=True).sum()
    return float(bytes_size / (1024 * 1024))


def unique_values(df: pd.DataFrame) -> Dict[str, int]:
    """
    Calculate unique counts for all columns.

    Args:
        df (pd.DataFrame): Dataframe.

    Returns:
        Dict[str, int]: Columns and their distinct value counts.
    """
    return df.nunique().to_dict()


def statistics_report(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate comprehensive numerical descriptions for numeric attributes.

    Args:
        df (pd.DataFrame): Dataframe.

    Returns:
        pd.DataFrame: Descriptive statistics (count, mean, std, min, percentiles, max).
    """
    # Exclude columns that are 100% missing (all NaN)
    df_valid = df.loc[:, ~df.isna().all()]
    numeric_df = df_valid.select_dtypes(include=[np.number])
    if numeric_df.empty:
        return pd.DataFrame()
    stats = numeric_df.describe().transpose()
    # Reset index to include column name as a standard attribute
    stats = stats.reset_index().rename(columns={"index": "Attribute"})
    return stats


def auto_profile(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Automatically generate structural and storage profiling metrics for a dataset.

    Args:
        df (pd.DataFrame): Input dataset.

    Returns:
        Dict[str, Any]: Profiling metrics containing rows, columns, missing values,
                        duplicates, numeric/categorical column counts, and memory usage.
    """
    # Exclude columns that are 100% missing (all NaN)
    df_valid = df.loc[:, ~df.isna().all()]

    rows = len(df)
    columns = len(df_valid.columns)
    missing_values = int(df_valid.isnull().sum().sum())
    duplicate_rows = int(df_valid.duplicated().sum())
    numeric_cols = len(df_valid.select_dtypes(include=[np.number]).columns)
    categorical_cols = len(df_valid.select_dtypes(include=["object", "category", "bool"]).columns)
    
    # Memory footprint in MB
    memory_bytes = int(df_valid.memory_usage(deep=True).sum())
    memory_usage_mb = float(memory_bytes / (1024 * 1024))
    
    return {
        "rows": rows,
        "columns": columns,
        "missing_values": missing_values,
        "duplicate_rows": duplicate_rows,
        "numeric_columns": numeric_cols,
        "categorical_columns": categorical_cols,
        "memory_usage_mb": memory_usage_mb,
    }
