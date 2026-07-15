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
        navigate_label (Optional[str]): Deprecated. Kept for backward compatibility.

    Returns:
        bool: True if the action button is clicked, False otherwise.
    """
    default_icon = """
    <svg viewBox="0 0 24 24" style="width: 28px; height: 28px; stroke: var(--primary); fill: none; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round;">
        <path d="M12 5v14M5 12h14"/>
    </svg>
    """
    resolved_icon = icon_svg if icon_svg else default_icon

    import textwrap
    st.markdown(
        textwrap.dedent(
            f"""
            <div class="glass-card" style="padding: 2.5rem 1.75rem; border-radius: 12px; text-align: center; margin: 1.5rem 0;">
                <div class="icon-wrap" style="width: 56px; height: 56px; margin: 0 auto 1.25rem; border-radius: 50%; display: flex; align-items: center; justify-content: center; background: rgba(99, 102, 241, 0.08); border: 1px solid rgba(99, 102, 241, 0.15);">
                    {textwrap.dedent(resolved_icon).strip()}
                </div>
                <h3 style="margin: 0 0 0.5rem; font-size: 1.15rem; font-weight: 600; color: var(--text);">{title}</h3>
                <p style="margin: 0 auto 1.5rem; max-width: 420px; font-size: 0.85rem; line-height: 1.6; color: var(--subtext);">{message}</p>
            </div>
            """
        ).strip(),
        unsafe_allow_html=True,
    )

    if action_label:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            clicked = st.button(action_label, use_container_width=True, type="primary")
            if clicked and navigate_to:
                st.session_state["current_page"] = navigate_to
                st.rerun()
            return clicked

    return False
