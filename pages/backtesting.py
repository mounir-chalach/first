"""
Backtesting Page for MASI Dashboard
Test sentiment strategies on historical data
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
from data_handler import DataHandler
from sentiment_calculator import MASISentimentCalculator
from utils.formatters import format_number, format_percentage


def render():
    """Render the backtesting page"""
    st.title("🔍 Backtesting")
    st.markdown("Test sentiment-based trading strategies on historical data")

    # Initialize
    data_handler = DataHandler()
    calculator = MASISentimentCalculator()

    # Strategy configuration
    st.subheader("⚙️ Strategy Configuration")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Time Period**")
        start_date = st.date_input(
            "Start Date",
            value=datetime.now().date() - timedelta(days=90),
            max_value=datetime.now().date()
        )
        end_date = st.date_input(
            "End Date",
            value=datetime.now().date(),
            max_value=datetime.now().date()
        )

    with col2:
        st.markdown("**Entry Conditions**")
        entry_threshold = st.slider(
            "Buy Signal Threshold",
            -100, 100, 30,
            help="Enter long position when sentiment >= this value"
        )
        exit_threshold = st.slider(
            "Sell Signal Threshold",
            -100, 100, -30,
            help="Exit position when sentiment <= this value"
        )

    with col3:
        st.markdown("**Position Sizing**")
        initial_capital = st.number_input(
            "Initial Capital (MAD)",
            1000, 10000000,
            100000,
            step=10000
        )
        position_size = st.slider(
            "Position Size (%)",
            10, 100, 100,
            help="% of capital to invest per trade"
        )

    st.divider()

    # Run backtest button
    if st.button("🚀 Run Backtest", type="primary"):
        if start_date >= end_date:
            st.error("Start date must be before end date")
            return

        with st.spinner("Running backtest..."):
            # Generate historical sentiment data
            historical_data = []
            current_date = start_date
            days = (end_date - start_date).days + 1

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
                        'date': current_date,
                        'sentiment': sentiment['overall_score'],
                        'price': market_data['close'],
                        'label': sentiment['sentiment_label']
                    })

                current_date += timedelta(days=1)

                # Update progress
                progress = (current_date - start_date).days / days
                progress_bar.progress(min(progress, 1.0))

            progress_bar.empty()
            status_text.empty()

            if not historical_data:
                st.warning("No data available for backtesting")
                return

            # Run strategy simulation
            results = simulate_strategy(
                historical_data,
                entry_threshold,
                exit_threshold,
                initial_capital,
                position_size / 100
            )

            # Store in session state
            st.session_state['backtest_results'] = results
            st.session_state['backtest_data'] = historical_data

            st.success(f"✅ Backtest completed! Analyzed {len(historical_data)} trading days")

    # Display results if available
    if 'backtest_results' in st.session_state:
        results = st.session_state['backtest_results']
        historical_data = st.session_state['backtest_data']

        st.divider()

        # Performance metrics
        st.subheader("📊 Performance Metrics")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            total_return = results['total_return']
            st.metric(
                "Total Return",
                format_percentage(total_return, include_sign=True),
                delta=None
            )

        with col2:
            final_value = results['final_value']
            st.metric(
                "Final Value",
                f"MAD {format_number(final_value, decimals=0)}",
                delta=format_number(final_value - initial_capital, decimals=0)
            )

        with col3:
            total_trades = results['total_trades']
            win_rate = results['win_rate']
            st.metric(
                "Total Trades",
                total_trades,
                delta=f"{win_rate:.1f}% win rate"
            )

        with col4:
            max_drawdown = results['max_drawdown']
            st.metric(
                "Max Drawdown",
                format_percentage(abs(max_drawdown), include_sign=False),
                delta=None,
                delta_color="inverse"
            )

        st.divider()

        # Additional metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Sharpe Ratio", f"{results['sharpe_ratio']:.2f}")

        with col2:
            st.metric("Average Win", format_percentage(results['avg_win']))

        with col3:
            st.metric("Average Loss", format_percentage(results['avg_loss']))

        with col4:
            st.metric("Profit Factor", f"{results['profit_factor']:.2f}")

        st.divider()

        # Equity curve
        st.subheader("📈 Equity Curve")

        equity_df = pd.DataFrame(results['equity_curve'])

        fig = go.Figure()

        # Add equity line
        fig.add_trace(go.Scatter(
            x=equity_df['date'],
            y=equity_df['value'],
            mode='lines',
            name='Portfolio Value',
            line=dict(color='#1f77b4', width=2)
        ))

        # Add buy/sell markers
        trades_df = pd.DataFrame(results['trades'])

        if not trades_df.empty:
            buy_trades = trades_df[trades_df['action'] == 'buy']
            sell_trades = trades_df[trades_df['action'] == 'sell']

            fig.add_trace(go.Scatter(
                x=buy_trades['date'],
                y=buy_trades['portfolio_value'],
                mode='markers',
                name='Buy Signal',
                marker=dict(color='green', size=10, symbol='triangle-up')
            ))

            fig.add_trace(go.Scatter(
                x=sell_trades['date'],
                y=sell_trades['portfolio_value'],
                mode='markers',
                name='Sell Signal',
                marker=dict(color='red', size=10, symbol='triangle-down')
            ))

        # Add initial capital line
        fig.add_hline(
            y=initial_capital,
            line_dash="dash",
            line_color="gray",
            annotation_text="Initial Capital",
            annotation_position="right"
        )

        fig.update_layout(
            title="Portfolio Value Over Time",
            xaxis_title="Date",
            yaxis_title="Value (MAD)",
            hovermode='x unified',
            height=500
        )

        st.plotly_chart(fig, use_container_width=True)

        st.divider()

        # Drawdown chart
        st.subheader("📉 Drawdown Analysis")

        drawdown_fig = go.Figure()

        drawdown_fig.add_trace(go.Scatter(
            x=equity_df['date'],
            y=equity_df['drawdown'],
            mode='lines',
            fill='tozeroy',
            name='Drawdown',
            line=dict(color='red', width=1),
            fillcolor='rgba(255, 0, 0, 0.2)'
        ))

        drawdown_fig.update_layout(
            title="Portfolio Drawdown",
            xaxis_title="Date",
            yaxis_title="Drawdown (%)",
            hovermode='x unified',
            height=300
        )

        st.plotly_chart(drawdown_fig, use_container_width=True)

        st.divider()

        # Trade log
        st.subheader("📋 Trade Log")

        if trades_df.empty:
            st.info("No trades executed during this period")
        else:
            # Format trades for display
            display_trades = trades_df.copy()
            display_trades['date'] = pd.to_datetime(display_trades['date']).dt.strftime('%Y-%m-%d')
            display_trades['price'] = display_trades['price'].apply(lambda x: f"{x:,.2f}")
            display_trades['sentiment'] = display_trades['sentiment'].apply(lambda x: f"{x:.1f}")
            display_trades['portfolio_value'] = display_trades['portfolio_value'].apply(lambda x: f"{x:,.2f}")

            if 'return' in display_trades.columns:
                display_trades['return'] = display_trades['return'].apply(
                    lambda x: f"{x:+.2f}%" if pd.notna(x) else "N/A"
                )

            st.dataframe(
                display_trades,
                use_container_width=True,
                hide_index=True
            )

        st.divider()

        # Strategy summary
        st.subheader("📝 Strategy Summary")

        summary_text = f"""
        **Strategy Parameters:**
        - Entry Threshold: {entry_threshold}
        - Exit Threshold: {exit_threshold}
        - Initial Capital: MAD {initial_capital:,}
        - Position Size: {position_size}%

        **Performance:**
        - Total Return: {format_percentage(total_return, include_sign=True)}
        - Final Value: MAD {final_value:,.2f}
        - Total Trades: {total_trades}
        - Win Rate: {win_rate:.1f}%
        - Max Drawdown: {format_percentage(abs(max_drawdown), include_sign=False)}
        - Sharpe Ratio: {results['sharpe_ratio']:.2f}
        """

        st.markdown(summary_text)


def simulate_strategy(historical_data, entry_threshold, exit_threshold,
                     initial_capital, position_size):
    """
    Simulate a sentiment-based trading strategy

    Args:
        historical_data: List of historical data with sentiment
        entry_threshold: Sentiment threshold for entry
        exit_threshold: Sentiment threshold for exit
        initial_capital: Starting capital
        position_size: Fraction of capital to use per trade

    Returns:
        Dictionary with backtest results
    """
    cash = initial_capital
    position = 0
    position_price = 0
    trades = []
    equity_curve = []
    peak_value = initial_capital

    returns = []
    winning_trades = []
    losing_trades = []

    for i, data in enumerate(historical_data):
        date = data['date']
        sentiment = data['sentiment']
        price = data['price']

        portfolio_value = cash + (position * price)
        equity_curve.append({
            'date': date,
            'value': portfolio_value,
            'drawdown': ((portfolio_value - peak_value) / peak_value * 100) if peak_value > 0 else 0
        })

        peak_value = max(peak_value, portfolio_value)

        # Trading logic
        if position == 0 and sentiment >= entry_threshold:
            # Buy signal
            investment = cash * position_size
            position = investment / price
            cash -= investment
            position_price = price

            trades.append({
                'date': date,
                'action': 'buy',
                'price': price,
                'sentiment': sentiment,
                'shares': position,
                'portfolio_value': portfolio_value
            })

        elif position > 0 and sentiment <= exit_threshold:
            # Sell signal
            proceeds = position * price
            cash += proceeds

            trade_return = ((price - position_price) / position_price) * 100
            returns.append(trade_return)

            if trade_return > 0:
                winning_trades.append(trade_return)
            else:
                losing_trades.append(trade_return)

            trades.append({
                'date': date,
                'action': 'sell',
                'price': price,
                'sentiment': sentiment,
                'shares': position,
                'return': trade_return,
                'portfolio_value': cash
            })

            position = 0
            position_price = 0

    # Close any open position at the end
    if position > 0:
        final_price = historical_data[-1]['price']
        proceeds = position * final_price
        cash += proceeds

        trade_return = ((final_price - position_price) / position_price) * 100
        returns.append(trade_return)

        if trade_return > 0:
            winning_trades.append(trade_return)
        else:
            losing_trades.append(trade_return)

        position = 0

    final_value = cash
    total_return = ((final_value - initial_capital) / initial_capital) * 100

    # Calculate metrics
    total_trades = len([t for t in trades if t['action'] == 'buy'])
    win_rate = (len(winning_trades) / total_trades * 100) if total_trades > 0 else 0

    avg_win = np.mean(winning_trades) if winning_trades else 0
    avg_loss = np.mean(losing_trades) if losing_trades else 0

    total_wins = sum(winning_trades) if winning_trades else 0
    total_losses = abs(sum(losing_trades)) if losing_trades else 0
    profit_factor = (total_wins / total_losses) if total_losses > 0 else 0

    # Sharpe ratio (simplified)
    if returns:
        avg_return = np.mean(returns)
        std_return = np.std(returns)
        sharpe_ratio = (avg_return / std_return) if std_return > 0 else 0
    else:
        sharpe_ratio = 0

    # Max drawdown
    max_drawdown = min([eq['drawdown'] for eq in equity_curve]) if equity_curve else 0

    return {
        'final_value': final_value,
        'total_return': total_return,
        'total_trades': total_trades,
        'win_rate': win_rate,
        'avg_win': avg_win,
        'avg_loss': avg_loss,
        'profit_factor': profit_factor,
        'sharpe_ratio': sharpe_ratio,
        'max_drawdown': max_drawdown,
        'trades': trades,
        'equity_curve': equity_curve,
        'returns': returns
    }
