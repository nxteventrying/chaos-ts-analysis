from models.arima import arima_tesis
from models.sarima import sarima_tesis
from models.sarimax import sarimax_tesis
from models.prophet import prophet_tesis
from models.lstm import lstm_tesis
from models.nbeats import nbeats_tesis
from models.tft import tft_tesis

def predictions_enssemble(df, test_days):
    predictions_arima = arima_tesis(df,test_days)
    predictions_sarima = sarima_tesis(df,test_days)
    predictions_sarimax = sarimax_tesis(df,test_days)
    predictions_prophet = prophet_tesis(df,test_days)
    predictions_lstm = lstm_tesis(df, test_days)
    predictions_nbeats = nbeats_tesis(df, test_days)
    predictions_tft = tft_tesis(df, test_days)
    return {'ARIMA':predictions_arima,
            'SARIMA' :predictions_sarima,
            'SARIMAX' : predictions_sarimax,
            'PROPHET' :predictions_prophet,
            'LSTM':predictions_lstm,
            'NBEATS' : predictions_nbeats,
            'TFT' : predictions_tft}