"""
Data cleaning module.

Provides pure functions for cleaning Pandas DataFrames (removing duplicates,
handling missing values, converting datatypes, and renaming columns).
"""

from typing import Union, Dict, Any, List, Optional
import pandas as pd


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate rows from a DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    return df.drop_duplicates().reset_index(drop=True)


def fill_missing(
    df: pd.DataFrame,
    column: str,
    strategy: str,
    fill_value: Optional[Any] = None,
) -> pd.DataFrame:
    """
    Fill missing values in a specific column of a DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame.
        column (str): Column name to fill missing values in.
        strategy (str): Strategy to use ('mean', 'median', 'mode', 'constant', 'drop').
        fill_value (Optional[Any]): Constant value to fill if strategy is 'constant'.

    Returns:
        pd.DataFrame: DataFrame with missing values filled or dropped.
    """
    new_df = df.copy()

    if strategy == "mean":
        mean_val = new_df[column].mean()
        new_df[column] = new_df[column].fillna(mean_val)
    elif strategy == "median":
        median_val = new_df[column].median()
        new_df[column] = new_df[column].fillna(median_val)
    elif strategy == "mode":
        if not new_df[column].mode().empty:
            mode_val = new_df[column].mode()[0]
            new_df[column] = new_df[column].fillna(mode_val)
    elif strategy == "constant":
        if fill_value is not None:
            new_df[column] = new_df[column].fillna(fill_value)
    elif strategy == "drop":
        new_df = new_df.dropna(subset=[column]).reset_index(drop=True)

    return new_df


def convert_datatypes(
    df: pd.DataFrame, column: str, datatype: str
) -> pd.DataFrame:
    """
    Convert a specific column's data type.

    Args:
        df (pd.DataFrame): Input DataFrame.
        column (str): Column name.
        datatype (str): Target datatype ('int64', 'float64', 'str', 'datetime', 'category').

    Returns:
        pd.DataFrame: DataFrame with modified column datatype.
    """
    new_df = df.copy()

    if datatype == "datetime":
        new_df[column] = pd.to_datetime(new_df[column], errors="coerce")
    elif datatype in {"int64", "float64"}:
        new_df[column] = pd.to_numeric(new_df[column], errors="coerce")
        new_df[column] = new_df[column].astype(datatype)
    else:
        new_df[column] = new_df[column].astype(datatype)

    return new_df


def rename_columns(df: pd.DataFrame, columns_dict: Dict[str, str]) -> pd.DataFrame:
    """
    Rename columns based on a dictionary mapping old names to new names.

    Args:
        df (pd.DataFrame): Input DataFrame.
        columns_dict (Dict[str, str]): Dict mapping {"old_col_name": "new_col_name"}.

    Returns:
        pd.DataFrame: DataFrame with columns renamed.
    """
    return df.rename(columns=columns_dict)


def remove_empty_rows(
    df: pd.DataFrame, threshold: float = 0.5
) -> pd.DataFrame:
    """
    Remove rows where the percentage of missing values exceeds a threshold.

    Args:
        df (pd.DataFrame): Input DataFrame.
        threshold (float): Percentage threshold of missing data (0.0 to 1.0) to drop a row.
                           Default is 0.5 (drop row if 50% or more fields are null).

    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    new_df = df.copy()
    limit = int((1 - threshold) * len(new_df.columns))
    return new_df.dropna(thresh=limit).reset_index(drop=True)


def detect_missing_values(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Detect missing values per column in a DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        Dict[str, Any]: Missing statistics containing column details and total counts.
    """
    missing_counts = df.isnull().sum().to_dict()
    total_missing = int(df.isnull().sum().sum())
    missing_pct = {col: float(val / len(df) * 100) if len(df) > 0 else 0.0 for col, val in missing_counts.items()}
    return {
        "columns": {col: {"count": int(missing_counts[col]), "percentage": missing_pct[col]} for col in df.columns},
        "total_missing": total_missing,
        "has_missing": total_missing > 0
    }


def detect_duplicates(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Detect duplicate rows in a DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        Dict[str, Any]: Duplicate statistics.
    """
    duplicate_count = int(df.duplicated().sum())
    duplicate_pct = float(duplicate_count / len(df) * 100) if len(df) > 0 else 0.0
    return {
        "duplicate_count": duplicate_count,
        "duplicate_percentage": duplicate_pct,
        "has_duplicates": duplicate_count > 0
    }


def auto_detect_datatypes(df: pd.DataFrame) -> Dict[str, str]:
    """
    Automatically detect suggested data types for columns.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        Dict[str, str]: Suggested data types for each column name.
    """
    detected = {}
    for col in df.columns:
        col_series = df[col].dropna()
        if col_series.empty:
            detected[col] = str(df[col].dtype)
            continue
        
        # 1. Try Numeric detection
        try:
            parsed_num = pd.to_numeric(col_series, errors="raise")
            # If all float values are integer-like, suggest int64
            if all(parsed_num.astype(float) % 1 == 0):
                detected[col] = "int64"
            else:
                detected[col] = "float64"
            continue
        except (ValueError, TypeError):
            pass
        
        # 2. Try Datetime detection (using a sample of first 15 values for speed)
        try:
            sample = col_series.head(15)
            pd.to_datetime(sample, errors="raise")
            detected[col] = "datetime64[ns]"
            continue
        except (ValueError, TypeError):
            pass
        
        # 3. Try Categorical detection (based on unique value cardinality percentage)
        unique_count = col_series.nunique()
        if unique_count > 0 and (unique_count < 10 or (unique_count / len(df)) < 0.15):
            detected[col] = "category"
        else:
            detected[col] = "object"
            
    return detected


def generate_cleaning_summary(before_df: pd.DataFrame, after_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Generate a basic summary of changes before and after cleaning.

    Args:
        before_df (pd.DataFrame): Raw DataFrame before cleaning.
        after_df (pd.DataFrame): Cleaned DataFrame.

    Returns:
        Dict[str, Any]: Summary metrics comparing the two states.
    """
    rows_removed = len(before_df) - len(after_df)
    duplicates_removed = int(before_df.duplicated().sum() - after_df.duplicated().sum())
    
    # Track any column datatype changes
    changed_dtypes = {}
    for col in before_df.columns:
        if col in after_df.columns:
            before_type = str(before_df[col].dtype)
            after_type = str(after_df[col].dtype)
            if before_type != after_type:
                changed_dtypes[col] = {"from": before_type, "to": after_type}
                
    before_missing = int(before_df.isnull().sum().sum())
    after_missing = int(after_df.isnull().sum().sum())
    missing_filled = before_missing - after_missing
    
    return {
        "rows_before": len(before_df),
        "rows_after": len(after_df),
        "rows_removed": rows_removed,
        "duplicates_removed": duplicates_removed,
        "missing_before": before_missing,
        "missing_after": after_missing,
        "missing_filled": missing_filled,
        "changed_datatypes": changed_dtypes
    }
