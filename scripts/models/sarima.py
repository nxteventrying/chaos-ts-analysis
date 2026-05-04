#ARIMA, SARIMA y SARIMAX
from pmdarima import auto_arima

def sarima_tesis(df,test_days):

  # Split the Data into Training and Test

  train, test = df.iloc[:-test_days], df.iloc[-test_days:]


  model_sarima = auto_arima(train['y'],
                            m = 7,
                            supprese_warnings = True)
  #model_sarima.summary()
  predictions_sarima = model_sarima.predict(n_periods = len(test))
  return predictions_sarima