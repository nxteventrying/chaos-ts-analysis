# Darts functions
from darts.timeseries import TimeSeries
from darts.utils.timeseries_generation import datetime_attribute_timeseries
from darts.dataprocessing.transformers import Scaler
from darts.models import TFTModel

def tft_tesis(df, test_days):

  '''
  So, we have that the dataframe needs to give the exogenous variables during training and
  forecasting, so we use the dataframe for training without the last n points (31 for this case).

  Then we use the whole exogenous variables length considering all of it for prediction

  The main difference
  '''
  df_training = df.iloc[:-test_days]
  series = TimeSeries.from_dataframe(df_training,
                                    value_cols = 'y')
  covariates_training = TimeSeries.from_dataframe(df_training.iloc[:,1:])

  # Function to encode the year as a normalized value
  def encode_year(idx):
    return (idx.year - 2000) / 50

  # Set up the add_encoders dictionary to specify how different time-related encoders and transformers should be applied
  add_encoders = {
      'cyclic': {'future': ['hour', 'day', 'dayofweek', 'week','month']},
      'datetime_attribute': {'future': ['hour', 'day', 'dayofweek', 'week','month']},
      'position': {'past': ['relative'], 'future': ['relative']},
      'custom': {'past': [encode_year], 'future': [encode_year]},
      'transformer': Scaler(),
      'tz': 'CET'
  }

  X = df.iloc[:,1:]
  covariates_prediction = TimeSeries.from_dataframe(X)


  # Import the Scaler class and initialize two instances of it
  scaler1 = Scaler()
  scaler2 = Scaler()

  # Apply the scaler1 to the time series
  y_transformed = scaler1.fit_transform(series)

  # Apply the scaler2 to the past and future covariates
  past_covariates_transformed = scaler2.fit_transform(covariates_training)
  future_covariates_transformed = scaler2.fit_transform(covariates_prediction)

  # Set the forecasting horizon
  forecasting_horizon = test_days

  # Build and configure the TFT (Temporal Fusion Transformer) model
  model = TFTModel(
      input_chunk_length=96,  # Number of time steps in the input sequence
      output_chunk_length=forecasting_horizon,  # Number of time steps to predict
      hidden_size=16,  # Number of hidden units in the model
      lstm_layers=2,  # Number of LSTM layers
      num_attention_heads=4,  # Number of attention heads in the attention mechanism
      dropout=0.1,  # Dropout rate to prevent overfitting
      batch_size=64,  # Batch size for training
      n_epochs=10,  # Number of epochs for training
      add_encoders=add_encoders,  # Encoders configuration for the model
      use_static_covariates=True,  # Whether to use static covariates
      #pl_trainer_kwargs = {'accelerator' : 'cpu'}
      pl_trainer_kwargs={'accelerator': 'gpu', 'devices': [0]}  # Trainer configuration for using GPU
  )

  # Fit the model to the time series data with past and future covariates
  model.fit(
      y_transformed,
      past_covariates=past_covariates_transformed,
      future_covariates=future_covariates_transformed
  )


  # Generate forecasts for the future using the tuned model
  forecast = model.predict(n = forecasting_horizon,
                                series = y_transformed,
                                past_covariates = past_covariates_transformed,
                                future_covariates = future_covariates_transformed)

  # Inverse transform the forecasted values to the original scale and rename the series
  predictions_tft = TimeSeries.pd_series(scaler1.inverse_transform(forecast)).rename("TFT")
  return predictions_tft