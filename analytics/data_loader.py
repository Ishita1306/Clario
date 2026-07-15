"""
Data loader module.

Responsible for reading datasets from different formats (CSV, XLSX)
into Pandas DataFrames, handling encodings and sheets safely.
"""

from typing import Union, IO, Optional
import os
import pandas as pd


def load_dataset(
    file_source: Union[str, IO[bytes]], file_name: Optional[str] = None
) -> pd.DataFrame:
    """
    Load a dataset from a file path or a binary file buffer.

    Args:
        file_source (Union[str, IO[bytes]]): The file path or file-like object containing data.
        file_name (Optional[str]): Original filename to detect extension when file_source is a buffer.

    Returns:
        pd.DataFrame: Loaded DataFrame.

    Raises:
        ValueError: If file type is unsupported or corrupted.
    """
    # Determine the extension
    ext = ""
    if isinstance(file_source, str):
        ext = os.path.splitext(file_source)[1].lower()
        if not os.path.exists(file_source):
            raise ValueError(f"The file '{file_source}' does not exist.")
        if os.path.getsize(file_source) == 0:
            raise ValueError("The specified file is empty (0 bytes).")
    elif file_name:
        ext = os.path.splitext(file_name)[1].lower()
        if hasattr(file_source, "seek") and hasattr(file_source, "tell"):
            file_source.seek(0, 2)
            size = file_source.tell()
            file_source.seek(0)
            if size == 0:
                raise ValueError("The uploaded file is empty (0 bytes).")

    if ext == ".csv":
        try:
            # Attempt default UTF-8 first, fallback to ISO-8859-1 on failure
            if isinstance(file_source, str):
                df = pd.read_csv(file_source)
            else:
                try:
                    file_source.seek(0)
                    df = pd.read_csv(file_source, encoding="utf-8")
                except UnicodeDecodeError:
                    file_source.seek(0)
                    df = pd.read_csv(file_source, encoding="latin1")
            
            if df.empty:
                raise ValueError("The uploaded dataset contains no rows or data.")
            return df
        except Exception as e:
            if isinstance(e, ValueError):
                raise e
            raise ValueError(f"Failed to parse CSV file: {str(e)}")

    elif ext in {".xlsx", ".xls"}:
        try:
            if isinstance(file_source, str):
                df = pd.read_excel(file_source)
            else:
                file_source.seek(0)
                df = pd.read_excel(file_source)
            
            if df.empty:
                raise ValueError("The uploaded dataset contains no rows or data.")
            return df
        except Exception as e:
            if isinstance(e, ValueError):
                raise e
            raise ValueError(f"Failed to parse Excel file: {str(e)}")

    else:
        raise ValueError(
            f"Unsupported file format '{ext}'. Only CSV and Excel (.xlsx, .xls) are supported."
        )
