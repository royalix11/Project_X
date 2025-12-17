"""Animate the historical S&P 500 closing prices.

Run this script directly to fetch the full available history of the S&P 500
(^GSPC) from Yahoo Finance and animate the closing price evolution over time.
"""
from __future__ import annotations

from datetime import datetime
from functools import lru_cache
from typing import Iterable

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
from matplotlib.animation import FuncAnimation


@lru_cache(maxsize=1)
def load_sp500_history() -> pd.DataFrame:
    """Return the full available S&P 500 price history.

    The data is retrieved from Yahoo Finance using yfinance. Results are cached
    for the life of the process so the download is only performed once per run.
    """

    history = yf.Ticker("^GSPC").history(period="max", auto_adjust=False)
    if history.empty or "Close" not in history:
        raise RuntimeError("Could not load S&P 500 history from Yahoo Finance.")

    data = history.reset_index()[["Date", "Close"]]
    data["Date"] = pd.to_datetime(data["Date"])
    return data


def _format_axes(ax: plt.Axes, dates: Iterable[pd.Timestamp], prices: Iterable[float]) -> None:
    ax.set_title("S&P 500 Closing Prices (all available history)")
    ax.set_ylabel("Index Level")
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))
    if dates:
        ax.set_xlim(min(dates), max(dates))
    if prices:
        price_min, price_max = min(prices), max(prices)
        padding = (price_max - price_min) * 0.05 or 10
        ax.set_ylim(price_min - padding, price_max + padding)


def animate_prices(data: pd.DataFrame) -> None:
    dates = list(data["Date"].dt.to_pydatetime())
    closes = data["Close"].tolist()

    plt.style.use("seaborn-v0_8")
    fig, ax = plt.subplots(figsize=(12, 6))
    line, = ax.plot([], [], lw=2.5, color="navy")
    marker, = ax.plot([], [], "o", color="crimson")
    label = ax.text(0.02, 0.95, "", transform=ax.transAxes, fontsize=11, va="top")

    _format_axes(ax, dates, closes)

    def init():
        line.set_data([], [])
        marker.set_data([], [])
        label.set_text("")
        return line, marker, label

    def update(frame: int):
        current_dates = dates[: frame + 1]
        current_prices = closes[: frame + 1]
        line.set_data(current_dates, current_prices)
        if current_dates:
            marker.set_data(current_dates[-1], current_prices[-1])
            label.set_text(
                f"{current_dates[-1].date().isoformat()}: {current_prices[-1]:.2f}"
            )
        return line, marker, label

    FuncAnimation(
        fig,
        update,
        init_func=init,
        frames=len(dates),
        interval=20,
        blit=True,
        repeat=False,
    )

    plt.tight_layout()
    plt.show()


def main() -> None:
    data = load_sp500_history()
    animate_prices(data)


if __name__ == "__main__":
    main()
