"""
Settings Workspace Page.

Configures system preferences, visual themes, and integration profiles.
"""

import streamlit as st
from components.section_header import render_section_header
from components.glass_card import glass_card_panel


def render() -> None:
    """Render the settings workspace page."""
    render_section_header(
        title="Settings Workspace",
        subtitle="Configure application preferences, interface themes, and credentials.",
        label="Configuration Center",
    )

    # 1. Interface Theme Selector
    st.markdown('<h4 style="margin-top: 1rem; font-weight: 700; color: var(--text);">Interface Customization</h4>', unsafe_allow_html=True)
    with glass_card_panel():
        st.markdown('<p style="font-size: 0.95rem; font-weight: 600; color: var(--text); margin-top: 0;">Theme Selection</p>', unsafe_allow_html=True)
        st.markdown('<p style="font-size: 0.85rem; color: var(--subtext); margin-bottom: 1rem;">Choose between Dark and Light mode. The chosen theme applies instantly across all workspaces.</p>', unsafe_allow_html=True)
        
        current_theme = st.session_state.get("theme", "dark")
        theme_index = 0 if current_theme == "dark" else 1
        
        selected_theme = st.selectbox(
            "Select Theme Mode",
            options=["Dark Theme", "Light Theme"],
            index=theme_index,
            key="theme_selector_widget"
        )
        
        target_theme = "dark" if selected_theme == "Dark Theme" else "light"
        if target_theme != current_theme:
            st.session_state["theme"] = target_theme
            st.rerun()

    # 2. System Preferences (Placeholders)
    st.markdown('<h4 style="margin-top: 2rem; font-weight: 700; color: var(--text);">System Preferences</h4>', unsafe_allow_html=True)
    with glass_card_panel():
        st.markdown('<p style="font-size: 0.95rem; font-weight: 600; color: var(--text); margin-top: 0;">API & Credentials</p>', unsafe_allow_html=True)
        st.text_input("GCP Project ID", value="clario-ai-prod", disabled=True)
        st.text_input("Storage Bucket URI", value="gs://clario-data-lake", disabled=True)
        st.markdown('<p style="font-size: 0.8rem; color: var(--subtext); margin-top: 0.5rem;">API and database configurations are currently managed by environment profiles.</p>', unsafe_allow_html=True)

    # 3. User Session Management
    st.markdown('<h4 style="margin-top: 2rem; font-weight: 700; color: var(--text);">Session Management</h4>', unsafe_allow_html=True)
    with glass_card_panel():
        st.markdown('<p style="font-size: 0.95rem; font-weight: 600; color: var(--text); margin-top: 0;">User Account</p>', unsafe_allow_html=True)
        user_info = st.session_state.get("user", {"email": "guest@clario.ai", "name": "Guest"})
        st.markdown(f'<p style="font-size: 0.85rem; color: var(--subtext); margin-bottom: 1rem;">Logged in as: <strong>{user_info["name"]}</strong> ({user_info["email"]})</p>', unsafe_allow_html=True)
        
        if st.button("Sign Out", type="secondary"):
            st.session_state["authenticated"] = False
            st.session_state["user"] = None
            st.session_state["current_page"] = "landing"
            st.rerun()
