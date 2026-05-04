#ARIMA, SARIMA y SARIMAX
from pmdarima import auto_arima
def arima_tesis(df,test_days):
  # Split the Data into Training and Test
  train, test = df.iloc[:-test_days], df.iloc[-test_days:]

  # using pdarima for the arima model and the best parameters
  model = auto_arima(train['y'],
                    sesasonal = False,
                    supress_warnings = True)
  #model.summary()
  predictions_arima = model.predict(n_periods = len(test))
  return predictions_arima