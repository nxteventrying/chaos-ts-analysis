from pmdarima import auto_arima

def sarimax_tesis(df,test_days):
  # Split the Data into Training and Test
  train, test = df.iloc[:-test_days], df.iloc[-test_days:]
  # Split the regressor data
  exog_train, exog_test = df.iloc[:-test_days, 1:3], df.iloc[-test_days:,1:3]

  model_sarimax = auto_arima(train['y'],
                            m = 7,
                            X = exog_train,
                            supress_warnings = True)

  predictions_sarimax = model_sarimax.predict(n_periods = len(test),
                                              X = exog_test)
  return predictions_sarimax