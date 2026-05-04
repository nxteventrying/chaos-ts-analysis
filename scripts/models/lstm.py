# Darts functions
from darts.timeseries import TimeSeries
from darts.utils.timeseries_generation import datetime_attribute_timeseries
from darts.dataprocessing.transformers import Scaler
from darts.models import RNNModel
import pandas as pd


def covariates_trans(series, covariates, dataframe):
  # Create a TimeSeries instances

  # Year
  year_series = datetime_attribute_timeseries(
      pd.date_range(start = series.start_time(),
                    freq = series.freq_str,
                    periods = dataframe.shape[0]),
                    attribute = "year",
                    one_hot = False)
  # Month
  month_series = datetime_attribute_timeseries(year_series,
                                              attribute = "month",
                                              one_hot = True)
  # Weekday
  weekday_series = datetime_attribute_timeseries(year_series,
                                              attribute = "weekday",
                                              one_hot = True)

  # Import the Scaler class and initialize two instances of it
  scaler1 = Scaler()
  scaler2 = Scaler()

  # Apply the scaler to the time series
  y_transformed = scaler1.fit_transform(series)

  # Scale the covariates with additional datetime attributes

  # Stack the year_series attribute with the covariates
  covariates = covariates.stack(year_series)

  # Apply scaling to the covariates
  covariates_transformed = scaler2.fit_transform(covariates)
  # Stack the month_series attribute with the already scaled covariates
  covariates_transformed = covariates_transformed.stack(month_series)
  # Stack the weekday_series attribute with the already scaled covariates
  covariates_transformed = covariates_transformed.stack(weekday_series)

  return scaler1, scaler2,  y_transformed, covariates_transformed

def lstm_tesis(df,test_days):
  '''
  So, we have that the dataframe needs to give the exogenous variables during training and
  forecasting, so we use the dataframe for training without the last n points (31 for this case).

  Then we use the whole exogenous variables length considering all of it for prediction

  The main difference
  '''

  df_training = df.iloc[:-test_days]
  series = TimeSeries.from_series(df_training.y)
  covariates_training = TimeSeries.from_dataframe(df_training.iloc[:,1:])

  X = df.iloc[:,1:]
  covariates_prediction = TimeSeries.from_dataframe(X)

  scaler1, scaler2, y_transformed, covariates_transformed = covariates_trans(series, covariates_training,df_training)

  forecasting_horizon = test_days  # Number of periods to forecast into the future
  input_chunk_length = 46  # Number of past periods used for making predictions

  training_length = forecasting_horizon + input_chunk_length  # Total length of the training window

  # Initialize the LSTM model with specified parameters
  model = RNNModel(model = "LSTM",                        # Specify LSTM as the type of RNN model
                  hidden_dim = 20,                       # Set the number of hidden units in LSTM layers
                  n_rnn_layers = 2,                      # Define the number of RNN layers
                  dropout = 0.1,                         # Set dropout rate for regularization
                  n_epochs = 10,                         # Define the number of training epochs
                  optimizer_kwargs = {"lr": 0.003},      # Specify learning rate for the optimizer
                  random_state = 1502,                   # Set random seed for reproducibility
                  training_length = training_length,     # Set the length of the training data
                  input_chunk_length = input_chunk_length,     # Set the length of input chunks for the model
                   #pl_trainer_kwargs = {"accelerator": "cpu"}   # Specify training on CPU
                    pl_trainer_kwargs = {"accelerator": "gpu",
                                        "devices": [0]}
                  )

  # Fit the model with transformed target data and covariates
  model.fit(y_transformed, future_covariates = covariates_transformed)

  scaler1, scaler2, y_transformed_pred, covariates_transformed_pred = covariates_trans(series,covariates_prediction,X)

  # Predict future values using the trained model
  predictions = model.predict(n = test_days,               # Predict for the length of the future data
                              future_covariates = covariates_transformed_pred) # Use transformed covariates for prediction

  # Convert predictions back to the original scale and create a pandas Series with the name "LSTM"
  predictions_lstm = TimeSeries.pd_series(
      scaler1.inverse_transform(predictions)).rename("LSTM")
  return predictions_lstm
