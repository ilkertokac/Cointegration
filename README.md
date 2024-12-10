# Cointegration Analysis and Volatility Forecasting
This repository provides a Python-based framework to:

Download constituent companies of selected indices.
Retrieve price data for the companies.
Identify cointegrated stock pairs using statistical tests.
Estimate volatility for selected stocks using GARCH models.

The tool is ideal for quantitative analysts and traders interested in pair trading strategies and volatility modeling.

# Features

Index Constituents Fetching: Automatically retrieves the list of companies from specified indices.
Price Data Retrieval: Downloads historical price data for each company in the selected indices.
Cointegration Analysis:
  Tests each stock pair for cointegration using the Engle-Granger two-step method.
  Logs cointegrated pairs along with model parameters (beta, intercept, and lag values).
Volatility Forecasting: Applies GARCH models to predict future volatility for selected stocks.

# Installation

Clone the repository:
  git clone https://github.com/ilkertokac/Cointegration.git
  cd Cointegration
Install dependencies:
pip install -r requirements.txt

# Output
Stock 1	Stock 2	Beta	Intercept	Lag
ABC	      XYZ	  1.05	  0.03	   2

# Author

Developed by İlker Tokaç.
For inquiries, reach out at ilkrtkc34@gmail.com.
