"""
Visualization service module.

Handles auto-detection of suitable dataset columns for plotting, and generates
premium dark-themed Plotly charts for Phase 2 dashboards.
"""

import streamlit as st
from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


class VisualizationService:
    """Service for generating premium, dark-themed interactive visualizations."""

    COLOR_SEQUENCE = ["#6366F1", "#06B6D4", "#8B5CF6", "#3B82F6", "#10B981", "#F59E0B", "#EC4899"]
    DIVERGING_SCALE = [
        [0.0, "#6366F1"],
        [0.5, "#1F2937"],
        [1.0, "#06B6D4"]
    ]

    @classmethod
    def get_theme_colors(cls) -> tuple:
        """Fetch active theme color sequences and scales."""
        from utils.theme_manager import get_current_theme
        theme_vars = get_current_theme()
        seq = [theme_vars['primary'], theme_vars['accent'], "#8B5CF6", "#3B82F6", "#10B981", "#F59E0B", "#EC4899"]
        div = [
            [0.0, theme_vars['primary']],
            [0.5, theme_vars['bg']],
            [1.0, theme_vars['accent']]
        ]
        return seq, div

    @classmethod
    def apply_theme(cls, fig: go.Figure) -> None:
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
            margin=dict(l=50, r=40, t=60, b=50),
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
            scene=dict(
                xaxis=dict(
                    backgroundcolor="rgba(0,0,0,0)",
                    gridcolor=grid_col,
                    color=axis_col
                ),
                yaxis=dict(
                    backgroundcolor="rgba(0,0,0,0)",
                    gridcolor=grid_col,
                    color=axis_col
                ),
                zaxis=dict(
                    backgroundcolor="rgba(0,0,0,0)",
                    gridcolor=grid_col,
                    color=axis_col
                )
            )
        )

    @staticmethod
    @st.cache_data(hash_funcs={pd.DataFrame: lambda df: (id(df), len(df), list(df.columns))})
    def detect_columns(df: pd.DataFrame) -> Dict[str, List[str]]:
        """
        Auto-detect lists of numeric, categorical, and datetime columns.
        Excludes unsuitable ID and high-cardinality textual columns.
        """
        # Exclude columns that are 100% missing (all NaN)
        df_valid = df.loc[:, ~df.isna().all()]
        n_rows = len(df_valid)

        # Numeric columns
        numeric_raw = df_valid.select_dtypes(include=[np.number]).columns.tolist()
        
        # Datetime columns (including objects that can be parsed as dates)
        datetime_cols = df_valid.select_dtypes(include=[np.datetime64, "datetime64[ns]"]).columns.tolist()
        
        # Categorical columns
        categorical_raw = df_valid.select_dtypes(include=["object", "category", "bool"]).columns.tolist()
        
        # Inspect objects to see if they can be candidate dates or categories
        for col in df_valid.select_dtypes(include=["object"]):
            if col in datetime_cols or col in categorical_raw:
                continue
            # Check if it could be a date
            try:
                # If first few elements are date-like
                sample = df_valid[col].dropna().head(5)
                if not sample.empty and pd.to_datetime(sample, errors="raise"):
                    datetime_cols.append(col)
                    continue
            except (ValueError, TypeError):
                pass
            
            # Default to categorical for object columns
            categorical_raw.append(col)

        # Filter out unsuitable columns (constant values, unique IDs, serial keys)
        numeric = []
        for col in numeric_raw:
            col_lower = col.lower()
            uniq_cnt = df_valid[col].nunique()
            if uniq_cnt <= 1:
                continue
            if any(kw in col_lower for kw in ["id", "index", "serial", "key", "pk", "uuid", "guid"]):
                if uniq_cnt >= n_rows * 0.98 and n_rows > 5:
                    continue
            numeric.append(col)

        categorical = []
        for col in categorical_raw:
            col_lower = col.lower()
            uniq_cnt = df_valid[col].nunique()
            if uniq_cnt <= 1:
                continue
            # Exclude unique ID/text fields
            if uniq_cnt > 20 and (uniq_cnt / n_rows > 0.95):
                continue
            if any(kw in col_lower for kw in ["id", "index", "serial", "key", "pk", "uuid", "guid"]):
                if uniq_cnt >= n_rows * 0.98 and n_rows > 5:
                    continue
            categorical.append(col)

        return {
            "numeric": numeric,
            "categorical": categorical,
            "datetime": datetime_cols,
            "all": df_valid.columns.tolist()
        }

    @classmethod
    def sample_if_large(cls, df: pd.DataFrame, max_rows: int = 10000) -> pd.DataFrame:
        """Sample a dataset if it exceeds max_rows to keep browser plotting responsive."""
        if len(df) > max_rows:
            return df.sample(n=max_rows, random_state=42)
        return df

    # 1. Correlation Heatmap
    @classmethod
    def create_correlation_heatmap(cls, df: pd.DataFrame) -> go.Figure:
        # Exclude columns that are 100% missing (all NaN)
        df_valid = df.loc[:, ~df.isna().all()]
        numeric_df = df_valid.select_dtypes(include=[np.number])
        if len(numeric_df.columns) < 2:
            fig = go.Figure()
            fig.update_layout(title="Correlation heatmap requires at least 2 numerical columns.")
            cls.apply_theme(fig)
            return fig

        color_seq, div_scale = cls.get_theme_colors()
        corr = numeric_df.corr()
        fig = px.imshow(
            corr,
            x=corr.columns,
            y=corr.columns,
            color_continuous_scale=div_scale,
            aspect="auto",
            title="Pearson Correlation Matrix",
        )
        cls.apply_theme(fig)
        return fig

    # 2. Histogram
    @classmethod
    def create_histogram(cls, df: pd.DataFrame, column: str, bins: int = 30) -> go.Figure:
        color_seq, _ = cls.get_theme_colors()
        fig = px.histogram(
            df,
            x=column,
            nbins=bins,
            title=f"Distribution of {column}",
            color_discrete_sequence=[color_seq[0]],
        )
        cls.apply_theme(fig)
        fig.update_layout(bargap=0.05)
        return fig

    # 3. Box Plot
    @classmethod
    def create_box_plot(cls, df: pd.DataFrame, y_col: str, x_col: Optional[str] = None) -> go.Figure:
        sampled_df = cls.sample_if_large(df, 20000)
        color_seq, _ = cls.get_theme_colors()
        fig = px.box(
            sampled_df,
            x=x_col,
            y=y_col,
            title=f"Box Plot of {y_col}" + (f" grouped by {x_col}" if x_col else ""),
            color_discrete_sequence=[color_seq[2] if len(color_seq) > 2 else color_seq[0]],
        )
        cls.apply_theme(fig)
        return fig

    # 4. Scatter Plot
    @classmethod
    def create_scatter_plot(
        cls, df: pd.DataFrame, x_col: str, y_col: str, color_col: Optional[str] = None
    ) -> go.Figure:
        sampled_df = cls.sample_if_large(df, 10000)
        color_seq, div_scale = cls.get_theme_colors()
        fig = px.scatter(
            sampled_df,
            x=x_col,
            y=y_col,
            color=color_col,
            title=f"Scatter Plot: {x_col} vs {y_col}",
            color_discrete_sequence=color_seq,
            color_continuous_scale=div_scale,
        )
        cls.apply_theme(fig)
        return fig

    # 5. Line Chart
    @classmethod
    def create_line_chart(
        cls, df: pd.DataFrame, x_col: str, y_col: str, group_col: Optional[str] = None
    ) -> go.Figure:
        # Group and aggregate if we have duplicates for the same X to avoid messy lines
        plot_df = df
        if group_col:
            grouped = df.groupby([x_col, group_col])[y_col].mean().reset_index()
            plot_df = grouped
        else:
            grouped = df.groupby(x_col)[y_col].mean().reset_index()
            plot_df = grouped

        plot_df = plot_df.sort_values(by=x_col)
        color_seq, _ = cls.get_theme_colors()
        fig = px.line(
            plot_df,
            x=x_col,
            y=y_col,
            color=group_col,
            title=f"Line Chart of Average {y_col} by {x_col}",
            color_discrete_sequence=color_seq,
        )
        cls.apply_theme(fig)
        return fig

    # 6. Area Chart
    @classmethod
    def create_area_chart(
        cls, df: pd.DataFrame, x_col: str, y_col: str, group_col: Optional[str] = None
    ) -> go.Figure:
        if group_col:
            grouped = df.groupby([x_col, group_col])[y_col].mean().reset_index()
        else:
            grouped = df.groupby(x_col)[y_col].mean().reset_index()
        
        grouped = grouped.sort_values(by=x_col)
        color_seq, _ = cls.get_theme_colors()
        fig = px.area(
            grouped,
            x=x_col,
            y=y_col,
            color=group_col,
            title=f"Area Chart of Average {y_col} by {x_col}",
            color_discrete_sequence=color_seq,
        )
        cls.apply_theme(fig)
        return fig

    # 7. Pie Chart
    @classmethod
    def create_pie_chart(cls, df: pd.DataFrame, names_col: str, values_col: Optional[str] = None) -> go.Figure:
        if values_col:
            grouped = df.groupby(names_col)[values_col].sum().reset_index()
            # Sort and take top 10 to keep it clean
            grouped = grouped.sort_values(by=values_col, ascending=False).head(10)
        else:
            grouped = df[names_col].value_counts().reset_index()
            grouped.columns = [names_col, "Count"]
            grouped = grouped.head(10)
            values_col = "Count"

        color_seq, _ = cls.get_theme_colors()
        fig = px.pie(
            grouped,
            names=names_col,
            values=values_col,
            title=f"Distribution of {names_col} (Top 10)",
            color_discrete_sequence=color_seq,
        )
        cls.apply_theme(fig)
        return fig

    # 8. Donut Chart
    @classmethod
    def create_donut_chart(cls, df: pd.DataFrame, names_col: str, values_col: Optional[str] = None) -> go.Figure:
        if values_col:
            grouped = df.groupby(names_col)[values_col].sum().reset_index()
            grouped = grouped.sort_values(by=values_col, ascending=False).head(10)
        else:
            grouped = df[names_col].value_counts().reset_index()
            grouped.columns = [names_col, "Count"]
            grouped = grouped.head(10)
            values_col = "Count"

        color_seq, _ = cls.get_theme_colors()
        fig = px.pie(
            grouped,
            names=names_col,
            values=values_col,
            hole=0.6,
            title=f"Distribution breakdown of {names_col} (Top 10)",
            color_discrete_sequence=color_seq,
        )
        cls.apply_theme(fig)
        return fig

    # 9. Treemap
    @classmethod
    def create_treemap(cls, df: pd.DataFrame, path_cols: List[str], values_col: Optional[str] = None) -> go.Figure:
        # Group to avoid huge treemaps
        if values_col:
            grouped = df.groupby(path_cols)[values_col].sum().reset_index()
            # limit rows for safety
            grouped = grouped.sort_values(by=values_col, ascending=False).head(50)
        else:
            grouped = df.groupby(path_cols).size().reset_index(name="Count")
            grouped = grouped.sort_values(by="Count", ascending=False).head(50)
            values_col = "Count"

        color_seq, _ = cls.get_theme_colors()
        fig = px.treemap(
            grouped,
            path=path_cols,
            values=values_col,
            title=f"Treemap Hierarchy: {' > '.join(path_cols)}",
            color_discrete_sequence=color_seq,
        )
        cls.apply_theme(fig)
        fig.update_layout(margin=dict(t=50, l=10, r=10, b=10))
        return fig

    # 10. Sunburst
    @classmethod
    def create_sunburst(cls, df: pd.DataFrame, path_cols: List[str], values_col: Optional[str] = None) -> go.Figure:
        if values_col:
            grouped = df.groupby(path_cols)[values_col].sum().reset_index()
            grouped = grouped.sort_values(by=values_col, ascending=False).head(40)
        else:
            grouped = df.groupby(path_cols).size().reset_index(name="Count")
            grouped = grouped.sort_values(by="Count", ascending=False).head(40)
            values_col = "Count"

        color_seq, _ = cls.get_theme_colors()
        fig = px.sunburst(
            grouped,
            path=path_cols,
            values=values_col,
            title=f"Sunburst Hierarchy: {' > '.join(path_cols)}",
            color_discrete_sequence=color_seq,
        )
        cls.apply_theme(fig)
        fig.update_layout(margin=dict(t=50, l=10, r=10, b=10))
        return fig

    # 11. Violin Plot
    @classmethod
    def create_violin_plot(cls, df: pd.DataFrame, y_col: str, x_col: Optional[str] = None) -> go.Figure:
        sampled_df = cls.sample_if_large(df, 15000)
        color_seq, _ = cls.get_theme_colors()
        fig = px.violin(
            sampled_df,
            x=x_col,
            y=y_col,
            box=True,
            points="outliers",
            title=f"Violin Plot of {y_col}" + (f" by {x_col}" if x_col else ""),
            color_discrete_sequence=[color_seq[1] if len(color_seq) > 1 else color_seq[0]],
        )
        cls.apply_theme(fig)
        return fig

    # 12. Pair Plot (Scatter Matrix)
    @classmethod
    def create_pair_plot(cls, df: pd.DataFrame, num_cols: List[str], color_col: Optional[str] = None) -> go.Figure:
        # Cap columns to 4 for visibility and rendering speed
        selected_cols = num_cols[:4]
        sampled_df = cls.sample_if_large(df, 2000) # Scatter matrices are expensive
        color_seq, div_scale = cls.get_theme_colors()
        fig = px.scatter_matrix(
            sampled_df,
            dimensions=selected_cols,
            color=color_col,
            title=f"Scatter Matrix (Pair Plot) of Numerical Features",
            color_discrete_sequence=color_seq,
            color_continuous_scale=div_scale,
        )
        cls.apply_theme(fig)
        # Update diagonal settings and marker size
        fig.update_traces(diagonal_visible=False, marker=dict(size=3, opacity=0.7))
        fig.update_layout(
            height=550,
            autosize=True,
            margin=dict(l=15, r=15, t=50, b=15),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        return fig
