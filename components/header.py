"""
Header component for MASI Dashboard
"""

import streamlit as st
from datetime import datetime


def render_header(title: str = "MASI Market Sentiment Dashboard",
                 subtitle: str = "Real-time Moroccan Stock Market Analysis"):
    """
    Render the dashboard header

    Args:
        title: Main title
        subtitle: Subtitle/description
    """
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #1f77b4 0%, #2ecc71 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    ">
        <h1 style="
            color: white;
            margin: 0;
            font-size: 2.5rem;
            font-weight: 700;
        ">
            📊 {title}
        </h1>
        <p style="
            color: rgba(255, 255, 255, 0.9);
            margin: 0.5rem 0 0 0;
            font-size: 1.1rem;
        ">
            {subtitle}
        </p>
        <p style="
            color: rgba(255, 255, 255, 0.7);
            margin: 0.5rem 0 0 0;
            font-size: 0.9rem;
        ">
            Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_page_header(title: str, icon: str = "📊", description: str = ""):
    """
    Render a simple page header

    Args:
        title: Page title
        icon: Emoji icon
        description: Optional description
    """
    st.markdown(f"""
    <div style="
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 1rem;
        margin-bottom: 2rem;
    ">
        <h1 style="
            color: #1f77b4;
            margin: 0;
            font-size: 2rem;
        ">
            {icon} {title}
        </h1>
        {f'<p style="color: #666; margin-top: 0.5rem;">{description}</p>' if description else ''}
    </div>
    """, unsafe_allow_html=True)


def render_section_header(title: str, icon: str = ""):
    """
    Render a section header within a page

    Args:
        title: Section title
        icon: Optional emoji icon
    """
    icon_part = f"{icon} " if icon else ""
    st.markdown(f"""
    <h2 style="
        color: #1f77b4;
        font-size: 1.5rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-left: 4px solid #1f77b4;
        padding-left: 1rem;
    ">
        {icon_part}{title}
    </h2>
    """, unsafe_allow_html=True)
