"""
Dataset Overview Page.

Renders interactive Plotly charts, feature summaries, and profiles
of numerical, categorical, and date variables matching the luxury dark design system.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from components.section_header import render_section_header
from components.empty_state import render_empty_state
from components.metric_card import render_metric_card
from components.table_container import render_table_container
from services.dataset_service import DatasetService


def apply_plotly_theme(fig: go.Figure) -> None:
    """Apply the active theme properties to a Plotly figure."""
    from utils.theme_manager import get_current_theme
    theme_vars = get_current_theme()
    paper_bg = "rgba(0,0,0,0)"
    font_col = theme_vars['text']
    legend_col = theme_vars['subtext']
    grid_col = theme_vars['border']
    zero_col = theme_vars['border']
    axis_col = theme_vars['subtext']

    fig.update_layout(
        paper_bgcolor=paper_bg,
        plot_bgcolor="rgba(0, 0, 0, 0)",
        font_family="Inter, -apple-system, sans-serif",
        font_color=font_col,
        title_font_color=font_col,
        legend_font_color=legend_col,
        margin=dict(l=40, r=40, t=50, b=40),
        xaxis=dict(
            gridcolor=grid_col,
            zerolinecolor=zero_col,
            color=axis_col,
            tickfont=dict(size=10),
            title=dict(font=dict(color=axis_col, size=11)),
        ),
        yaxis=dict(
            gridcolor=grid_col,
            zerolinecolor=zero_col,
            color=axis_col,
            tickfont=dict(size=10),
            title=dict(font=dict(color=axis_col, size=11)),
        ),
    )


def render() -> None:
    """Render the overview workspace."""
    if "dataset" not in st.session_state:
        render_empty_state(
            title="No Dataset Selected",
            message="We couldn't locate an active dataset in memory. Please upload a dataset first.",
            action_label="Go to Upload Workspace",
            navigate_to="upload",
            navigate_label="Upload",
        )
        return

    df = st.session_state["dataset"]
    filename = st.session_state.get("dataset_filename", "dataset.csv")

    render_section_header(
        title="Dataset Overview",
        subtitle=f"Statistical variables and metrics breakdown for {filename}.",
        label="Dataset Profiler",
    )

    # 1. Metric stats
    profile = DatasetService.get_profile(df)
    summary = profile["summary"]
    from utils.theme_manager import get_current_theme
    theme_vars = get_current_theme()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_metric_card(
            value=f"{summary['numeric_cols']}",
            label="Numeric Columns",
            detail="Variables with continuous values",
            icon_svg='<svg viewBox="0 0 24 24"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>',
        )
    with col2:
        render_metric_card(
            value=f"{summary['categorical_cols']}",
            label="Categorical Columns",
            detail="Variables with labels or symbols",
            icon_svg='<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M12 8l-4 8h8l-4-8z"/></svg>',
        )
    with col3:
        render_metric_card(
            value=f"{summary['datetime_cols']}",
            label="Date Columns",
            detail="Variables with timestamps",
            icon_svg='<svg viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>',
        )
    with col4:
        missing_val = summary["missing_cells"]
        missing_pct = summary["missing_pct"]
        render_metric_card(
            value=f"{missing_val:,}",
            label="Missing Values",
            detail="Total empty values across cells",
            trend=f"{missing_pct:.1f}%",
            trend_positive=(missing_val == 0),
            icon_svg='<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>',
        )

    # 2. Charts Section
    st.markdown('<h3 style="margin-top: 2rem; font-weight: 700;">Interactive Explorations</h3>', unsafe_allow_html=True)

    grid_col1, grid_col2 = st.columns(2)

    with grid_col1:
        # Donut Chart - Columns Data Types
        data_types_counts = {
            "Numeric": summary["numeric_cols"],
            "Categorical": summary["categorical_cols"],
            "Date/Time": summary["datetime_cols"],
        }
        labels = [k for k, v in data_types_counts.items() if v > 0]
        values = [v for k, v in data_types_counts.items() if v > 0]

        if values:
            fig_types = px.pie(
                names=labels,
                values=values,
                hole=0.6,
                title="Data Types Distribution",
                color_discrete_sequence=[theme_vars['primary'], theme_vars['accent'], theme_vars['subtext']],
            )
            apply_plotly_theme(fig_types)
            fig_types.update_layout(height=380)
            st.plotly_chart(fig_types, use_container_width=True)
        else:
            st.info("No columns available to plot data types.")

    with grid_col2:
        # Bar Chart - Missing Values per Column
        missing_df = profile["missing"]
        if not missing_df.empty:
            missing_df_reset = missing_df.reset_index().rename(
                columns={"index": "Column", "Missing Count": "Missing Count"}
            )
            fig_missing = px.bar(
                missing_df_reset,
                x="Column",
                y="Missing Count",
                title="Missing Values Count per Column",
                color_discrete_sequence=[theme_vars['primary']],
            )
            apply_plotly_theme(fig_missing)
            fig_missing.update_layout(height=380)
            st.plotly_chart(fig_missing, use_container_width=True)
        else:
            # Render a premium visualization representing complete dataset
            fig_complete = go.Figure(
                go.Indicator(
                    mode="number+gauge",
                    value=100,
                    number={"suffix": "%", "font": {"color": "#10B981"}},
                    title={"text": "Data Completeness Rate", "font": {"color": theme_vars['text']}},
                    gauge={
                        "axis": {"range": [0, 100], "tickcolor": theme_vars['text']},
                        "bar": {"color": "#10B981"},
                        "bgcolor": "rgba(0,0,0,0.02)" if st.session_state.get("theme") == "light" else "rgba(255,255,255,0.02)",
                        "steps": [{"range": [0, 100], "color": "rgba(99,102,241,0.04)"}],
                    },
                )
            )
            apply_plotly_theme(fig_complete)
            fig_complete.update_layout(height=380)
            st.plotly_chart(fig_complete, use_container_width=True)

    # 3. Distributions & Correlation Row
    grid_col3, grid_col4 = st.columns(2)

    with grid_col3:
        # Numeric Feature Distribution Selector
        numeric_cols = df.loc[:, ~df.isna().all()].select_dtypes(include=[np.number]).columns.tolist()
        if numeric_cols:
            selected_num = st.selectbox(
                "Select Numeric Variable to Plot Distribution", numeric_cols
            )
            fig_dist = px.histogram(
                df,
                x=selected_num,
                marginal="box",
                title=f"Distribution of {selected_num}",
                color_discrete_sequence=[theme_vars['primary']],
            )
            apply_plotly_theme(fig_dist)
            fig_dist.update_layout(height=380)
            st.plotly_chart(fig_dist, use_container_width=True)
        else:
            st.info("No numerical features found for distributions.")

    with grid_col4:
        # Categorical Feature Frequency Selector
        categorical_cols = df.loc[:, ~df.isna().all()].select_dtypes(
            include=["object", "category", "bool"]
        ).columns.tolist()
        if categorical_cols:
            selected_cat = st.selectbox(
                "Select Categorical Variable to Plot Frequency", categorical_cols
            )
            counts = df[selected_cat].value_counts().reset_index()
            counts.columns = [selected_cat, "Frequency"]
            # Show top 15 categories for readability
            counts_top = counts.head(15)

            fig_freq = px.bar(
                counts_top,
                x="Frequency",
                y=selected_cat,
                orientation="h",
                title=f"Top Categories in {selected_cat}",
                color_discrete_sequence=[theme_vars['accent']],
            )
            fig_freq.update_layout(yaxis=dict(autorange="reversed"), height=380)
            apply_plotly_theme(fig_freq)
            st.plotly_chart(fig_freq, use_container_width=True)
        else:
            st.info("No categorical features found for frequencies.")

    # 4. Correlation Heatmap (Full width card)
    numeric_df = df.loc[:, ~df.isna().all()].select_dtypes(include=[np.number])
    if len(numeric_df.columns) > 1:
        st.markdown('<h4 style="margin-top: 2rem; font-weight: 700;">Correlation Matrix</h4>', unsafe_allow_html=True)
        corr = numeric_df.corr()

        fig_heat = px.imshow(
            corr,
            x=corr.columns,
            y=corr.columns,
            color_continuous_scale=[
                [0.0, theme_vars['primary']],
                [0.5, theme_vars['bg']],
                [1.0, theme_vars['accent']],
            ],
            aspect="auto",
            title="Pearson Correlation Heatmap",
        )
        apply_plotly_theme(fig_heat)
        fig_heat.update_layout(height=450)
        st.plotly_chart(fig_heat, use_container_width=True)
    elif len(numeric_df.columns) == 1:
        st.info("Correlation heatmap requires at least two numerical columns. Only one numerical column detected.")
    else:
        st.info("No numerical columns found. Correlation analysis skipped.")

    # 5. Numerical Descriptive Summary Table
    if not profile["statistics"].empty:
        st.markdown('<h4 style="margin-top: 2rem; font-weight: 700;">Descriptive Statistics</h4>', unsafe_allow_html=True)
        render_table_container(profile["statistics"], max_height_px=350)


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    try:
        with open("styles/theme.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass
    render()
