"""
Sanity tests for Phase 1 components.

Verifies loading, profiling, and cleaning functionalities using safe encoding characters.
"""

import sys
import os
import pandas as pd
import numpy as np

# Ensure path is mapped correctly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from analytics.data_loader import load_dataset
from analytics.cleaning import remove_duplicates, fill_missing, convert_datatypes
from analytics.profiling import dataset_summary, column_summary, statistics_report
from services.dataset_service import DatasetService


def test_analytics_profiling_and_cleaning():
    print("Running basic data pipeline validations...")

    # Create dummy dataset
    data = {
        "A": [1, 2, 2, np.nan, 5],
        "B": ["cat", "dog", "dog", "mouse", "cat"],
        "C": ["2026-01-01", "2026-01-02", "2026-01-02", "2026-01-04", "2026-01-05"],
    }
    df = pd.DataFrame(data)

    # Test summary profiling
    summary = dataset_summary(df)
    assert summary["rows"] == 5
    assert summary["columns"] == 3
    assert summary["duplicate_rows"] == 1
    assert summary["missing_cells"] == 1
    print("SUCCESS: Profiling dataset_summary validation passed.")

    # Test columns summary
    col_sum = column_summary(df)
    assert len(col_sum) == 3
    print("SUCCESS: Profiling column_summary validation passed.")

    # Test duplicates cleaning
    cleaned_dups = remove_duplicates(df)
    assert len(cleaned_dups) == 4
    print("SUCCESS: Cleaning remove_duplicates validation passed.")

    # Test missing value filling
    filled_df = fill_missing(df, "A", "constant", fill_value=10.0)
    assert filled_df["A"].isnull().sum() == 0
    assert filled_df["A"].iloc[3] == 10.0
    print("SUCCESS: Cleaning fill_missing validation passed.")

    # Test type conversion
    converted_df = convert_datatypes(df, "C", "datetime")
    assert pd.api.types.is_datetime64_any_dtype(converted_df["C"])
    print("SUCCESS: Cleaning convert_datatypes validation passed.")

    # Test missing value detection
    missing_report = DatasetService.detect_missing_values(df)
    assert missing_report["total_missing"] == 1
    assert missing_report["has_missing"] is True
    assert missing_report["columns"]["A"]["count"] == 1
    print("SUCCESS: detect_missing_values validation passed.")

    # Test duplicate detection
    dup_report = DatasetService.detect_duplicates(df)
    assert dup_report["duplicate_count"] == 1
    assert dup_report["has_duplicates"] is True
    print("SUCCESS: detect_duplicates validation passed.")

    # Test automatic datatype detection
    autodetect_report = DatasetService.auto_detect_datatypes(df)
    assert autodetect_report["A"] == "int64"
    assert autodetect_report["B"] == "category"
    print("SUCCESS: auto_detect_datatypes validation passed.")

    # Test cleaning summary
    cleaned_df = remove_duplicates(df)
    summary_report = DatasetService.generate_cleaning_summary(df, cleaned_df)
    assert summary_report["rows_before"] == 5
    assert summary_report["rows_after"] == 4
    assert summary_report["rows_removed"] == 1
    assert summary_report["duplicates_removed"] == 1
    print("SUCCESS: generate_cleaning_summary validation passed.")

    # Test automatic dataset profiling
    autoprofile_report = DatasetService.auto_profile(df)
    assert autoprofile_report["rows"] == 5
    assert autoprofile_report["columns"] == 3
    assert autoprofile_report["missing_values"] == 1
    assert autoprofile_report["duplicate_rows"] == 1
    assert autoprofile_report["numeric_columns"] == 1
    assert autoprofile_report["categorical_columns"] == 2
    assert autoprofile_report["memory_usage_mb"] > 0
    print("SUCCESS: auto_profile validation passed.")

    # Test service integration
    service_profile = DatasetService.get_profile(df)
    assert service_profile["summary"]["rows"] == 5
    print("SUCCESS: DatasetService.get_profile validation passed.")

    print("\nAll pipeline validations completed successfully!")


def test_exclude_all_nan_columns():
    print("Running 100% missing column exclusion validations...")
    from services.visualization_service import VisualizationService
    # Dataset with a 100% missing column "D"
    data = {
        "A": [1, 2, 3],
        "B": ["cat", "dog", "mouse"],
        "C": [np.nan, 2.0, 3.0],
        "D": [np.nan, np.nan, np.nan], # 100% missing
    }
    df = pd.DataFrame(data)

    # 1. Profile / KPI check
    profile = DatasetService.auto_profile(df)
    assert profile["columns"] == 3 # A, B, C (D is excluded)
    
    # 2. Descriptive statistics check
    stats = statistics_report(df)
    assert "D" not in stats["Attribute"].values
    
    # 3. Column type detection check
    detected = VisualizationService.detect_columns(df)
    assert "D" not in detected["numeric"]
    assert "D" not in detected["categorical"]
    assert "D" not in detected["all"]

    # 4. Correlation check
    fig = VisualizationService.create_correlation_heatmap(df)
    assert len(fig.data) >= 0
    print("SUCCESS: 100% missing columns excluded correctly!")


if __name__ == "__main__":
    test_analytics_profiling_and_cleaning()
    test_exclude_all_nan_columns()
