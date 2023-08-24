from statsmodels.tsa.api import adfuller
from statsmodels.api import add_constant, OLS
from scipy.stats import linregress, pearsonr,spearmanr, shapiro, skew, kurtosis
import yfinance as yf
import datetime as dt

"""
Cointegration Analysis with Pairs Trading Strategy

This Python script performs cointegration analysis between a main stock and a list of pair stocks.
The main objective is to identify pairs of stocks that exhibit cointegration, a long-term relationship,
which can be utilized in a pairs trading strategy. Pairs trading involves taking advantage of deviations
from the cointegrated relationship by simultaneously buying one stock and shorting the other when they
diverge and then closing the positions when they revert to their historical relationship.

The script follows these steps:
1. Imports necessary libraries for data analysis and finance data retrieval.
2. Defines the training period duration (in days) and calculates the start date accordingly.
3. Specifies the main stock and a list of pair stocks to be analyzed.
4. Downloads adjusted close prices of the main stock and calculates its percentage returns.
5. Loops through each pair stock, performing cointegration analysis:
   a. Checks for cointegration in both directions between the main stock and the pair stock.
   b. If cointegration is detected in either direction:
      - Calculates correlation between the main stock and pair stock.
      - Performs linear regression analysis to determine the relationship between their returns.
      - Stores analysis results including correlation, regression parameters, and p-values.
   c. Prints a message if cointegration is not detected for a specific pair.
   d. Handles exceptions that may occur during the analysis.
6. Prints the analysis results for each cointegrated pair, including correlation, regression parameters,
   and other relevant statistics.

To use the script:
- Set the 'train' variable to the desired training period in days.
- Specify the 'main' stock ticker symbol.
- Provide a list of 'pair_list' containing the ticker symbols of potential pair stocks.
- Run the script to perform cointegration analysis and receive insights into potential pairs for
  a pairs trading strategy.
  
"""
train = 235
start_date = dt.datetime.now()  # Today
date_days = dt.timedelta(days=train)
start_date = start_date - date_days
start_date_str = start_date.strftime('%Y-%m-%d') # Previous date up to the number of Train days

main = "AKBNK.IS"
pair_list = ['ALARK.IS', 'ARCLK.IS', 'ASELS.IS', 'ASTOR.IS', 'BIMAS.IS', 'EKGYO.IS', 'ENKAI.IS', 'EREGL.IS']

main_dataset = yf.download(main, start=start_date_str)["Adj Close"]
main_returns = main_dataset.pct_change().dropna(how="all")

pair_results = []  #To store pair results

for stock in pair_list:
    pair_dataset = yf.download(stock, start=start_date_str)["Adj Close"]
    try:
        # Cointegration check
        resid1 = OLS(main_dataset, add_constant(pair_dataset)).fit().resid
        resid2 = OLS(pair_dataset, add_constant(main_dataset)).fit().resid
        model1 = adfuller(resid1)[1] < 0.05
        model2 = adfuller(resid2)[1] < 0.05
        
        if model1 or model2:
            pair_set = {}  # To create a dictionary for each pair
            pair_set["Main"] = main.replace(".IS", "")
            pair_set["Pair"] = stock.replace(".IS", "")
            pair_returns = pair_dataset.pct_change().dropna(how="all")
            if((shapiro(main_returns)[1] > 0.05 and shapiro(pair_returns)[1] > 5) or \
               (skew(main_returns) < 2 and skew(main_returns) > -2 and skew(pair_returns)<2 and kurtosis(pair_returns)>-2)
               ):
                correlation_method = "Pearson"
                correlation = round(pearsonr(pair_dataset, main_dataset)[0],5)
                pvalue = round(pearsonr(pair_dataset, main_dataset)[1],5)
            else:
                correlation_method = "Spearman"
                correlation = round(spearmanr(pair_dataset, main_dataset)[0],5)
                pvalue = round(spearmanr(pair_dataset, main_dataset)[1],5)
            pair_set["correlation_method"] = correlation_method
            pair_set["Correlation P-Value"] = pvalue
            pair_set["Correlation"] = correlation
            # linear regression and statistics
            slope, intercept, r_value, p_value, std_err = linregress(pair_dataset, main_dataset)
            pair_set["Regregression P-Value"] = round(p_value,5)
            pair_set["Slope"] = round(slope,5)
            pair_set["Intercept"] = round(intercept,5)
            pair_set["R^2"] = round(r_value ** 2,5)
            pair_results.append(pair_set)  # To add the results to the list.

    except Exception as e:
        print(f"Error analyzing {stock}: {e}")

# pair results
for result in pair_results:
    print(result)