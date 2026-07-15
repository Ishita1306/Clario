"""
Theme manager utility for InsightFlow.
"""

import streamlit as st

THEMES = {
    "dark": {
        "bg": "#0B0F19",
        "surface": "#111827",
        "card": "#1F2937",
        "primary": "#6366F1",
        "secondary": "#4F46E5",
        "accent": "#06B6D4",
        "text": "#F9FAFB",
        "subtext": "#9CA3AF",
        "border": "rgba(255, 255, 255, 0.08)",
        "glass": "rgba(17, 24, 39, 0.7)",
    },
    "light": {
        "bg": "#FFFFFF",
        "surface": "#F8FAFC",
        "card": "#FFFFFF",
        "primary": "#0F172A",
        "secondary": "#334155",
        "accent": "#475569",
        "text": "#0F172A",
        "subtext": "#64748B",
        "border": "#E2E8F0",
        "glass": "#FFFFFF",
    }
}


def get_current_theme():
    """Retrieve active theme variables from session state."""
    theme_name = st.session_state.get("theme", "dark")
    return THEMES.get(theme_name, THEMES["dark"])


def inject_theme_css():
    """Inject theme-specific CSS variables to override theme.css variables."""
    theme_name = st.session_state.get("theme", "dark")
    theme_vars = THEMES.get(theme_name, THEMES["dark"])
    
    theme_css = f"""
    <style>
    :root {{
        --bg: {theme_vars['bg']} !important;
        --surface: {theme_vars['surface']} !important;
        --card: {theme_vars['card']} !important;
        --primary: {theme_vars['primary']} !important;
        --secondary: {theme_vars['secondary']} !important;
        --accent: {theme_vars['accent']} !important;
        --text: {theme_vars['text']} !important;
        --subtext: {theme_vars['subtext']} !important;
        --border: {theme_vars['border']} !important;
        --glass: {theme_vars['glass']} !important;
    }}
    
    /* Native App Layout */
    .stApp {{
        background-color: {theme_vars['bg']} !important;
    }}
    
    /* Headers & Text colors */
    h1, h2, h3, h4, h5, h6, p, span, label {{
        color: {theme_vars['text']} !important;
    }}
    
    /* Selectboxes, Dropdowns, Inputs styling */
    div[data-baseweb="select"] > div, div[data-baseweb="input"] {{
        background-color: {theme_vars['surface']} !important;
        border: 1px solid {theme_vars['border']} !important;
        border-radius: 6px !important;
        color: {theme_vars['text']} !important;
    }}
    
    div[data-baseweb="select"] span, div[data-baseweb="input"] input {{
        color: {theme_vars['text']} !important;
    }}
    
    /* Popover/Dropdown listbox */
    div[role="listbox"] {{
        background-color: {theme_vars['surface']} !important;
        border: 1px solid {theme_vars['border']} !important;
        border-radius: 6px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
    }}
    
    div[role="option"] {{
        color: {theme_vars['text']} !important;
    }}
    div[role="option"]:hover, div[role="option"][aria-selected="true"] {{
        background-color: {theme_vars['card']} !important;
        color: {theme_vars['primary']} !important;
    }}
    
    /* Tabs styling */
    button[data-baseweb="tab"] {{
        color: {theme_vars['subtext']} !important;
        font-weight: 500 !important;
        background: transparent !important;
        border: none !important;
        padding: 0.5rem 1rem !important;
        transition: color 0.18s ease-in-out !important;
    }}
    button[data-baseweb="tab"][aria-selected="true"] {{
        color: {theme_vars['primary']} !important;
        border-bottom: 2px solid {theme_vars['primary']} !important;
    }}
    
    /* Checkboxes & Radios */
    span[data-baseweb="checkbox"] > div {{
        border-color: {theme_vars['border']} !important;
        border-radius: 4px !important;
    }}
    span[data-baseweb="checkbox"][data-checked="true"] > div {{
        background-color: {theme_vars['primary']} !important;
        border-color: {theme_vars['primary']} !important;
    }}
    
    /* Sidebar styling overrides */
    [data-testid="stSidebar"] {{
        background-color: {theme_vars['surface']} !important;
        border-right: 1px solid {theme_vars['border']} !important;
    }}
    
    /* Upload drag and drop box */
    div[data-testid="stFileUploaderDropzone"] {{
        background-color: {theme_vars['surface']} !important;
        border: 1px dashed {theme_vars['primary']} !important;
        border-radius: 8px !important;
    }}
    
    /* Success, Info, Warning, Error alerts styling */
    div[data-testid="stAlert"] {{
        background-color: {theme_vars['surface']} !important;
        border: 1px solid {theme_vars['border']} !important;
        border-radius: 8px !important;
    }}
    """
    
    # Apply flat, gradient-free styles for light theme
    if theme_name == "light":
        theme_css += """
        .stApp {
            background: #FFFFFF !important;
        }
        .hero-section {
            background: #F8FAFC !important;
            border: 1px solid #E2E8F0 !important;
        }
        .hero-glow, .dash-glow-ring {
            display: none !important;
        }
        .glass-card {
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05), 0 1px 2px 0 rgba(0, 0, 0, 0.03) !important;
        }
        .glass-card:hover {
            transform: none !important;
            border-color: #0F172A !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03) !important;
        }
        """
        
    theme_css += "\n</style>"
    st.markdown(theme_css, unsafe_allow_html=True)
