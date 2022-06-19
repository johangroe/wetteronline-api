==========
Quickstart
==========

Ready to get started?

Basic usage
###########

.. code-block:: python

   >> import wetteronline
   >> l = wetteronline.location("New York")
   >> l.url
   "wetter/new-york-city"
   >> w = wetteronline.weather("wetter/new-york-city")
   >> w.temperature
   18 # °C


Advanced usage
##############

.. code-block:: python
   >> import wetteronline
   >> l = wetteronline.location("New York")
   >> l.autosuggests
   ['New York', 'New York Mills, New York', 'New York, Missouri', 'New York Mills, Minnesota']
   >> w = wetteronline.weather(l.url)
   >> w.forecast_4d
   {'19.06.': {
      'maxTemperature': 24, 
      'minTemperature': 13, 
      'sunHours': 13, 
      'precipitationProbability': 10
      }, 
   '20.06.': {
      'maxTemperature': 27, 
      'minTemperature': 13, 
      'sunHours': 13, 
      'precipitationProbability': 5
      }, 
   '21.06.': {
      'maxTemperature': 25, 
      'minTemperature': 15, 
      'sunHours': 3, 
      'precipitationProbability': 80
      }, 
   '22.06.': {
      'maxTemperature': 27, 
      'minTemperature': 18, 
      'sunHours': 8, 
      'precipitationProbability': 50
      }
   }
