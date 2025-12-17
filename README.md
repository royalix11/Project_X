# Project_X

## S&P 500 animation script

This repository contains a simple Python script that downloads the full available history of the S&P 500 (ticker `^GSPC`) from Yahoo Finance and animates the closing price over time.

### Setup

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the animation:

   ```bash
   python sp500_animation.py
   ```

Each time you run the script it will fetch fresh data and animate the chart from the beginning, showing the S&P 500's historical trajectory.
