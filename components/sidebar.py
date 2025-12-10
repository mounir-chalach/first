"""
Sidebar component for MASI Dashboard
"""

import streamlit as st
from datetime import datetime, date
from typing import Optional, List, Tuple


def render_sidebar(bloomberg_connected: bool = False,
                  current_date: Optional[date] = None) -> Tuple[date, bool, str]:
    """
    Render the sidebar navigation and controls

    Args:
        bloomberg_connected: Whether Bloomberg is connected
        current_date: Current analysis date

    Returns:
        Tuple of (selected_date, use_bloomberg, selected_tab)
    """
    if current_date is None:
        current_date = datetime.now().date()

    with st.sidebar:
        # Logo/Title
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h1 style="color: #1f77b4; font-size: 2rem;">📊</h1>
            <h2 style="color: #1f77b4; margin: 0;">MASI Dashboard</h2>
            <p style="color: #666; font-size: 0.9rem;">Market Sentiment Analysis</p>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # Date Selection
        st.subheader("📅 Date Selection")
        selected_date = st.date_input(
            "Analysis Date",
            value=current_date,
            max_value=current_date,
            help="Select date for market analysis"
        )

        st.divider()

        # Data Source
        st.subheader("🔌 Data Source")

        if bloomberg_connected:
            st.success("✅ Bloomberg Connected")
            use_bloomberg = True
        else:
            st.warning("⚠️ Bloomberg Not Connected")
            use_bloomberg = st.checkbox(
                "Use Synthetic Data",
                value=True,
                help="Use generated synthetic data for testing"
            )

        st.divider()

        # Navigation
        st.subheader("📱 Navigation")
        tabs = [
            "📈 Dashboard",
            "📊 Market Analysis",
            "📅 Historical Data",
            "⚙️ Configuration",
            "🔍 Backtesting"
        ]

        selected_tab = st.radio(
            "Select Page",
            tabs,
            label_visibility="collapsed"
        )

        st.divider()

        # Quick Info
        st.subheader("ℹ️ Quick Info")
        st.info(f"""
        **Market**: MASI
        **Date**: {selected_date.strftime('%Y-%m-%d')}
        **Status**: {'Live' if bloomberg_connected else 'Simulation'}
        """)

        st.divider()

        # Footer
        st.caption("© 2025 MASI Sentiment Dashboard")
        st.caption("Powered by Bloomberg Terminal")

    return selected_date, use_bloomberg, selected_tab


def render_sidebar_metrics(metrics: dict):
    """
    Render quick metrics in the sidebar

    Args:
        metrics: Dictionary of metric_name: metric_value
    """
    with st.sidebar:
        st.divider()
        st.subheader("⚡ Quick Stats")

        for metric_name, metric_value in metrics.items():
            st.metric(label=metric_name, value=metric_value)


def render_sidebar_settings():
    """Render settings panel in sidebar"""
    with st.sidebar:
        st.divider()
        st.subheader("⚙️ Settings")

        with st.expander("Display Options"):
            show_grid = st.checkbox("Show Grid", value=True)
            show_legend = st.checkbox("Show Legend", value=True)
            theme = st.selectbox("Color Theme", ["Default", "Dark", "Light"])

        with st.expander("Data Options"):
            cache_enabled = st.checkbox("Enable Cache", value=True)
            auto_refresh = st.checkbox("Auto Refresh", value=False)
            if auto_refresh:
                refresh_interval = st.slider("Refresh Interval (min)", 1, 60, 5)

        return {
            'show_grid': show_grid,
            'show_legend': show_legend,
            'theme': theme,
            'cache_enabled': cache_enabled,
            'auto_refresh': auto_refresh
        }
