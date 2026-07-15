"""
Empty state component.

Renders high-fidelity notices when data or context is unavailable, matching
the platform's dark theme design system.
"""

from typing import Optional
import streamlit as st


def render_empty_state(
    title: str,
    message: str,
    icon_svg: Optional[str] = None,
    action_label: Optional[str] = None,
    navigate_to: Optional[str] = None,
    navigate_label: Optional[str] = None,
) -> bool:
    """
    Render a premium empty state container with an optional action button.

    Args:
        title (str): Warning or status title.
        message (str): Explanatory text.
        icon_svg (Optional[str]): SVG icon path or content. Defaults to a database upload icon.
        action_label (Optional[str]): Label for an action button.
        navigate_to (Optional[str]): Internal page key to navigate to on action click.
        navigate_label (Optional[str]): Sidebar label matching navigate_to.

    Returns:
        bool: True if the action button is clicked, False otherwise.
    """
    default_icon = """
    <svg viewBox="0 0 24 24" style="width: 32px; height: 32px; stroke: var(--accent); fill: none; stroke-width: 1.5; stroke-linecap: round; stroke-linejoin: round;">
        <path d="M12 5v14M5 12h14"/>
    </svg>
    """
    resolved_icon = icon_svg if icon_svg else default_icon

    st.markdown(
        f"""
        <div class="glass-card" style="padding: 3rem 2rem; border-radius: 16px; text-align: center; margin: 2rem 0;">
            <div class="icon-wrap" style="width: 64px; height: 64px; margin: 0 auto 1.5rem; border-radius: 50%; display: flex; align-items: center; justify-content: center; background: rgba(124, 58, 237, 0.1); border: 1px solid rgba(124, 58, 237, 0.2);">
                {resolved_icon}
            </div>
            <h3 style="margin: 0 0 0.5rem; font-size: 1.25rem; font-weight: 700; color: var(--text);">{title}</h3>
            <p style="margin: 0 auto 2rem; max-width: 420px; font-size: 0.9rem; line-height: 1.6; color: var(--subtext);">{message}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if action_label:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            clicked = st.button(action_label, use_container_width=True, type="primary")
            if clicked and navigate_to:
                st.session_state["current_page"] = navigate_to
                if navigate_label:
                    st.session_state["nav_selection"] = navigate_label
                st.rerun()
            return clicked

    return False
