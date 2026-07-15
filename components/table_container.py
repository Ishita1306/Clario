"""
Table container component.

Renders pandas DataFrames as high-fidelity, scrollable HTML tables conforming
to the luxury dark design system.
"""

import pandas as pd
import streamlit as st


def render_table_container(
    df: pd.DataFrame, max_height_px: int = 400, index: bool = False
) -> None:
    """
    Render a pandas DataFrame inside a premium styled, scrollable table container.

    Args:
        df (pd.DataFrame): Dataframe to visualize.
        max_height_px (int): Vertical height cap for scrollbar.
        index (bool): Show dataframe index column.
    """
    import textwrap
    table_css = textwrap.dedent(
        """
        <style>
            .table-wrapper {
                width: 100%;
                overflow-x: auto;
                border-radius: 8px;
                border: 1px solid var(--border);
                background: var(--glass);
                margin: 1rem 0 2rem;
            }
            .premium-table {
                width: 100%;
                border-collapse: collapse;
                font-size: 0.85rem;
                color: var(--text);
                text-align: left;
            }
            .premium-table th {
                background: var(--surface);
                padding: 0.85rem 1.15rem;
                font-weight: 600;
                font-size: 0.78rem;
                letter-spacing: 0.05em;
                text-transform: uppercase;
                color: var(--subtext);
                border-bottom: 1px solid var(--border);
                position: sticky;
                top: 0;
                z-index: 10;
            }
            .premium-table td {
                padding: 0.85rem 1.15rem;
                border-bottom: 1px solid var(--border);
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
                max-width: 250px;
            }
            .premium-table tbody tr:hover {
                background: rgba(99, 102, 241, 0.05);
            }
            .premium-table tbody tr:last-child td {
                border-bottom: none;
            }
        </style>
        """
    ).strip()
    st.markdown(table_css, unsafe_allow_html=True)

    # Convert DataFrame to premium styled HTML
    html_table = df.to_html(
        index=index,
        classes="premium-table",
        escape=True,
        border=0,
    )

    scrollable_container = textwrap.dedent(
        f"""
        <div class="table-wrapper" style="max-height: {max_height_px}px;">
            {html_table}
        </div>
        """
    ).strip()
    st.markdown(scrollable_container, unsafe_allow_html=True)
