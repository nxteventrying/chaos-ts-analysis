#Le Prophet
from prophet import Prophet


def prophet_tesis(df,test_days):
  def prophet_trans_df(df):
    df = df.copy()
    df = df.reset_index() #la fecha debe ser una columna, no un indice
    df = df.rename(columns = {'date':'ds'})
    return df

  df_prophet = prophet_trans_df(df)

  train_p = df_prophet.iloc[:-test_days]
  test_p = df_prophet.iloc[-test_days:]

  model = Prophet(
      yearly_seasonality=True,    # Auto-detect yearly patterns (adjust if needed)
      weekly_seasonality=True,   # Auto-detect weekly patterns
      daily_seasonality=False,   # Disable daily (since data is daily but no sub-daily patterns)
      seasonality_mode='additive'
  )

  # Add exogenous variables as regressors
  model.add_regressor('exo_1')
  model.add_regressor('exo_2')

  # Fit the model
  model.fit(train_p)

  # Generate future dates
  future = model.make_future_dataframe(periods=test_days, freq='D')

  # Merge exogenous variables from original data
  future = future.merge(df_prophet[['ds', 'exo_1', 'exo_2']], on='ds', how='left')

  # Predict
  forecast = model.predict(future)
  predictions_prophet = forecast[['ds', 'yhat']].tail(test_days)
  predictions_prophet = predictions_prophet.set_index('ds')
  return predictions_prophet