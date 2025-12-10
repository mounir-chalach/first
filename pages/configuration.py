"""
Configuration Page for MASI Dashboard
Manage sentiment weights, thresholds, and system settings
"""

import streamlit as st
import json
from pathlib import Path
from config import (
    SENTIMENT_WEIGHTS,
    THRESHOLDS,
    TECHNICAL_CONFIG,
    BREADTH_THRESHOLDS,
    CACHE_CONFIG,
    COLORS
)


def render():
    """Render the configuration page"""
    st.title("⚙️ Configuration")
    st.markdown("Customize sentiment calculation and dashboard settings")

    # Create tabs for different configuration sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎯 Sentiment Weights",
        "📊 Thresholds",
        "📈 Technical Indicators",
        "💾 Cache Settings",
        "🎨 Display Settings"
    ])

    # Tab 1: Sentiment Weights
    with tab1:
        st.subheader("Sentiment Component Weights")
        st.info("Adjust the importance of each sentiment component. Total must equal 100%.")

        col1, col2 = st.columns([2, 1])

        with col1:
            # Weight sliders
            breadth_weight = st.slider(
                "📊 Breadth (Advances/Declines)",
                0, 100,
                int(SENTIMENT_WEIGHTS['breadth'] * 100),
                help="Market breadth analysis weight"
            )

            momentum_weight = st.slider(
                "🚀 Momentum (Price Action)",
                0, 100,
                int(SENTIMENT_WEIGHTS['momentum'] * 100),
                help="Price momentum indicators weight"
            )

            trend_weight = st.slider(
                "📈 Trend (Moving Averages)",
                0, 100,
                int(SENTIMENT_WEIGHTS['trend'] * 100),
                help="Trend analysis weight"
            )

            volume_weight = st.slider(
                "💧 Volume Analysis",
                0, 100,
                int(SENTIMENT_WEIGHTS['volume'] * 100),
                help="Volume analysis weight"
            )

            total_weight = breadth_weight + momentum_weight + trend_weight + volume_weight

            if total_weight != 100:
                st.error(f"⚠️ Total weight is {total_weight}%. Must equal 100%!")
            else:
                st.success("✅ Weights are balanced!")

        with col2:
            st.metric("Total Weight", f"{total_weight}%")

            if total_weight == 100:
                st.markdown("**Current Allocation:**")
                st.markdown(f"- Breadth: {breadth_weight}%")
                st.markdown(f"- Momentum: {momentum_weight}%")
                st.markdown(f"- Trend: {trend_weight}%")
                st.markdown(f"- Volume: {volume_weight}%")

        st.divider()

        if st.button("💾 Save Weight Configuration", disabled=(total_weight != 100)):
            # Save configuration
            new_weights = {
                'breadth': breadth_weight / 100,
                'momentum': momentum_weight / 100,
                'trend': trend_weight / 100,
                'volume': volume_weight / 100
            }
            save_config('sentiment_weights', new_weights)
            st.success("✅ Weight configuration saved!")

    # Tab 2: Thresholds
    with tab2:
        st.subheader("Sentiment Score Thresholds")
        st.info("Define the boundaries for sentiment classifications (-100 to 100 scale)")

        col1, col2 = st.columns(2)

        with col1:
            very_bullish = st.number_input(
                "Very Bullish Threshold",
                -100, 100,
                int(THRESHOLDS['very_bullish']),
                help="Score above this is Very Bullish"
            )

            bullish = st.number_input(
                "Bullish Threshold",
                -100, 100,
                int(THRESHOLDS['bullish']),
                help="Score above this is Bullish"
            )

            neutral = st.number_input(
                "Neutral Threshold",
                -100, 100,
                int(THRESHOLDS['neutral']),
                help="Score above this is Neutral"
            )

            bearish = st.number_input(
                "Bearish Threshold",
                -100, 100,
                int(THRESHOLDS['bearish']),
                help="Score above this is Bearish"
            )

        with col2:
            # Visualization
            st.markdown("**Sentiment Ranges:**")

            st.markdown(f"""
            - 🚀 **Very Bullish**: {very_bullish} to 100
            - ↗️ **Bullish**: {bullish} to {very_bullish}
            - ➡️ **Neutral**: {neutral} to {bullish}
            - ↘️ **Bearish**: {bearish} to {neutral}
            - 📉 **Very Bearish**: -100 to {bearish}
            """)

        # Validate thresholds
        if not (bearish < neutral < bullish < very_bullish):
            st.error("⚠️ Thresholds must be in ascending order!")
        else:
            st.success("✅ Thresholds are valid!")

        st.divider()

        if st.button("💾 Save Threshold Configuration"):
            new_thresholds = {
                'very_bullish': very_bullish,
                'bullish': bullish,
                'neutral': neutral,
                'bearish': bearish,
                'very_bearish': -100
            }
            save_config('thresholds', new_thresholds)
            st.success("✅ Threshold configuration saved!")

    # Tab 3: Technical Indicators
    with tab3:
        st.subheader("Technical Indicator Settings")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**RSI Settings**")
            rsi_period = st.number_input(
                "RSI Period",
                5, 50,
                TECHNICAL_CONFIG['rsi_period']
            )

            st.markdown("**MACD Settings**")
            macd_fast = st.number_input(
                "MACD Fast Period",
                5, 50,
                TECHNICAL_CONFIG['macd_fast']
            )
            macd_slow = st.number_input(
                "MACD Slow Period",
                10, 100,
                TECHNICAL_CONFIG['macd_slow']
            )
            macd_signal = st.number_input(
                "MACD Signal Period",
                5, 20,
                TECHNICAL_CONFIG['macd_signal']
            )

        with col2:
            st.markdown("**Moving Average Settings**")
            ma_short = st.number_input(
                "Short MA Period",
                5, 50,
                TECHNICAL_CONFIG['ma_short']
            )
            ma_medium = st.number_input(
                "Medium MA Period",
                20, 100,
                TECHNICAL_CONFIG['ma_medium']
            )
            ma_long = st.number_input(
                "Long MA Period",
                100, 300,
                TECHNICAL_CONFIG['ma_long']
            )

            st.markdown("**Stochastic Settings**")
            stochastic_period = st.number_input(
                "Stochastic Period",
                5, 30,
                TECHNICAL_CONFIG['stochastic_period']
            )

        st.divider()

        if st.button("💾 Save Technical Configuration"):
            new_technical = {
                'rsi_period': rsi_period,
                'macd_fast': macd_fast,
                'macd_slow': macd_slow,
                'macd_signal': macd_signal,
                'ma_short': ma_short,
                'ma_medium': ma_medium,
                'ma_long': ma_long,
                'stochastic_period': stochastic_period
            }
            save_config('technical_config', new_technical)
            st.success("✅ Technical configuration saved!")

    # Tab 4: Cache Settings
    with tab4:
        st.subheader("Cache Management")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Cache TTL Settings (seconds)**")

            default_ttl = st.number_input(
                "Default TTL",
                60, 86400,
                CACHE_CONFIG['default_ttl']
            )
            market_data_ttl = st.number_input(
                "Market Data TTL",
                60, 3600,
                CACHE_CONFIG['market_data_ttl']
            )
            sentiment_ttl = st.number_input(
                "Sentiment TTL",
                60, 7200,
                CACHE_CONFIG['sentiment_ttl']
            )
            historical_ttl = st.number_input(
                "Historical Data TTL",
                3600, 604800,
                CACHE_CONFIG['historical_ttl']
            )

        with col2:
            st.markdown("**Cache Management**")

            if st.button("🗑️ Clear All Cache"):
                from utils.cache import clear_cache
                clear_cache()
                st.success("✅ All cache cleared!")

            if st.button("🧹 Clear Expired Cache"):
                from utils.cache import clear_expired_cache
                count = clear_expired_cache()
                st.success(f"✅ Cleared {count} expired cache entries!")

            st.info(f"""
            **Current Settings:**
            - Default: {default_ttl}s ({default_ttl // 60}min)
            - Market: {market_data_ttl}s ({market_data_ttl // 60}min)
            - Sentiment: {sentiment_ttl}s ({sentiment_ttl // 60}min)
            - Historical: {historical_ttl}s ({historical_ttl // 3600}h)
            """)

        st.divider()

        if st.button("💾 Save Cache Configuration"):
            new_cache = {
                'default_ttl': default_ttl,
                'market_data_ttl': market_data_ttl,
                'sentiment_ttl': sentiment_ttl,
                'historical_ttl': historical_ttl
            }
            save_config('cache_config', new_cache)
            st.success("✅ Cache configuration saved!")

    # Tab 5: Display Settings
    with tab5:
        st.subheader("Display and UI Settings")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Chart Settings**")
            show_grid = st.checkbox("Show Grid Lines", value=True)
            show_legend = st.checkbox("Show Legend", value=True)
            animation_enabled = st.checkbox("Enable Animations", value=True)

            st.markdown("**Number Format**")
            decimal_places = st.number_input("Decimal Places", 0, 4, 2)
            use_thousands_sep = st.checkbox("Use Thousands Separator", value=True)

        with col2:
            st.markdown("**Color Theme**")
            theme = st.selectbox(
                "Select Theme",
                ["Default", "Dark", "Light", "Custom"]
            )

            if theme == "Custom":
                primary_color = st.color_picker("Primary Color", COLORS['primary'])
                success_color = st.color_picker("Success Color", COLORS['success'])
                danger_color = st.color_picker("Danger Color", COLORS['danger'])

        st.divider()

        if st.button("💾 Save Display Configuration"):
            display_config = {
                'show_grid': show_grid,
                'show_legend': show_legend,
                'animation_enabled': animation_enabled,
                'decimal_places': decimal_places,
                'use_thousands_sep': use_thousands_sep,
                'theme': theme
            }
            save_config('display_config', display_config)
            st.success("✅ Display configuration saved!")

    # Export/Import Configuration
    st.divider()
    st.subheader("🔄 Import/Export Configuration")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📥 Export All Configurations"):
            config_data = load_all_configs()
            config_json = json.dumps(config_data, indent=2)

            st.download_button(
                label="💾 Download Configuration",
                data=config_json,
                file_name="masi_dashboard_config.json",
                mime="application/json"
            )

    with col2:
        uploaded_file = st.file_uploader("📤 Import Configuration", type=['json'])
        if uploaded_file:
            config_data = json.load(uploaded_file)
            if st.button("✅ Apply Imported Configuration"):
                save_all_configs(config_data)
                st.success("✅ Configuration imported successfully!")
                st.info("Please refresh the page to apply changes.")


def save_config(config_name: str, config_data: dict):
    """Save configuration to file"""
    config_dir = Path('data/config')
    config_dir.mkdir(parents=True, exist_ok=True)

    config_file = config_dir / f'{config_name}.json'
    with open(config_file, 'w') as f:
        json.dump(config_data, f, indent=2)


def load_config(config_name: str) -> dict:
    """Load configuration from file"""
    config_file = Path('data/config') / f'{config_name}.json'

    if config_file.exists():
        with open(config_file, 'r') as f:
            return json.load(f)
    return {}


def load_all_configs() -> dict:
    """Load all configurations"""
    configs = {
        'sentiment_weights': SENTIMENT_WEIGHTS,
        'thresholds': THRESHOLDS,
        'technical_config': TECHNICAL_CONFIG,
        'cache_config': CACHE_CONFIG
    }

    # Load saved configs if they exist
    for config_name in configs.keys():
        saved_config = load_config(config_name)
        if saved_config:
            configs[config_name] = saved_config

    return configs


def save_all_configs(configs: dict):
    """Save all configurations"""
    for config_name, config_data in configs.items():
        save_config(config_name, config_data)
