import yfinance as yf
from arch import unitroot
import pandas as pd
import statsmodels.api as sm
from arch import unitroot
from preprocessing import import_stock_list,import_price

stock_list=import_stock_list(index_code="XU030")
print(stock_list)
df = pd.DataFrame(columns=["Main", "Pair", "Slope", "Lag", "PValue"])

for main in stock_list:
    main_price=import_price(stock_code=main,start_date='2023-12-31',end_date="2024-11-12")
    for pair in stock_list:
        if main == pair:
            continue
        else:
            pair_price=import_price(stock_code=pair,start_date='2023-12-31',end_date="2024-11-12")
            if len(main_price) != len(pair_price):
                continue
            else:
                adf_main=unitroot.ADF(main_price, trend="ct", method="aic")
                adf_pair=unitroot.ADF(pair_price, trend="ct", method="aic")
                adf_main_diff=unitroot.ADF(main_price.diff().dropna(), trend="c", method="aic")
                adf_pair_diff=unitroot.ADF(pair_price.diff().dropna(), trend="c", method="aic")
                eg_test = unitroot.engle_granger(main_price, pair_price,trend="ct",method="aic")
                if adf_main.pvalue > 0.05 and adf_pair.pvalue > 0.05 and \
                        adf_main_diff.pvalue < 0.05 and adf_pair_diff.pvalue < 0.05 and \
                        eg_test.pvalue < 0.05:
                    model = sm.OLS(main_price,sm.add_constant(pair_price)).fit()
                    slope = model.params[1]
                    lag=eg_test.lags
                    pvalue = eg_test.pvalue
                    df=df._append({"Main":main,"Pair":pair,"Slope":slope,"Lag":lag,"PValue":pvalue},ignore_index=True)
print(df)