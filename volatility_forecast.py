import pandas as pd
import preprocessing
from arch import arch_model
from matplotlib import pyplot as plt
import numpy as np

def volatility_forecast(stock,start_date,end_date):
    data=pd.DataFrame(preprocessing.import_price(stock_code=stock,start_date=start_date,end_date=end_date).values,columns=[stock])
    print(data)
    returns=data.pct_change().dropna()*100
    vol_model=arch_model(returns,mean="Zero",dist="skewstudent",vol="GARCH",p=1,q=1,o=1).fit(disp="off")
    plt.plot(returns.index,returns,label="Daily Returns")
    plt.plot(returns.index,np.sqrt(vol_model.conditional_volatility),label="Daily Volatility")
    plt.plot(returns.index,np.sqrt(vol_model.conditional_volatility)*np.sqrt(252),label="Yearly Volatility")
    plt.legend()
    plt.grid(visible=True)
    plt.show()
    daily_for=float(vol_model.forecast(horizon=1,method="bootstrap" if len(data)>110 else "analytic").variance.values[-1][0])
    yearly_for=float(daily_for*np.sqrt(252))
    content="Volatility Forecast:\nDaily: {:.2f}\nYearly: {:.2f}".format(daily_for,yearly_for)
    return content