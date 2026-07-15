"""
Upload Service.

Handles filesystem storage, file type validation, and pandas parsing for CSV and XLSX files.
"""

import os
import pandas as pd
from typing import Tuple

class UploadService:
    UPLOAD_DIR = "data/uploads"

    @classmethod
    def ensure_upload_dir(cls) -> None:
        """Ensure the upload directory exists."""
        os.makedirs(cls.UPLOAD_DIR, exist_ok=True)

    @classmethod
    def process_upload(cls, uploaded_file) -> Tuple[pd.DataFrame, str]:
        """
        Process the uploaded file:
        1. Validate filename extension (CSV, XLSX)
        2. Save a copy of the file inside data/uploads/
        3. Read the file into a pandas DataFrame
        4. Validate that the dataset is not empty
        
        Returns:
            Tuple[pd.DataFrame, str]: (DataFrame, saved_file_path)
            
        Raises:
            ValueError: for unsupported, empty, corrupted, or failed files.
        """
        cls.ensure_upload_dir()
        
        filename = uploaded_file.name
        ext = os.path.splitext(filename.lower())[1]
        
        if ext not in [".csv", ".xlsx"]:
            raise ValueError(f"Unsupported file format '{ext}'. Only CSV and XLSX are supported.")
            
        # Save file to data/uploads/
        saved_path = os.path.join(cls.UPLOAD_DIR, filename)
        try:
            uploaded_file.seek(0)
            with open(saved_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
        except Exception as e:
            raise ValueError(f"Failed to save uploaded file to disk: {str(e)}")
            
        # Read the file using pandas
        try:
            uploaded_file.seek(0)
            if ext == ".csv":
                df = pd.read_csv(saved_path)
            else:
                df = pd.read_excel(saved_path)
        except Exception as e:
            raise ValueError(f"Corrupted or invalid file. Could not parse tabular data: {str(e)}")
            
        if df.empty:
            raise ValueError("The uploaded dataset is empty (contains no data rows).")
            
        # Clean column names
        df.columns = [str(col).strip() for col in df.columns]
        
        return df, saved_path
