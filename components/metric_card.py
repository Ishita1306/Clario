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

    trend_color = "#4ade80" if trend_positive else "#f87171"
    trend_html = (
        f'<span class="kpi-trend" style="color: {trend_color};">{trend}</span>'
        if trend
        else ""
    )

    detail_html = f'<p class="kpi-detail">{detail}</p>' if detail else ""

    import textwrap
    card_html = textwrap.dedent(
        f"""
        <div class="kpi-card glass-card" style="margin-bottom: 1rem;">
            <div class="kpi-top">
                <div class="kpi-icon-wrap icon-box">
                    {textwrap.dedent(resolved_icon).strip()}
                </div>
                {trend_html}
            </div>
            <p class="kpi-value">{value}</p>
            <p class="kpi-label">{label}</p>
            {detail_html}
        </div>
        """
    ).strip()
    st.markdown(card_html, unsafe_allow_html=True)
