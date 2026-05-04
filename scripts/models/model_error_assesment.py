import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error

def model_assessment(test,predictions, chart_title):
  plt.figure(figsize = (10,4))
  #plt.plot(train, label = 'Train')
  plt.plot(test, label = 'test')
  plt.plot(predictions, label = 'Forecast')
  plt.title(chart_title)
  plt.legend()
  plt.show()

  mae = mean_absolute_error(test, predictions)
  rmse = mean_squared_error(test, predictions) ** 0.5
  mape = mean_absolute_percentage_error(test, predictions)

  print(f'The MAE is {mae:.2f}')
  print(f'The RMSE is {rmse:.2f}')
  print(f'The MAPE is {100 * mape:.2f} %')