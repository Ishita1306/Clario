"""
Glass card component.

Provides a styled container with glassmorphic backdrop filter and borders,
supporting dark theme aesthetics.
"""

from contextlib import contextmanager

import streamlit as st


def render_glass_card(content_html: str, class_name: str = "") -> None:
    """
    Render a premium glassmorphic card containing static HTML content.

    Args:
        content_html (str): The HTML content to render inside the card.
        class_name (str): Additional CSS classes to append.
    """
    card_html = f'<div class="glass-card {class_name}">{content_html}</div>'
    st.markdown(card_html, unsafe_allow_html=True)


@contextmanager
def glass_card_panel():
    """
    Wrap Streamlit widgets in a glass-styled bordered container.

    Uses native Streamlit containers instead of split HTML tags, which would
    otherwise render orphaned closing tags as visible text.
    """
    with st.container(border=True):
        yield


def glass_card_wrapper_start(style_attrs: str = "") -> None:
    """
    Deprecated: use glass_card_panel() context manager instead.

    Kept for backward compatibility; delegates to a bordered container marker.
    """
    del style_attrs
    st.markdown('<div class="glass-card-panel-marker"></div>', unsafe_allow_html=True)


def glass_card_wrapper_end() -> None:
    """Deprecated: no-op. Closing tags are not injected to avoid visible HTML."""
    return
