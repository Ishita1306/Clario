"""
Metric card component.

Renders high-fidelity KPI metric cards with trends, icons, and secondary details
adhering to the platform's luxury dark theme.
"""

from typing import Optional
import streamlit as st


def render_metric_card(
    value: str,
    label: str,
    detail: Optional[str] = None,
    trend: Optional[str] = None,
    trend_positive: bool = True,
    icon_svg: Optional[str] = None,
) -> None:
    """
    Render a premium KPI metrics card.

    Args:
        value (str): Main metric value (e.g., "$24K", "1,200").
        label (str): Label describing the metric.
        detail (Optional[str]): Informational subtext below the label.
        trend (Optional[str]): Trend percentage indicator (e.g. "+14%").
        trend_positive (bool): Whether the trend is green (positive) or red (negative).
        icon_svg (Optional[str]): Custom SVG content. If none provided, displays a default.
    """
    default_icon = (
        '<svg viewBox="0 0 24 24"><path d="M4 7h16M4 12h10M4 17h14"/></svg>'
    )
    resolved_icon = icon_svg if icon_svg else default_icon

    trend_color = "#10B981" if trend_positive else "#EF4444"
    trend_html = (
        f'<span class="kpi-trend" style="color: {trend_color};">{trend}</span>'
        if trend
        else ""
    )

    detail_html = f'<p class="kpi-detail">{detail}</p>' if detail else ""

    card_html = (
        f'<div class="kpi-card glass-card" style="margin-bottom: 1rem;">'
        f'<div class="kpi-top">'
        f'<div class="kpi-icon-wrap icon-box">{resolved_icon.strip()}</div>'
        f'{trend_html}'
        f'</div>'
        f'<p class="kpi-value">{value}</p>'
        f'<p class="kpi-label">{label}</p>'
        f'{detail_html}'
        f'</div>'
    )
    st.markdown(card_html, unsafe_allow_html=True)
