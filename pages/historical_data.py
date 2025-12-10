"""
Historical Data Page for MASI Dashboard
View and export historical sentiment data
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date, timedelta
from data_handler import DataHandler
from sentiment_calculator import MASISentimentCalculator
from bl_client import BloombergClient
from utils.formatters import format_number, format_percentage, format_date
from components.charts import create_sentiment_timeline


def render():
    """Render the historical data page"""
    st.title("📅 Historical Data")
    st.markdown("View historical market data and sentiment trends")

    # Initialize handlers
    data_handler = DataHandler()
    calculator = MASISentimentCalculator()

    # Date range selector
    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input(
            "Start Date",
            value=datetime.now().date() - timedelta(days=30),
            max_value=datetime.now().date()
        )

    with col2:
        end_date = st.date_input(
            "End Date",
            value=datetime.now().date(),
            max_value=datetime.now().date()
        )

    if start_date > end_date:
        st.error("Start date must be before end date")
        return

    # Data source selector
    data_source = st.radio(
        "Data Source",
        ["Cached Sentiment Data", "Generate from Historical Data"],
        horizontal=True
    )

    st.divider()

    # Load data button
    if st.button("📊 Load Historical Data", type="primary"):
        with st.spinner("Loading historical data..."):
            # Calculate number of days
            days = (end_date - start_date).days + 1

            if data_source == "Cached Sentiment Data":
                # Load from cache
                history = data_handler.get_sentiment_history(days=days)

                if history:
                    # Convert to DataFrame
                    df_data = []
                    for record in history:
                        df_data.append({
                            'Date': record.get('analysis_date', record.get('date')),
                            'Sentiment Score': record.get('overall_score', 0),
                            'Label': record.get('sentiment_label', 'N/A'),
                            'Breadth': record['components'].get('breadth_score', 0),
                            'Momentum': record['components'].get('momentum_score', 0),
                            'Trend': record['components'].get('trend_score', 0),
                            'Volume': record['components'].get('volume_score', 0),
                            'Confidence': record.get('confidence', 0)
                        })

                    df = pd.DataFrame(df_data)

                    # Filter by date range
                    df = df[
                        (pd.to_datetime(df['Date']).dt.date >= start_date) &
                        (pd.to_datetime(df['Date']).dt.date <= end_date)
                    ]

                    if df.empty:
                        st.warning("No cached data found for selected date range")
                        return

                    st.session_state['historical_df'] = df
                    st.success(f"Loaded {len(df)} records from cache")
                else:
                    st.warning("No cached sentiment data found")
                    return

            else:
                # Generate from historical data
                historical_data = []
                current_date = start_date

                progress_bar = st.progress(0)
                status_text = st.empty()

                while current_date <= end_date:
                    status_text.text(f"Processing {current_date}...")

                    # Get market data
                    market_data = data_handler.get_historical_data(current_date)

                    if market_data:
                        # Calculate sentiment
                        sentiment = calculator.calculate_sentiment(market_data, current_date)

                        historical_data.append({
                            'Date': current_date,
                            'Sentiment Score': sentiment['overall_score'],
                            'Label': sentiment['sentiment_label'],
                            'Breadth': sentiment['components']['breadth_score'],
                            'Momentum': sentiment['components']['momentum_score'],
                            'Trend': sentiment['components']['trend_score'],
                            'Volume': sentiment['components']['volume_score'],
                            'Confidence': sentiment['confidence']
                        })

                    current_date += timedelta(days=1)

                    # Update progress
                    progress = (current_date - start_date).days / days
                    progress_bar.progress(min(progress, 1.0))

                progress_bar.empty()
                status_text.empty()

                if historical_data:
                    df = pd.DataFrame(historical_data)
                    st.session_state['historical_df'] = df
                    st.success(f"Generated sentiment data for {len(df)} days")
                else:
                    st.warning("No data available for selected date range")
                    return

    # Display data if available
    if 'historical_df' in st.session_state:
        df = st.session_state['historical_df']

        # Summary statistics
        st.subheader("📊 Summary Statistics")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Average Sentiment",
                f"{df['Sentiment Score'].mean():.1f}",
                delta=f"{df['Sentiment Score'].iloc[-1] - df['Sentiment Score'].iloc[0]:.1f}"
            )

        with col2:
            st.metric(
                "Max Sentiment",
                f"{df['Sentiment Score'].max():.1f}",
                delta=None
            )

        with col3:
            st.metric(
                "Min Sentiment",
                f"{df['Sentiment Score'].min():.1f}",
                delta=None
            )

        with col4:
            st.metric(
                "Volatility (Std)",
                f"{df['Sentiment Score'].std():.1f}",
                delta=None
            )

        st.divider()

        # Sentiment timeline chart
        st.subheader("📈 Sentiment Timeline")

        # Prepare data for chart
        chart_df = df.copy()
        chart_df.columns = ['date' if col == 'Date' else 'sentiment_score' if col == 'Sentiment Score' else col.lower() for col in chart_df.columns]

        timeline_fig = create_sentiment_timeline(chart_df)
        st.plotly_chart(timeline_fig, use_container_width=True)

        st.divider()

        # Component breakdown
        st.subheader("🔍 Component Breakdown")

        component_fig = px.line(
            df,
            x='Date',
            y=['Breadth', 'Momentum', 'Trend', 'Volume'],
            title="Sentiment Components Over Time",
            labels={'value': 'Score', 'variable': 'Component'}
        )
        component_fig.update_layout(
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(component_fig, use_container_width=True)

        st.divider()

        # Data table
        st.subheader("📋 Data Table")

        # Format display
        display_df = df.copy()
        display_df['Date'] = pd.to_datetime(display_df['Date']).dt.strftime('%Y-%m-%d')
        display_df['Sentiment Score'] = display_df['Sentiment Score'].apply(lambda x: f"{x:.1f}")
        display_df['Breadth'] = display_df['Breadth'].apply(lambda x: f"{x:.1f}")
        display_df['Momentum'] = display_df['Momentum'].apply(lambda x: f"{x:.1f}")
        display_df['Trend'] = display_df['Trend'].apply(lambda x: f"{x:.1f}")
        display_df['Volume'] = display_df['Volume'].apply(lambda x: f"{x:.1f}")
        display_df['Confidence'] = display_df['Confidence'].apply(lambda x: f"{x:.2%}")

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        # Export options
        st.subheader("💾 Export Data")

        col1, col2, col3 = st.columns(3)

        with col1:
            # CSV export
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"masi_sentiment_{start_date}_{end_date}.csv",
                mime="text/csv"
            )

        with col2:
            # Excel export
            try:
                from io import BytesIO
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='Sentiment Data')
                excel_data = output.getvalue()

                st.download_button(
                    label="📥 Download Excel",
                    data=excel_data,
                    file_name=f"masi_sentiment_{start_date}_{end_date}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            except ImportError:
                st.info("Install openpyxl for Excel export: pip install openpyxl")

        with col3:
            # JSON export
            json_data = df.to_json(orient='records', date_format='iso')
            st.download_button(
                label="📥 Download JSON",
                data=json_data,
                file_name=f"masi_sentiment_{start_date}_{end_date}.json",
                mime="application/json"
            )
