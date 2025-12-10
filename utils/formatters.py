"""
Formatting utilities for MASI Dashboard
Provides consistent number and text formatting
"""

from typing import Union, Optional


def format_number(value: Union[int, float],
                  decimals: int = 2,
                  suffix: str = "",
                  prefix: str = "") -> str:
    """
    Format a number with thousands separator and optional suffix/prefix

    Args:
        value: Number to format
        decimals: Number of decimal places
        suffix: Optional suffix (e.g., "M", "K", "%")
        prefix: Optional prefix (e.g., "$", "MAD")

    Returns:
        Formatted string

    Examples:
        >>> format_number(1234567.89)
        '1,234,567.89'
        >>> format_number(1234.5, decimals=1, suffix="M")
        '1,234.5M'
        >>> format_number(50.5, prefix="$", decimals=2)
        '$50.50'
    """
    try:
        if value is None:
            return "N/A"

        # Format with thousands separator
        formatted = f"{value:,.{decimals}f}"

        return f"{prefix}{formatted}{suffix}"
    except (ValueError, TypeError):
        return "N/A"


def format_percentage(value: Union[int, float],
                     decimals: int = 2,
                     include_sign: bool = True) -> str:
    """
    Format a number as a percentage

    Args:
        value: Value to format (e.g., 5 for 5%)
        decimals: Number of decimal places
        include_sign: Include + sign for positive values

    Returns:
        Formatted percentage string

    Examples:
        >>> format_percentage(5.234)
        '+5.23%'
        >>> format_percentage(-2.1, decimals=1)
        '-2.1%'
        >>> format_percentage(0.5, include_sign=False)
        '0.50%'
    """
    try:
        if value is None:
            return "N/A"

        sign = ""
        if include_sign and value > 0:
            sign = "+"
        elif value < 0:
            sign = "-"
            value = abs(value)

        formatted = f"{value:.{decimals}f}"
        return f"{sign}{formatted}%"
    except (ValueError, TypeError):
        return "N/A"


def format_currency(value: Union[int, float],
                   currency: str = "MAD",
                   decimals: int = 2) -> str:
    """
    Format a number as currency

    Args:
        value: Amount to format
        currency: Currency code (default: MAD for Moroccan Dirham)
        decimals: Number of decimal places

    Returns:
        Formatted currency string

    Examples:
        >>> format_currency(1234567.89)
        'MAD 1,234,567.89'
        >>> format_currency(500, currency="USD", decimals=0)
        'USD 500'
    """
    try:
        if value is None:
            return "N/A"

        formatted = f"{value:,.{decimals}f}"
        return f"{currency} {formatted}"
    except (ValueError, TypeError):
        return "N/A"


def format_large_number(value: Union[int, float],
                       decimals: int = 1) -> str:
    """
    Format large numbers with K, M, B suffixes

    Args:
        value: Number to format
        decimals: Number of decimal places

    Returns:
        Formatted string with appropriate suffix

    Examples:
        >>> format_large_number(1234)
        '1.2K'
        >>> format_large_number(1234567)
        '1.2M'
        >>> format_large_number(1234567890)
        '1.2B'
    """
    try:
        if value is None:
            return "N/A"

        abs_value = abs(value)
        sign = "-" if value < 0 else ""

        if abs_value >= 1_000_000_000:
            formatted = f"{abs_value / 1_000_000_000:.{decimals}f}B"
        elif abs_value >= 1_000_000:
            formatted = f"{abs_value / 1_000_000:.{decimals}f}M"
        elif abs_value >= 1_000:
            formatted = f"{abs_value / 1_000:.{decimals}f}K"
        else:
            formatted = f"{abs_value:.{decimals}f}"

        return f"{sign}{formatted}"
    except (ValueError, TypeError):
        return "N/A"


def format_volume(value: Union[int, float]) -> str:
    """
    Format trading volume with appropriate suffix

    Args:
        value: Volume value

    Returns:
        Formatted volume string

    Examples:
        >>> format_volume(2500000)
        '2.5M'
        >>> format_volume(1500)
        '1,500'
    """
    try:
        if value is None:
            return "N/A"

        if value >= 1_000_000:
            return f"{value / 1_000_000:.1f}M"
        else:
            return f"{value:,.0f}"
    except (ValueError, TypeError):
        return "N/A"


def format_change(value: Union[int, float],
                 is_percentage: bool = False,
                 decimals: int = 2) -> str:
    """
    Format a change value with color indicator

    Args:
        value: Change value
        is_percentage: Whether value is a percentage
        decimals: Number of decimal places

    Returns:
        Formatted change string with sign

    Examples:
        >>> format_change(5.2, is_percentage=True)
        '+5.20%'
        >>> format_change(-10.5)
        '-10.50'
    """
    try:
        if value is None:
            return "N/A"

        sign = "+" if value > 0 else ""
        suffix = "%" if is_percentage else ""

        formatted = f"{value:.{decimals}f}"
        return f"{sign}{formatted}{suffix}"
    except (ValueError, TypeError):
        return "N/A"


def truncate_text(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """
    Truncate text to a maximum length

    Args:
        text: Text to truncate
        max_length: Maximum length before truncation
        suffix: Suffix to add when truncated

    Returns:
        Truncated text

    Examples:
        >>> truncate_text("This is a very long text that needs truncation", 20)
        'This is a very lo...'
    """
    if not text:
        return ""

    if len(text) <= max_length:
        return text

    return text[:max_length - len(suffix)] + suffix


def format_date(date_obj, format_str: str = "%Y-%m-%d") -> str:
    """
    Format a date object to string

    Args:
        date_obj: Date or datetime object
        format_str: Format string (default: YYYY-MM-DD)

    Returns:
        Formatted date string

    Examples:
        >>> from datetime import date
        >>> format_date(date(2025, 1, 15))
        '2025-01-15'
    """
    try:
        if date_obj is None:
            return "N/A"
        return date_obj.strftime(format_str)
    except (ValueError, AttributeError):
        return "N/A"


def format_sentiment_label(score: float) -> str:
    """
    Format sentiment score as colored label

    Args:
        score: Sentiment score (-100 to 100)

    Returns:
        Sentiment label string
    """
    if score >= 60:
        return "🚀 Very Bullish"
    elif score >= 30:
        return "↗️ Bullish"
    elif score >= -30:
        return "➡️ Neutral"
    elif score >= -60:
        return "↘️ Bearish"
    else:
        return "📉 Very Bearish"
