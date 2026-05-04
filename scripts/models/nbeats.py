# Darts functions
from darts.timeseries import TimeSeries
from darts.utils.timeseries_generation import datetime_attribute_timeseries
from darts.dataprocessing.transformers import Scaler
from darts.models import NBEATSModel

def nbeats_tesis(df, test_days):
  '''
  So, we have that the dataframe needs to give the exogenous variables during training and
  forecasting, so we use the dataframe for training without the last n points (31 for this case).

  Then we use the whole exogenous variables length considering all of it for prediction

  The main difference
  '''

  df_training = df.iloc[:-test_days]
  series = TimeSeries.from_dataframe(df_training,
                                    value_cols = 'y',
                                    freq = 'D')
  covariates_training = TimeSeries.from_dataframe(df_training.iloc[:,1:],
                                                  freq = 'D')

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



  # Isolating the Past Covariates
  X_past = df.iloc[:,2:]
  # Convert the isolated past covariates into a TimeSeries object with Hourly frequency
  past_covariates = TimeSeries.from_dataframe(X_past,
                                              freq = 'H')
  # Import the Scaler class and initialize two instances of it
  scaler1 = Scaler()
  scaler2 = Scaler()
  # Apply the scaler1 to the time series
  y_transformed = scaler1.fit_transform(series)
  # Apply the scaler2 to the past covariates
  past_covariates_transformed = scaler2.fit_transform(past_covariates)


  # Set the forecasting horizon
  forecast_horizon = test_days

  # Define the N-BEATS model with specified parameters
  model = NBEATSModel(
      input_chunk_length = 96,                     # Length of the input sequence
      output_chunk_length = forecast_horizon,      # Length of the forecast sequence
      add_encoders = add_encoders,                 # Additional encoders to use
      random_state = 1502,                         # Seed for reproducibility
      n_epochs = 10,                               # Number of training epochs
      batch_size = 64,                             # Size of training batches
      num_stacks = 30,                             # Number of stacks in the model
      num_blocks = 1,                              # Number of blocks per stack
      num_layers = 4,                              # Number of layers per block
      layer_widths = 512,                          # Width of each layer
      #pl_trainer_kwargs = {'accelerator' : 'cpu'}
      pl_trainer_kwargs = {'accelerator': 'gpu',   # Training on GPU
                         'devices': [0]}
  )

  # Fit the model to the transformed time series data with past covariates
  model.fit(y_transformed,
            past_covariates = past_covariates_transformed)


  # Forecast the future
  forecast = model.predict(n = forecast_horizon,
                                series = y_transformed,
                                past_covariates = past_covariates_transformed)

  # Inverse transform the forecast to original scale
  predictions_nbeats = TimeSeries.pd_series(
      scaler1.inverse_transform(forecast)).rename("N-BEATS")
  return predictions_nbeats