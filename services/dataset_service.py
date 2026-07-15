"""
Dataset service module.

Coordinates and encapsulates core business logic for file validation, loading,
profiling, and cleaning datasets.
"""

import streamlit as st
from typing import Union, IO, Dict, Any, Optional
import pandas as pd
from analytics.data_loader import load_dataset
from analytics.cleaning import (
    remove_duplicates,
    fill_missing,
    convert_datatypes,
    rename_columns,
    remove_empty_rows,
    detect_missing_values,
    detect_duplicates,
    auto_detect_datatypes,
    generate_cleaning_summary,
)
from analytics.profiling import (
    dataset_summary,
    column_summary,
    missing_report,
    memory_usage,
    unique_values,
    statistics_report,
    auto_profile,
)


class DatasetService:
    """Service class for dataset operations."""

    @staticmethod
    def load_and_validate(
        file_source: Union[str, IO[bytes]], file_name: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Load dataset and validate basic structural rules.

        Args:
            file_source (Union[str, IO[bytes]]): Path or file buffer.
            file_name (Optional[str]): Original filename to resolve extension.

        Returns:
            pd.DataFrame: Validated DataFrame.

        Raises:
            ValueError: If file is empty, corrupted, or invalid.
        """
        df = load_dataset(file_source, file_name)

        if df.empty:
            raise ValueError("The uploaded dataset is empty.")

        # Ensure column names are clean strings
        df.columns = [str(col).strip() for col in df.columns]

        return df

    @staticmethod
    @st.cache_data(hash_funcs={pd.DataFrame: lambda df: (id(df), len(df), list(df.columns))})
    def get_profile(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Extract descriptive statistical profile and metadata of a DataFrame.

        Args:
            df (pd.DataFrame): Dataset.

        Returns:
            Dict[str, Any]: Structure profiles, summaries, and distribution statistics.
        """
        summary = dataset_summary(df)
        cols_summary = column_summary(df)
        missing = missing_report(df)
        stats = statistics_report(df)
        uniques = unique_values(df)

        return {
            "summary": summary,
            "columns": cols_summary,
            "missing": missing,
            "statistics": stats,
            "uniques": uniques,
            "memory_usage_mb": float(summary["memory_bytes"] / (1024 * 1024)),
        }

    @staticmethod
    def clean_dataset(
        df: pd.DataFrame,
        do_remove_duplicates: bool = True,
        fill_missing_cols: Optional[Dict[str, Dict[str, Any]]] = None,
        cast_cols: Optional[Dict[str, str]] = None,
        rename_cols: Optional[Dict[str, str]] = None,
        empty_rows_threshold: Optional[float] = None,
    ) -> pd.DataFrame:
        """
        Apply serial cleaning steps on a DataFrame.

        Args:
            df (pd.DataFrame): Input DataFrame.
            do_remove_duplicates (bool): Remove duplicate rows.
            fill_missing_cols (Optional[Dict[str, Dict[str, Any]]]): e.g., {"ColName": {"strategy": "mean", "val": None}}
            cast_cols (Optional[Dict[str, str]]): e.g., {"ColName": "datetime"}
            rename_cols (Optional[Dict[str, str]]): e.g., {"OldCol": "NewCol"}
            empty_rows_threshold (Optional[float]): Null percentage row drop threshold.

        Returns:
            pd.DataFrame: Cleaned DataFrame.
        """
        processed_df = df.copy()

        # 1. Rename columns
        if rename_cols:
            processed_df = rename_columns(processed_df, rename_cols)

        # 2. Convert datatypes
        if cast_cols:
            for col, dtype in cast_cols.items():
                if col in processed_df.columns:
                    processed_df = convert_datatypes(processed_df, col, dtype)

        # 3. Fill missing
        if fill_missing_cols:
            for col, config in fill_missing_cols.items():
                if col in processed_df.columns:
                    strategy = config.get("strategy", "constant")
                    val = config.get("val")
                    processed_df = fill_missing(
                        processed_df, col, strategy, fill_value=val
                    )

        # 4. Remove duplicates
        if do_remove_duplicates:
            processed_df = remove_duplicates(processed_df)

        # 5. Remove empty rows
        if empty_rows_threshold is not None:
            processed_df = remove_empty_rows(
                processed_df, threshold=empty_rows_threshold
            )

        return processed_df

    @staticmethod
    def detect_missing_values(df: pd.DataFrame) -> Dict[str, Any]:
        """Expose missing values detection."""
        return detect_missing_values(df)

    @staticmethod
    def detect_duplicates(df: pd.DataFrame) -> Dict[str, Any]:
        """Expose duplicates detection."""
        return detect_duplicates(df)

    @staticmethod
    def auto_detect_datatypes(df: pd.DataFrame) -> Dict[str, str]:
        """Expose automatic data type detection."""
        return auto_detect_datatypes(df)

    @staticmethod
    def generate_cleaning_summary(before_df: pd.DataFrame, after_df: pd.DataFrame) -> Dict[str, Any]:
        """Expose basic cleaning summary generation."""
        return generate_cleaning_summary(before_df, after_df)

    @staticmethod
    @st.cache_data(hash_funcs={pd.DataFrame: lambda df: (id(df), len(df), list(df.columns))})
    def auto_profile(df: pd.DataFrame) -> Dict[str, Any]:
        """Expose automatic dataset profiling."""
        return auto_profile(df)
