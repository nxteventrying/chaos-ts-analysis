import matplotlib.pyplot as plt

def model__visual_assessment_comparison(test,predictions_ensemble, chart_title):
  plt.figure(figsize = (10,4))
  #plt.plot(train, color = 'blue',label = 'train')
  plt.plot(test, color = 'blue', marker='*',label = 'test')


  colors = ['lime', 'black', 'purple','red','gray','pink', 'cyan']

  for i, (key, value) in enumerate(predictions_ensemble.items()):
    plt.plot(value, label=key, color=colors[i % len(colors)])

  #for key, value in predictions_ensemble.items():
   # plt.plot(value, label = key)

  plt.title(chart_title)
  plt.legend()
  plt.show()