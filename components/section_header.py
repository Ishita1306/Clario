"""
Section header component.

Renders headers with optional labels, titles, and descriptions, matching the
dark mode font sizing and alignment.
"""

from typing import Optional
import streamlit as st


def render_section_header(
    title: str,
    subtitle: Optional[str] = None,
    label: Optional[str] = None,
    center: bool = False,
) -> None:
    """
    Render a premium section header.

    Args:
        title (str): Primary section title.
        subtitle (Optional[str]): Informational description paragraph.
        label (Optional[str]): Small uppercase label pill above the title.
        center (bool): Center align the header content.
    """
    align_class = "center" if center else ""
    label_html = f'<span class="section-label">{label}</span>' if label else ""
    subtitle_html = (
        f'<p class="section-subtitle">{subtitle}</p>' if subtitle else ""
    )

    import textwrap
    header_html = textwrap.dedent(
        f"""
        <div class="section-header {align_class}" style="margin-bottom: 2rem; margin-top: 1.5rem;">
            {label_html}
            <h2 class="section-title" style="margin-top: 0.5rem; font-size: 1.8rem; font-weight: 800;">{title}</h2>
            {subtitle_html}
        </div>
        """
    ).strip()
    st.markdown(header_html, unsafe_allow_html=True)
