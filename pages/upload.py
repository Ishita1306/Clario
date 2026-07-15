"""
Dataset upload page workspace.

Provides interactive controls to upload CSV and Excel (XLSX) datasets, profiles
them, and displays KPI cards and summaries matching the premium dark theme.
"""

import io
import streamlit as st
import pandas as pd

from components.section_header import render_section_header
from components.empty_state import render_empty_state
from components.metric_card import render_metric_card
from components.table_container import render_table_container
from components.glass_card import glass_card_wrapper_start, glass_card_wrapper_end
from services.dataset_service import DatasetService


def format_memory_size(bytes_size: int) -> str:
    """Format size in bytes to a human-readable string."""
    if bytes_size < 1024:
        return f"{bytes_size} B"
    elif bytes_size < 1024 * 1024:
        return f"{bytes_size / 1024:.2f} KB"
    else:
        return f"{bytes_size / (1024 * 1024):.2f} MB"


def render() -> None:
    """Render the upload workspace."""
    render_section_header(
        title="Upload Dataset",
        subtitle="Import your CSV or Excel spreadsheets to profile, clean, and analyze your business data.",
        label="Data Workspace",
    )

    # File uploader workspace styled inside a card
    with st.container(border=True):
        uploaded_file = st.file_uploader(
            "Choose a data file",
            type=["csv", "xlsx", "xls"],
            help="Supported formats: CSV, Excel (.xlsx, .xls). File size limits up to 200MB.",
            label_visibility="collapsed",
        )

    # Process upload if file is provided
    if uploaded_file is not None:
        try:
            # Read file buffer and save DataFrame to state
            df = DatasetService.load_and_validate(
                uploaded_file, uploaded_file.name
            )
            st.session_state["dataset"] = df
            st.session_state["dataset_filename"] = uploaded_file.name
        except Exception as e:
            st.error(f"Failed to load dataset: {str(e)}")

    # Retrieve dataset from session state
    if "dataset" in st.session_state:
        df = st.session_state["dataset"]
        filename = st.session_state.get("dataset_filename", "dataset.csv")

        # Get profile stats
        profile = DatasetService.get_profile(df)
        summary = profile["summary"]

        st.success(f"Successfully loaded {filename}")

        # Metrics section (6 columns grid)
        col1, col2, col3, col4, col5, col6 = st.columns(6)

        with col1:
            render_metric_card(
                value=f"{summary['rows']:,}",
                label="Rows",
                detail="Total data samples",
                icon_svg='<svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><line x1="9" y1="3" x2="9" y2="21"/><line x1="15" y1="3" x2="15" y2="21"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="3" y1="15" x2="21" y2="15"/></svg>',
            )
        with col2:
            render_metric_card(
                value=str(summary["columns"]),
                label="Columns",
                detail="Total variables",
                icon_svg='<svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><line x1="21" y1="12" x2="3" y2="12"/><line x1="12" y1="3" x2="12" y2="21"/></svg>',
            )
        with col3:
            # Color trend positive/negative based on missing values presence
            missing_val = summary["missing_cells"]
            missing_pct = summary["missing_pct"]
            render_metric_card(
                value=f"{missing_val:,}",
                label="Missing",
                detail=f"{missing_pct:.1f}% of total dataset",
                trend=f"{missing_pct:.1f}%",
                trend_positive=(missing_val == 0),
                icon_svg='<svg viewBox="0 0 24 24"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
            )
        with col4:
            dups = summary["duplicate_rows"]
            render_metric_card(
                value=f"{dups:,}",
                label="Duplicates",
                detail="Redundant rows",
                trend=str(dups),
                trend_positive=(dups == 0),
                icon_svg='<svg viewBox="0 0 24 24"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>',
            )
        with col5:
            # Format dataset size (in-memory footprint)
            formatted_mem = format_memory_size(summary["memory_bytes"])
            render_metric_card(
                value=formatted_mem,
                label="Dataset Size",
                detail="Raw dataset footprint",
                icon_svg='<svg viewBox="0 0 24 24"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l-7 4a2 2 0 0 0 2 0l7-4a2 2 0 0 0 1-1.73z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>',
            )
        with col6:
            # Memory usage formatted
            mem_mb = profile["memory_usage_mb"]
            render_metric_card(
                value=f"{mem_mb:.2f} MB",
                label="Memory Usage",
                detail="System active RAM",
                icon_svg='<svg viewBox="0 0 24 24"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg>',
            )

        # Tabbed preview workspace
        tab1, tab2, tab3 = st.tabs(
            ["Dataset Preview", "Schema & Types", "Missing Summary"]
        )

        with tab1:
            st.subheader("Data Preview")
            # Show first 15 rows in premium table
            render_table_container(df.head(15), max_height_px=450)

        with tab2:
            st.subheader("Column Metadata")
            # Show column summaries
            render_table_container(profile["columns"], max_height_px=450)

        with tab3:
            st.subheader("Missing Values Breakdown")
            # Show missing report
            missing_df = profile["missing"]
            if not missing_df.empty:
                # Reset index to make column name a visible attribute
                missing_df = missing_df.reset_index().rename(
                    columns={"index": "Column Name"}
                )
                render_table_container(missing_df, max_height_px=450)
            else:
                st.info("No missing values detected in the dataset. Excellent data quality!")

    else:
        render_empty_state(
            title="No Dataset Uploaded",
            message="Please drag and drop your data file above. InsightFlow will display analytics metrics, summaries, and distribution profiles once a file is provided.",
        )


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    # Load external stylesheet if run standalone
    try:
        with open("styles/theme.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass
    render()
