"""
Forecasting Workspace Page.

Implements trend projections and predictive analytics on active datasets.
Features include target selection, forecast horizon controls, actuals comparison,
confidence intervals, and formatted exports.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from components.section_header import render_section_header
from components.empty_state import render_empty_state
from components.glass_card import glass_card_panel


def compute_forecast(df: pd.DataFrame, target_col: str, date_col: str, horizon: int) -> pd.DataFrame:
    """Compute trend projection and confidence intervals using linear trend + AR residuals."""
    if date_col and date_col != "[None]":
        df_clean = df[[date_col, target_col]].dropna().copy()
        df_clean[date_col] = pd.to_datetime(df_clean[date_col], errors="coerce")
        df_clean = df_clean.dropna().sort_values(by=date_col)
        df_agg = df_clean.groupby(date_col)[target_col].mean().reset_index()
        df_agg = df_agg.rename(columns={date_col: "ds", target_col: "y"})
    else:
        df_agg = df[[target_col]].dropna().copy().reset_index()
        df_agg = df_agg.rename(columns={"index": "ds", target_col: "y"})

    n_hist = len(df_agg)
    if n_hist < 3:
        return pd.DataFrame()

    # Fit trend: y = alpha * t + beta
    t_hist = np.arange(n_hist)
    y_hist = df_agg["y"].values
    alpha, beta = np.polyfit(t_hist, y_hist, 1)

    residuals = y_hist - (alpha * t_hist + beta)
    sigma = np.std(residuals) if np.std(residuals) > 0 else 1.0

    # Project horizon
    if date_col and date_col != "[None]":
        last_date = df_agg["ds"].max()
        future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=horizon, freq="D")
    else:
        last_val = df_agg["ds"].max()
        future_dates = np.arange(last_val + 1, last_val + 1 + horizon)

    t_future = np.arange(n_hist, n_hist + horizon)
    y_future = alpha * t_future + beta

    # Propagate last residual with decay
    last_res = residuals[-1]
    decay = 0.8
    residual_extrap = last_res * (decay ** np.arange(1, horizon + 1))
    y_future += residual_extrap

    # Standard errors growing with horizon
    se = sigma * np.sqrt(1 + 0.15 * np.arange(1, horizon + 1))
    upper_bounds = y_future + 1.96 * se
    lower_bounds = y_future - 1.96 * se

    # Assemble historical part
    hist_part = pd.DataFrame({
        "Timeline": df_agg["ds"],
        "Actual": df_agg["y"],
        "Forecast": np.nan,
        "Lower Bound": np.nan,
        "Upper Bound": np.nan,
    })

    # Assemble forecast part starting at the last point to connect lines
    forecast_timeline = [df_agg["ds"].iloc[-1]] + list(future_dates)
    forecast_y = [df_agg["y"].iloc[-1]] + list(y_future)
    forecast_lower = [df_agg["y"].iloc[-1]] + list(lower_bounds)
    forecast_upper = [df_agg["y"].iloc[-1]] + list(upper_bounds)

    fore_part = pd.DataFrame({
        "Timeline": forecast_timeline,
        "Actual": np.nan,
        "Forecast": forecast_y,
        "Lower Bound": forecast_lower,
        "Upper Bound": forecast_upper,
    })

    return pd.concat([hist_part, fore_part], ignore_index=True)


def render() -> None:
    """Render the Forecasting Workspace."""
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
        title="Predictive Forecasting Workspace",
        subtitle=f"Extrapolate future trajectories and confidence intervals for {filename}.",
        label="Predictive Engine",
    )

    if st.session_state.get("cleaned_df") is not None:
        st.info("All insights and metrics are generated from the cleaned dataset.")

    from services.visualization_service import VisualizationService
    detected = VisualizationService.detect_columns(df)
    numeric_cols = detected["numeric"]
    datetime_cols = detected["datetime"]

    if not numeric_cols:
        st.warning("Forecasting requires at least one numerical column. Please upload a dataset with numerical variables.")
        return

    from utils.theme_manager import get_current_theme
    theme_vars = get_current_theme()

    # Split Pane: Left Control Panel, Right Chart Panel
    col_ctrl, col_chart = st.columns([1, 2.5])

    with col_ctrl:
        st.markdown(f'<h4 style="margin-top: 0; font-weight: 700; color: var(--text);">Configuration</h4>', unsafe_allow_html=True)
        
        with glass_card_panel():
            target_var = st.selectbox(
                "Target variable (y)",
                options=numeric_cols,
                index=0,
                help="Select the continuous variable to project."
            )

            date_var = st.selectbox(
                "Timeline column (optional)",
                options=["[None]"] + datetime_cols,
                index=1 if datetime_cols else 0,
                help="Select a date column to align projections. If none selected, row sequence index is used."
            )

            horizon = st.slider(
                "Forecast horizon",
                min_value=7,
                max_value=120,
                value=30,
                step=1,
                help="Select the number of periods/days to project into the future."
            )

            st.markdown('<div style="margin-top: 1rem; border-top: 1px solid var(--border); padding-top: 1rem;"></div>', unsafe_allow_html=True)
            
            # Run forecast
            forecast_df = compute_forecast(df, target_var, date_var, horizon)
            
            if not forecast_df.empty:
                # Add to activity log
                if "forecast_logged" not in st.session_state or st.session_state.get("forecast_logged") != (target_var, date_var, horizon):
                    st.session_state["forecast_logged"] = (target_var, date_var, horizon)
                    if "activity_log" in st.session_state:
                        import datetime
                        now_str = datetime.datetime.now().strftime("%I:%M %p")
                        st.session_state["activity_log"].insert(0, {"time": now_str, "event": f"Forecast: {target_var} (+{horizon} steps)"})

                # Export option
                csv_bytes = forecast_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "📥 Download Forecast Data",
                    data=csv_bytes,
                    file_name=f"clario_forecast_{target_var}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.error("Failed to compute forecast. Ensure the selected variables contain valid rows.")

    with col_chart:
        st.markdown(f'<h4 style="margin-top: 0; font-weight: 700; color: var(--text);">Projection Canvas</h4>', unsafe_allow_html=True)
        
        if not forecast_df.empty:
            # Create Plotly forecast chart
            fig = go.Figure()
            
            # 1. Shaded Confidence Interval Region
            # Plotly fill 'tonexty' requires lower and upper trace plotted sequentially
            fig.add_trace(go.Scatter(
                x=forecast_df["Timeline"],
                y=forecast_df["Lower Bound"],
                mode="lines",
                line=dict(width=0),
                showlegend=False
            ))
            
            fig.add_trace(go.Scatter(
                x=forecast_df["Timeline"],
                y=forecast_df["Upper Bound"],
                mode="lines",
                line=dict(width=0),
                fill="tonexty",
                fillcolor="rgba(99, 102, 241, 0.08)" if theme_vars["primary"] == "#6366F1" else "rgba(79, 70, 229, 0.08)",
                name="95% Confidence Interval"
            ))
            
            # 2. Historical Actual Values
            fig.add_trace(go.Scatter(
                x=forecast_df["Timeline"],
                y=forecast_df["Actual"],
                mode="lines",
                line=dict(color=theme_vars["primary"], width=2),
                name="Historical Actual"
            ))
            
            # 3. Future Projections
            fig.add_trace(go.Scatter(
                x=forecast_df["Timeline"],
                y=forecast_df["Forecast"],
                mode="lines",
                line=dict(color=theme_vars["accent"], width=2.5, dash="dash"),
                name="Future Projection"
            ))
            
            # Apply Plotly theme details
            VisualizationService.apply_theme(fig)
            fig.update_layout(
                title=f"Forecast Projection: Average {target_var} over {horizon} Periods",
                height=500,
                hovermode="x unified",
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Quick Stats
            st.markdown('<p style="font-size: 0.95rem; font-weight: 600; color: var(--text); margin-top: 1rem; margin-bottom: 0.5rem;">Summary Metrics</p>', unsafe_allow_html=True)
            with glass_card_panel():
                sum_col1, sum_col2, sum_col3 = st.columns(3)
                hist_avg = df[target_var].mean()
                projected_vals = forecast_df["Forecast"].dropna()
                proj_avg = projected_vals.mean()
                proj_max = projected_vals.max()
                
                with sum_col1:
                    st.markdown('<p style="font-size: 0.82rem; color: var(--subtext); margin-bottom: 0;">Historical Mean</p>', unsafe_allow_html=True)
                    st.markdown(f'<p style="font-size: 1.25rem; font-weight: 700; color: var(--text); margin-top: 0;">{hist_avg:,.2f}</p>', unsafe_allow_html=True)
                with sum_col2:
                    st.markdown('<p style="font-size: 0.82rem; color: var(--subtext); margin-bottom: 0;">Projected Mean</p>', unsafe_allow_html=True)
                    st.markdown(f'<p style="font-size: 1.25rem; font-weight: 700; color: var(--accent); margin-top: 0;">{proj_avg:,.2f}</p>', unsafe_allow_html=True)
                with sum_col3:
                    st.markdown('<p style="font-size: 0.82rem; color: var(--subtext); margin-bottom: 0;">Peak Prediction</p>', unsafe_allow_html=True)
                    st.markdown(f'<p style="font-size: 1.25rem; font-weight: 700; color: var(--text); margin-top: 0;">{proj_max:,.2f}</p>', unsafe_allow_html=True)
        else:
            st.info("A forecast chart will appear here once the configurations are validated.")


if __name__ == "__main__":
    render()
