"""
InsightFlow application entry point.

This module configures the Streamlit runtime and renders the landing page.
Business logic and feature modules are intentionally excluded at this stage.
"""

import streamlit as st


def configure_page():
    """Apply global Streamlit page configuration."""
    st.set_page_config(
        page_title="InsightFlow AI",
        layout="wide",
        initial_sidebar_state="collapsed",
    )


def inject_styles():
    """Inject custom CSS for typography, spacing, and layout."""
    st.markdown(
        """
        <style>
            @import url(
                'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
            );

            :root {
                --bg: #09090B;
                --surface: #111113;
                --card: #18181B;
                --primary: #7C3AED;
                --secondary: #8B5CF6;
                --accent: #22D3EE;
                --text: #FAFAFA;
                --subtext: #A1A1AA;
                --border: rgba(255, 255, 255, 0.08);
                --glass: rgba(24, 24, 27, 0.65);
            }

            html, body, [class*="css"] {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                color: var(--text);
            }

            .stApp {
                background:
                    radial-gradient(
                        ellipse 70% 45% at 15% -5%,
                        rgba(124, 58, 237, 0.14),
                        transparent 55%
                    ),
                    radial-gradient(
                        ellipse 50% 35% at 85% 5%,
                        rgba(34, 211, 238, 0.08),
                        transparent 50%
                    ),
                    radial-gradient(
                        ellipse 60% 40% at 50% 100%,
                        rgba(139, 92, 246, 0.06),
                        transparent 55%
                    ),
                    var(--bg);
            }

            .block-container {
                padding-top: 1.25rem;
                padding-bottom: 0;
                max-width: 1200px;
            }

            #MainMenu { visibility: hidden; }
            footer { visibility: hidden; }

            /* ── Shared ───────────────────────────────────────────── */
            .page-section {
                margin-bottom: 7rem;
            }

            .section-header {
                margin-bottom: 3.5rem;
            }

            .section-header.center {
                text-align: center;
            }

            .section-header.center .section-subtitle {
                margin-left: auto;
                margin-right: auto;
            }

            .section-label {
                display: inline-block;
                margin-bottom: 1rem;
                padding: 0.35rem 0.9rem;
                font-size: 0.68rem;
                font-weight: 600;
                letter-spacing: 0.14em;
                text-transform: uppercase;
                color: var(--accent);
                background: rgba(34, 211, 238, 0.06);
                border: 1px solid rgba(34, 211, 238, 0.14);
                border-radius: 999px;
            }

            .section-title {
                margin: 0 0 0.85rem;
                font-size: clamp(1.9rem, 3.5vw, 2.65rem);
                font-weight: 800;
                letter-spacing: -0.04em;
                line-height: 1.12;
                color: var(--text);
            }

            .section-subtitle {
                max-width: 580px;
                margin: 0;
                font-size: 1.02rem;
                line-height: 1.75;
                color: var(--subtext);
            }

            .glass-card {
                background: var(--glass);
                backdrop-filter: blur(24px);
                -webkit-backdrop-filter: blur(24px);
                border: 1px solid var(--border);
                box-shadow:
                    0 0 0 1px rgba(255, 255, 255, 0.02) inset,
                    0 12px 40px rgba(0, 0, 0, 0.35);
                transition:
                    transform 0.4s cubic-bezier(0.22, 1, 0.36, 1),
                    border-color 0.4s ease,
                    box-shadow 0.4s ease;
            }

            .glass-card:hover {
                transform: translateY(-5px);
                border-color: rgba(124, 58, 237, 0.35);
                box-shadow:
                    0 0 0 1px rgba(124, 58, 237, 0.08) inset,
                    0 20px 56px rgba(124, 58, 237, 0.12);
            }

            .icon-box {
                display: flex;
                align-items: center;
                justify-content: center;
                flex-shrink: 0;
            }

            .icon-box svg {
                width: 22px;
                height: 22px;
                stroke: var(--accent);
                fill: none;
                stroke-width: 1.75;
                stroke-linecap: round;
                stroke-linejoin: round;
            }

            .icon-box.lg svg {
                width: 24px;
                height: 24px;
            }

            .icon-wrap {
                display: flex;
                align-items: center;
                justify-content: center;
                width: 48px;
                height: 48px;
                margin-bottom: 1.35rem;
                border-radius: 12px;
                background: rgba(124, 58, 237, 0.1);
                border: 1px solid rgba(124, 58, 237, 0.18);
                transition: all 0.35s cubic-bezier(0.22, 1, 0.36, 1);
            }

            .glass-card:hover .icon-wrap {
                background: linear-gradient(135deg, var(--primary), var(--secondary));
                border-color: transparent;
                box-shadow: 0 8px 24px rgba(124, 58, 237, 0.35);
            }

            .glass-card:hover .icon-wrap svg {
                stroke: #ffffff;
            }

            /* ── Hero ─────────────────────────────────────────────── */
            .hero-section {
                position: relative;
                overflow: hidden;
                padding: 4rem 0 5rem;
                margin-bottom: 4rem;
            }

            .hero-grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 4rem;
                align-items: center;
            }

            .hero-glow {
                position: absolute;
                border-radius: 50%;
                filter: blur(100px);
                pointer-events: none;
            }

            .hero-glow-a {
                top: -60px;
                left: -80px;
                width: 400px;
                height: 400px;
                background: rgba(124, 58, 237, 0.2);
            }

            .hero-glow-b {
                bottom: -40px;
                right: -60px;
                width: 320px;
                height: 320px;
                background: rgba(34, 211, 238, 0.1);
            }

            .hero-content {
                position: relative;
                z-index: 1;
            }

            .hero-badge {
                display: inline-flex;
                align-items: center;
                gap: 0.5rem;
                padding: 0.4rem 1rem;
                margin-bottom: 1.75rem;
                font-size: 0.7rem;
                font-weight: 600;
                letter-spacing: 0.1em;
                text-transform: uppercase;
                color: var(--secondary);
                background: rgba(139, 92, 246, 0.08);
                border: 1px solid rgba(139, 92, 246, 0.2);
                border-radius: 999px;
            }

            .hero-badge-dot {
                width: 6px;
                height: 6px;
                border-radius: 50%;
                background: var(--accent);
                box-shadow: 0 0 10px var(--accent);
            }

            .hero-title {
                margin: 0 0 1.25rem;
                font-size: clamp(2.5rem, 5vw, 3.75rem);
                font-weight: 800;
                line-height: 1.05;
                letter-spacing: -0.045em;
                color: var(--text);
            }

            .hero-title span {
                background: linear-gradient(
                    135deg,
                    var(--secondary) 0%,
                    var(--accent) 100%
                );
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }

            .hero-headline {
                margin: 0 0 1rem;
                font-size: clamp(1.2rem, 2.2vw, 1.55rem);
                font-weight: 600;
                letter-spacing: -0.02em;
                line-height: 1.35;
                color: var(--text);
            }

            .hero-description {
                margin: 0 0 2.5rem;
                max-width: 480px;
                font-size: 1rem;
                line-height: 1.75;
                color: var(--subtext);
            }

            .hero-actions {
                display: flex;
                flex-wrap: wrap;
                gap: 0.85rem;
            }

            .btn {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                gap: 0.5rem;
                padding: 0.875rem 1.75rem;
                font-size: 0.9rem;
                font-weight: 600;
                border-radius: 10px;
                cursor: pointer;
                transition: all 0.35s cubic-bezier(0.22, 1, 0.36, 1);
                border: none;
            }

            .btn-primary {
                color: #ffffff;
                background: linear-gradient(
                    135deg,
                    var(--primary) 0%,
                    var(--secondary) 100%
                );
                box-shadow: 0 4px 20px rgba(124, 58, 237, 0.4);
            }

            .btn-primary:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 32px rgba(124, 58, 237, 0.55);
            }

            .btn-secondary {
                color: var(--text);
                background: rgba(255, 255, 255, 0.03);
                border: 1px solid var(--border);
            }

            .btn-secondary:hover {
                background: rgba(255, 255, 255, 0.06);
                border-color: rgba(255, 255, 255, 0.15);
                transform: translateY(-2px);
            }

            /* Dashboard illustration */
            .hero-visual {
                position: relative;
                z-index: 1;
            }

            .dash-frame {
                padding: 1rem;
                border-radius: 16px;
                background: var(--surface);
                border: 1px solid var(--border);
                box-shadow:
                    0 0 0 1px rgba(255, 255, 255, 0.03) inset,
                    0 32px 64px rgba(0, 0, 0, 0.5);
            }

            .dash-topbar {
                display: flex;
                align-items: center;
                gap: 0.5rem;
                margin-bottom: 1rem;
                padding-bottom: 0.85rem;
                border-bottom: 1px solid var(--border);
            }

            .dash-dot {
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background: #3f3f46;
            }

            .dash-dot.red { background: #ef4444; }
            .dash-dot.yellow { background: #eab308; }
            .dash-dot.green { background: #22c55e; }

            .dash-topbar-title {
                margin-left: 0.5rem;
                font-size: 0.72rem;
                font-weight: 500;
                color: var(--subtext);
            }

            .dash-body {
                display: grid;
                grid-template-columns: 64px 1fr;
                gap: 0.85rem;
            }

            .dash-sidebar {
                display: flex;
                flex-direction: column;
                gap: 0.5rem;
            }

            .dash-nav-item {
                height: 8px;
                border-radius: 4px;
                background: #27272a;
            }

            .dash-nav-item.active {
                background: linear-gradient(90deg, var(--primary), var(--secondary));
            }

            .dash-main {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 0.65rem;
            }

            .dash-widget {
                padding: 0.85rem;
                border-radius: 10px;
                background: var(--card);
                border: 1px solid var(--border);
            }

            .dash-widget.wide {
                grid-column: span 2;
            }

            .dash-widget-label {
                margin-bottom: 0.65rem;
                font-size: 0.62rem;
                font-weight: 500;
                letter-spacing: 0.06em;
                text-transform: uppercase;
                color: var(--subtext);
            }

            .dash-bars {
                display: flex;
                align-items: flex-end;
                gap: 4px;
                height: 48px;
            }

            .dash-bar {
                flex: 1;
                border-radius: 3px 3px 0 0;
                background: linear-gradient(
                    180deg,
                    var(--secondary),
                    var(--primary)
                );
                opacity: 0.85;
            }

            .dash-line-chart {
                position: relative;
                height: 48px;
                overflow: hidden;
            }

            .dash-line-chart svg {
                width: 100%;
                height: 100%;
            }

            .dash-kpi-row {
                display: flex;
                gap: 0.5rem;
            }

            .dash-kpi {
                flex: 1;
                padding: 0.5rem;
                border-radius: 6px;
                background: rgba(124, 58, 237, 0.08);
                border: 1px solid rgba(124, 58, 237, 0.12);
            }

            .dash-kpi-val {
                font-size: 0.85rem;
                font-weight: 700;
                color: var(--accent);
            }

            .dash-kpi-lbl {
                font-size: 0.55rem;
                color: var(--subtext);
            }

            .dash-glow-ring {
                position: absolute;
                inset: -1px;
                border-radius: 17px;
                background: linear-gradient(
                    135deg,
                    rgba(124, 58, 237, 0.3),
                    transparent 40%,
                    rgba(34, 211, 238, 0.2)
                );
                z-index: -1;
                opacity: 0.6;
            }

            /* ── KPI ──────────────────────────────────────────────── */
            .kpi-grid {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 1rem;
                margin-bottom: 7rem;
            }

            .kpi-card {
                padding: 1.75rem 1.5rem;
                border-radius: 14px;
            }

            .kpi-top {
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-bottom: 1.25rem;
            }

            .kpi-icon-wrap {
                width: 40px;
                height: 40px;
                border-radius: 10px;
                background: rgba(34, 211, 238, 0.08);
                border: 1px solid rgba(34, 211, 238, 0.12);
            }

            .kpi-icon-wrap svg {
                stroke: var(--accent);
            }

            .kpi-trend {
                font-size: 0.72rem;
                font-weight: 600;
                color: #4ade80;
            }

            .kpi-value {
                margin: 0 0 0.25rem;
                font-size: clamp(1.6rem, 2.5vw, 2rem);
                font-weight: 800;
                letter-spacing: -0.03em;
                color: var(--text);
            }

            .kpi-label {
                margin: 0 0 0.5rem;
                font-size: 0.85rem;
                font-weight: 600;
                color: var(--text);
            }

            .kpi-detail {
                margin: 0;
                font-size: 0.78rem;
                line-height: 1.5;
                color: var(--subtext);
            }

            /* ── Timeline / Workflow ──────────────────────────────── */
            .workflow-section {
                padding: 3.5rem 2.5rem;
                border-radius: 20px;
                background: var(--surface);
                border: 1px solid var(--border);
            }

            .timeline {
                position: relative;
                display: flex;
                justify-content: space-between;
                padding-top: 2rem;
            }

            .timeline-rail {
                position: absolute;
                top: 2.65rem;
                left: 5%;
                right: 5%;
                height: 2px;
                background: linear-gradient(
                    90deg,
                    var(--primary),
                    var(--secondary),
                    var(--accent)
                );
                opacity: 0.35;
            }

            .timeline-step {
                flex: 1;
                display: flex;
                flex-direction: column;
                align-items: center;
                text-align: center;
                padding: 0 0.75rem;
                position: relative;
                z-index: 1;
            }

            .timeline-node {
                display: flex;
                align-items: center;
                justify-content: center;
                width: 52px;
                height: 52px;
                margin-bottom: 1.25rem;
                border-radius: 50%;
                background: var(--card);
                border: 2px solid rgba(124, 58, 237, 0.4);
                transition: all 0.35s cubic-bezier(0.22, 1, 0.36, 1);
            }

            .timeline-step:hover .timeline-node {
                border-color: var(--accent);
                background: rgba(124, 58, 237, 0.15);
                box-shadow: 0 0 24px rgba(124, 58, 237, 0.3);
                transform: scale(1.08);
            }

            .timeline-step h4 {
                margin: 0 0 0.35rem;
                font-size: 0.92rem;
                font-weight: 700;
                color: var(--text);
            }

            .timeline-step p {
                margin: 0;
                font-size: 0.78rem;
                line-height: 1.5;
                color: var(--subtext);
                max-width: 130px;
            }

            .timeline-index {
                position: absolute;
                top: -1.5rem;
                font-size: 0.65rem;
                font-weight: 700;
                letter-spacing: 0.08em;
                color: var(--primary);
            }

            /* ── Features ───────────────────────────────────────── */
            .feature-grid {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 1rem;
            }

            .feature-card {
                padding: 2rem 1.5rem;
                border-radius: 14px;
                position: relative;
                overflow: hidden;
            }

            .feature-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 1px;
                background: linear-gradient(
                    90deg,
                    transparent,
                    rgba(124, 58, 237, 0.4),
                    transparent
                );
                opacity: 0;
                transition: opacity 0.35s ease;
            }

            .feature-card:hover::before {
                opacity: 1;
            }

            .feature-card h3 {
                margin: 0 0 0.6rem;
                font-size: 1rem;
                font-weight: 700;
                color: var(--text);
            }

            .feature-card p {
                margin: 0;
                font-size: 0.85rem;
                line-height: 1.65;
                color: var(--subtext);
            }

            .feature-tag {
                display: inline-block;
                margin-top: 1.25rem;
                padding: 0.25rem 0.65rem;
                font-size: 0.68rem;
                font-weight: 600;
                letter-spacing: 0.04em;
                color: var(--secondary);
                background: rgba(139, 92, 246, 0.1);
                border-radius: 6px;
            }

            /* ── Why section ──────────────────────────────────────── */
            .why-section {
                padding: 4rem 2.5rem;
                border-radius: 20px;
                background:
                    radial-gradient(
                        ellipse 70% 50% at 50% 0%,
                        rgba(124, 58, 237, 0.08),
                        transparent 60%
                    ),
                    var(--surface);
                border: 1px solid var(--border);
            }

            .why-grid {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 1rem;
            }

            .why-card {
                padding: 2rem 1.5rem;
                border-radius: 14px;
                text-align: left;
            }

            .why-card h3 {
                margin: 0 0 0.55rem;
                font-size: 1rem;
                font-weight: 700;
                color: var(--text);
            }

            .why-card p {
                margin: 0;
                font-size: 0.85rem;
                line-height: 1.65;
                color: var(--subtext);
            }

            /* ── Tech stack ───────────────────────────────────────── */
            .tech-section {
                text-align: center;
            }

            .tech-grid {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 0.75rem;
                margin-top: 2.5rem;
            }

            .tech-pill {
                display: inline-flex;
                align-items: center;
                gap: 0.55rem;
                padding: 0.65rem 1.15rem;
                font-size: 0.82rem;
                font-weight: 500;
                color: var(--text);
                background: var(--card);
                border: 1px solid var(--border);
                border-radius: 10px;
                transition: all 0.3s ease;
            }

            .tech-pill:hover {
                border-color: rgba(124, 58, 237, 0.4);
                background: rgba(124, 58, 237, 0.08);
                transform: translateY(-2px);
            }

            .tech-dot {
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background: var(--primary);
            }

            /* ── Footer ───────────────────────────────────────────── */
            .site-footer {
                margin: 0 -5rem;
                padding: 0 5rem 2.5rem;
            }

            .footer-divider {
                height: 1px;
                margin-bottom: 3.5rem;
                background: linear-gradient(
                    90deg,
                    transparent,
                    var(--border),
                    transparent
                );
            }

            .footer-inner {
                max-width: 1200px;
                margin: 0 auto;
            }

            .footer-top {
                display: grid;
                grid-template-columns: 1.6fr 1fr 1fr 1fr;
                gap: 3rem;
                padding-bottom: 3rem;
            }

            .footer-brand-name {
                margin: 0 0 0.85rem;
                font-size: 1.3rem;
                font-weight: 800;
                letter-spacing: -0.03em;
                color: var(--text);
            }

            .footer-brand-name span {
                color: var(--secondary);
            }

            .footer-brand-desc {
                margin: 0 0 1.5rem;
                font-size: 0.85rem;
                line-height: 1.7;
                color: var(--subtext);
                max-width: 280px;
            }

            .footer-social {
                display: flex;
                gap: 0.65rem;
            }

            .footer-social-icon {
                display: flex;
                align-items: center;
                justify-content: center;
                width: 36px;
                height: 36px;
                border-radius: 8px;
                background: var(--card);
                border: 1px solid var(--border);
                transition: all 0.3s ease;
            }

            .footer-social-icon:hover {
                border-color: rgba(124, 58, 237, 0.4);
                background: rgba(124, 58, 237, 0.1);
            }

            .footer-social-icon svg {
                width: 16px;
                height: 16px;
                stroke: var(--subtext);
                fill: none;
                stroke-width: 1.75;
            }

            .footer-col h5 {
                margin: 0 0 1.15rem;
                font-size: 0.68rem;
                font-weight: 600;
                letter-spacing: 0.12em;
                text-transform: uppercase;
                color: var(--subtext);
            }

            .footer-col p {
                margin: 0 0 0.55rem;
                font-size: 0.85rem;
                color: #71717a;
                line-height: 1.5;
            }

            .footer-bottom {
                display: flex;
                align-items: center;
                justify-content: space-between;
                flex-wrap: wrap;
                gap: 1rem;
                padding-top: 2rem;
                border-top: 1px solid var(--border);
            }

            .footer-copy {
                margin: 0;
                font-size: 0.8rem;
                color: #52525b;
            }

            .footer-badge {
                display: inline-flex;
                align-items: center;
                gap: 0.5rem;
                padding: 0.4rem 0.85rem;
                font-size: 0.72rem;
                font-weight: 500;
                color: var(--subtext);
                background: var(--card);
                border: 1px solid var(--border);
                border-radius: 8px;
            }

            .footer-dot {
                width: 6px;
                height: 6px;
                border-radius: 50%;
                background: #4ade80;
                box-shadow: 0 0 8px rgba(74, 222, 128, 0.5);
            }

            /* ── Responsive ───────────────────────────────────────── */
            @media (max-width: 1024px) {
                .hero-grid {
                    grid-template-columns: 1fr;
                    gap: 3rem;
                }

                .hero-visual {
                    order: -1;
                }

                .kpi-grid,
                .feature-grid {
                    grid-template-columns: repeat(2, 1fr);
                }

                .why-grid {
                    grid-template-columns: repeat(2, 1fr);
                }
            }

            @media (max-width: 768px) {
                .timeline {
                    flex-direction: column;
                    gap: 2rem;
                    padding-top: 0;
                }

                .timeline-rail {
                    display: none;
                }

                .timeline-step {
                    flex-direction: row;
                    text-align: left;
                    gap: 1.25rem;
                    padding: 0;
                }

                .timeline-node {
                    margin-bottom: 0;
                    flex-shrink: 0;
                }

                .timeline-index {
                    position: static;
                    margin-bottom: 0.25rem;
                }

                .timeline-step p {
                    max-width: none;
                }

                .footer-top {
                    grid-template-columns: 1fr 1fr;
                }
            }

            @media (max-width: 600px) {
                .kpi-grid,
                .feature-grid,
                .why-grid {
                    grid-template-columns: 1fr;
                }

                .hero-actions {
                    flex-direction: column;
                }

                .btn {
                    width: 100%;
                }

                .workflow-section,
                .why-section {
                    padding: 2.5rem 1.25rem;
                }

                .footer-top {
                    grid-template-columns: 1fr;
                }

                .site-footer {
                    margin: 0 -1rem;
                    padding: 0 1.25rem 2rem;
                }

                .dash-body {
                    grid-template-columns: 1fr;
                }

                .dash-sidebar {
                    display: none;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero():
    """Render the hero section with headline and call-to-action buttons."""
    st.markdown(
        """
        <section class="hero-section">
            <div class="hero-glow hero-glow-a"></div>
            <div class="hero-glow hero-glow-b"></div>
            <div class="hero-grid">
                <div class="hero-content">
                    <span class="hero-badge">
                        <span class="hero-badge-dot"></span>
                        AI-Powered Platform
                    </span>
                    <h1 class="hero-title">InsightFlow <span>AI</span></h1>
                    <p class="hero-headline">
                        Transform Business Data Into Intelligent Decisions
                    </p>
                    <p class="hero-description">
                        AI-Powered Business Intelligence Platform for teams
                        that need clarity, speed, and precision at enterprise scale.
                    </p>
                    <div class="hero-actions">
                        <button class="btn btn-primary">Get Started</button>
                        <button class="btn btn-secondary">View Demo</button>
                    </div>
                </div>
                <div class="hero-visual">
                    <div class="dash-glow-ring"></div>
                    <div class="dash-frame">
                        <div class="dash-topbar">
                            <span class="dash-dot red"></span>
                            <span class="dash-dot yellow"></span>
                            <span class="dash-dot green"></span>
                            <span class="dash-topbar-title">
                                InsightFlow Analytics
                            </span>
                        </div>
                        <div class="dash-body">
                            <div class="dash-sidebar">
                                <div class="dash-nav-item active"></div>
                                <div class="dash-nav-item"></div>
                                <div class="dash-nav-item"></div>
                                <div class="dash-nav-item"></div>
                            </div>
                            <div class="dash-main">
                                <div class="dash-widget">
                                    <div class="dash-widget-label">Revenue</div>
                                    <div class="dash-kpi-row">
                                        <div class="dash-kpi">
                                            <div class="dash-kpi-val">$2.4M</div>
                                            <div class="dash-kpi-lbl">Total</div>
                                        </div>
                                        <div class="dash-kpi">
                                            <div class="dash-kpi-val">+18%</div>
                                            <div class="dash-kpi-lbl">Growth</div>
                                        </div>
                                    </div>
                                </div>
                                <div class="dash-widget">
                                    <div class="dash-widget-label">Pipeline</div>
                                    <div class="dash-bars">
                                        <div class="dash-bar" style="height:55%"></div>
                                        <div class="dash-bar" style="height:80%"></div>
                                        <div class="dash-bar" style="height:45%"></div>
                                        <div class="dash-bar" style="height:90%"></div>
                                        <div class="dash-bar" style="height:65%"></div>
                                    </div>
                                </div>
                                <div class="dash-widget wide">
                                    <div class="dash-widget-label">
                                        Performance Trend
                                    </div>
                                    <div class="dash-line-chart">
                                        <svg viewBox="0 0 200 48" preserveAspectRatio="none">
                                            <polyline
                                                points="0,40 30,32 60,36 90,18 120,24 150,10 180,14 200,6"
                                                fill="none"
                                                stroke="#8B5CF6"
                                                stroke-width="2"
                                            />
                                            <polyline
                                                points="0,40 30,32 60,36 90,18 120,24 150,10 180,14 200,6 200,48 0,48"
                                                fill="url(#grad)"
                                                opacity="0.25"
                                            />
                                            <defs>
                                                <linearGradient id="grad" x1="0" y1="0" x2="0" y2="1">
                                                    <stop offset="0%" stop-color="#7C3AED"/>
                                                    <stop offset="100%" stop-color="transparent"/>
                                                </linearGradient>
                                            </defs>
                                        </svg>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_kpi_stats():
    """Render KPI metric cards below the hero section."""
    st.markdown(
        """
        <div class="kpi-grid">
            <div class="kpi-card glass-card">
                <div class="kpi-top">
                    <div class="kpi-icon-wrap icon-box">
                        <svg viewBox="0 0 24 24"><path d="M4 7h16M4 12h10M4 17h14"/></svg>
                    </div>
                    <span class="kpi-trend">+24%</span>
                </div>
                <p class="kpi-value">2.4M+</p>
                <p class="kpi-label">Rows Processed</p>
                <p class="kpi-detail">Enterprise data analyzed at scale</p>
            </div>
            <div class="kpi-card glass-card">
                <div class="kpi-top">
                    <div class="kpi-icon-wrap icon-box">
                        <svg viewBox="0 0 24 24"><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/></svg>
                    </div>
                    <span class="kpi-trend">+3.2%</span>
                </div>
                <p class="kpi-value">97.8%</p>
                <p class="kpi-label">Prediction Accuracy</p>
                <p class="kpi-detail">Validated model precision</p>
            </div>
            <div class="kpi-card glass-card">
                <div class="kpi-top">
                    <div class="kpi-icon-wrap icon-box">
                        <svg viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>
                    </div>
                    <span class="kpi-trend">+156</span>
                </div>
                <p class="kpi-value">1,200+</p>
                <p class="kpi-label">Dashboards Created</p>
                <p class="kpi-detail">Live views across organizations</p>
            </div>
            <div class="kpi-card glass-card">
                <div class="kpi-top">
                    <div class="kpi-icon-wrap icon-box">
                        <svg viewBox="0 0 24 24"><path d="M12 2a4 4 0 0 1 4 4c0 1.5-.8 2.8-2 3.4V12h4a2 2 0 0 1 2 2v1h-2v5H8v-5H6v-1a2 2 0 0 1 2-2h4V9.4A4 4 0 0 1 12 2z"/></svg>
                    </div>
                    <span class="kpi-trend">+12K</span>
                </div>
                <p class="kpi-value">48K+</p>
                <p class="kpi-label">AI Insights Generated</p>
                <p class="kpi-detail">Automated recommendations delivered</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_workflow():
    """Render the end-to-end data workflow section."""
    st.markdown(
        """
        <section class="page-section workflow-section">
            <div class="section-header center">
                <span class="section-label">Pipeline</span>
                <h2 class="section-title">From raw data to intelligence</h2>
                <p class="section-subtitle">
                    A refined five-stage pipeline that transforms CSV exports
                    into executive-ready insights — seamlessly and at scale.
                </p>
            </div>
            <div class="timeline">
                <div class="timeline-rail"></div>
                <div class="timeline-step">
                    <span class="timeline-index">01</span>
                    <div class="timeline-node icon-box lg">
                        <svg viewBox="0 0 24 24"><path d="M12 16V4M12 16l-4-4M12 16l4-4M4 20h16"/></svg>
                    </div>
                    <h4>Upload CSV</h4>
                    <p>Import datasets instantly</p>
                </div>
                <div class="timeline-step">
                    <span class="timeline-index">02</span>
                    <div class="timeline-node icon-box lg">
                        <svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/></svg>
                    </div>
                    <h4>Clean Data</h4>
                    <p>Normalize and validate</p>
                </div>
                <div class="timeline-step">
                    <span class="timeline-index">03</span>
                    <div class="timeline-node icon-box lg">
                        <svg viewBox="0 0 24 24"><path d="M3 3v18h18"/><path d="M7 16l4-6 4 3 5-8"/></svg>
                    </div>
                    <h4>Analyze</h4>
                    <p>Surface key metrics</p>
                </div>
                <div class="timeline-step">
                    <span class="timeline-index">04</span>
                    <div class="timeline-node icon-box lg">
                        <svg viewBox="0 0 24 24"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
                    </div>
                    <h4>Forecast</h4>
                    <p>Predict revenue trends</p>
                </div>
                <div class="timeline-step">
                    <span class="timeline-index">05</span>
                    <div class="timeline-node icon-box lg">
                        <svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M9 15l2 2 4-4"/></svg>
                    </div>
                    <h4>Generate Reports</h4>
                    <p>Export executive PDFs</p>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_features():
    """Render the feature cards section."""
    st.markdown(
        """
        <section class="page-section">
            <div class="section-header">
                <span class="section-label">Capabilities</span>
                <h2 class="section-title">Built for modern revenue teams</h2>
                <p class="section-subtitle">
                    Every module engineered for clarity, performance, and
                    the precision enterprise leaders demand.
                </p>
            </div>
            <div class="feature-grid">
                <div class="feature-card glass-card">
                    <div class="icon-wrap icon-box">
                        <svg viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>
                    </div>
                    <h3>Interactive Dashboards</h3>
                    <p>
                        Real-time, filterable views of KPIs, trends, and
                        team performance — designed for decision-makers.
                    </p>
                    <span class="feature-tag">Live Data</span>
                </div>
                <div class="feature-card glass-card">
                    <div class="icon-wrap icon-box">
                        <svg viewBox="0 0 24 24"><path d="M3 3v18h18"/><path d="M7 16l4-6 4 3 5-8"/></svg>
                    </div>
                    <h3>Sales Forecasting</h3>
                    <p>
                        Project pipeline outcomes and revenue with validated
                        models built on historical signals.
                    </p>
                    <span class="feature-tag">Predictive</span>
                </div>
                <div class="feature-card glass-card">
                    <div class="icon-wrap icon-box">
                        <svg viewBox="0 0 24 24"><path d="M12 2a4 4 0 0 1 4 4c0 1.5-.8 2.8-2 3.4V12h4a2 2 0 0 1 2 2v1h-2v5H8v-5H6v-1a2 2 0 0 1 2-2h4V9.4A4 4 0 0 1 12 2z"/></svg>
                    </div>
                    <h3>AI Business Insights</h3>
                    <p>
                        Uncover hidden patterns and receive actionable
                        recommendations from complex datasets.
                    </p>
                    <span class="feature-tag">Intelligent</span>
                </div>
                <div class="feature-card glass-card">
                    <div class="icon-wrap icon-box">
                        <svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M9 15l2 2 4-4"/></svg>
                    </div>
                    <h3>PDF Executive Reports</h3>
                    <p>
                        Generate polished, board-ready documents that
                        communicate results with clarity and impact.
                    </p>
                    <span class="feature-tag">Export Ready</span>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_why():
    """Render the 'Why InsightFlow?' value proposition section."""
    st.markdown(
        """
        <section class="page-section why-section">
            <div class="section-header center">
                <span class="section-label">Why Us</span>
                <h2 class="section-title">Why Companies Choose InsightFlow AI</h2>
                <p class="section-subtitle">
                    Trusted by forward-thinking organizations that refuse to
                    compromise on speed, security, or intelligence.
                </p>
            </div>
            <div class="why-grid">
                <div class="why-card glass-card">
                    <div class="icon-wrap icon-box">
                        <svg viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                    </div>
                    <h3>Enterprise Security</h3>
                    <p>
                        SOC 2-ready architecture with encryption at rest
                        and in transit across every layer.
                    </p>
                </div>
                <div class="why-card glass-card">
                    <div class="icon-wrap icon-box">
                        <svg viewBox="0 0 24 24"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>
                    </div>
                    <h3>Real-time Processing</h3>
                    <p>
                        Query millions of records in seconds with
                        sub-second response times at any scale.
                    </p>
                </div>
                <div class="why-card glass-card">
                    <div class="icon-wrap icon-box">
                        <svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/></svg>
                    </div>
                    <h3>AI-Powered Insights</h3>
                    <p>
                        Machine learning models surface patterns and
                        recommendations humans would miss.
                    </p>
                </div>
                <div class="why-card glass-card">
                    <div class="icon-wrap icon-box">
                        <svg viewBox="0 0 24 24"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
                    </div>
                    <h3>Scalable Architecture</h3>
                    <p>
                        Cloud-native infrastructure that grows with your
                        data volume and team size effortlessly.
                    </p>
                </div>
                <div class="why-card glass-card">
                    <div class="icon-wrap icon-box">
                        <svg viewBox="0 0 24 24"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>
                    </div>
                    <h3>Seamless Integration</h3>
                    <p>
                        Connect CRM, ERP, and warehouse sources through
                        native connectors and open APIs.
                    </p>
                </div>
                <div class="why-card glass-card">
                    <div class="icon-wrap icon-box">
                        <svg viewBox="0 0 24 24"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
                    </div>
                    <h3>Executive Reporting</h3>
                    <p>
                        Board-ready PDF exports with branded templates
                        and automated scheduling built in.
                    </p>
                </div>
            </div>
        </section>

        <section class="page-section tech-section">
            <span class="section-label">Technology</span>
            <h2 class="section-title">Powered by a modern stack</h2>
            <p class="section-subtitle">
                Built on proven, production-grade technologies for
                reliability, performance, and developer velocity.
            </p>
            <div class="tech-grid">
                <span class="tech-pill"><span class="tech-dot"></span>Python</span>
                <span class="tech-pill"><span class="tech-dot"></span>Streamlit</span>
                <span class="tech-pill"><span class="tech-dot"></span>Pandas</span>
                <span class="tech-pill"><span class="tech-dot"></span>NumPy</span>
                <span class="tech-pill"><span class="tech-dot"></span>Plotly</span>
                <span class="tech-pill"><span class="tech-dot"></span>Scikit-learn</span>
                <span class="tech-pill"><span class="tech-dot"></span>PostgreSQL</span>
                <span class="tech-pill"><span class="tech-dot"></span>Redis</span>
                <span class="tech-pill"><span class="tech-dot"></span>Docker</span>
                <span class="tech-pill"><span class="tech-dot"></span>REST API</span>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_footer():
    """Render the site footer."""
    st.markdown(
        """
        <footer class="site-footer">
            <div class="footer-divider"></div>
            <div class="footer-inner">
                <div class="footer-top">
                    <div class="footer-brand">
                        <p class="footer-brand-name">InsightFlow <span>AI</span></p>
                        <p class="footer-brand-desc">
                            Enterprise business intelligence for teams that
                            demand clarity, speed, and precision at scale.
                        </p>
                        <div class="footer-social">
                            <span class="footer-social-icon icon-box">
                                <svg viewBox="0 0 24 24"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-4 0v7h-4v-7a6 6 0 0 1 6-6zM2 9h4v12H2z"/><circle cx="4" cy="4" r="2"/></svg>
                            </span>
                            <span class="footer-social-icon icon-box">
                                <svg viewBox="0 0 24 24"><path d="M23 3a10.9 10.9 0 0 1-3.14 1.53 4.48 4.48 0 0 0-7.86 3v1A10.66 10.66 0 0 1 3 4s-4 9 5 13a11.64 11.64 0 0 1-7 2c9 5 20 0 20-11.5a4.5 4.5 0 0 0-.08-.83A7.72 7.72 0 0 0 23 3z"/></svg>
                            </span>
                            <span class="footer-social-icon icon-box">
                                <svg viewBox="0 0 24 24"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/></svg>
                            </span>
                        </div>
                    </div>
                    <div class="footer-col">
                        <h5>Product</h5>
                        <p>Dashboards</p>
                        <p>Forecasting</p>
                        <p>AI Insights</p>
                        <p>Reports</p>
                    </div>
                    <div class="footer-col">
                        <h5>Platform</h5>
                        <p>Data Pipeline</p>
                        <p>Security</p>
                        <p>Integrations</p>
                        <p>API Access</p>
                    </div>
                    <div class="footer-col">
                        <h5>Company</h5>
                        <p>About</p>
                        <p>Careers</p>
                        <p>Contact</p>
                        <p>Legal</p>
                    </div>
                </div>
                <div class="footer-bottom">
                    <p class="footer-copy">
                        &copy; 2026 InsightFlow AI. All rights reserved.
                    </p>
                    <span class="footer-badge">
                        <span class="footer-dot"></span>
                        All systems operational
                    </span>
                </div>
            </div>
        </footer>
        """,
        unsafe_allow_html=True,
    )


def render_landing_page():
    """Assemble and display the full landing page."""
    inject_styles()
    render_hero()
    render_kpi_stats()
    render_workflow()
    render_features()
    render_why()
    render_footer()


def main():
    """Bootstrap the application."""
    configure_page()
    render_landing_page()


if __name__ == "__main__":
    main()
