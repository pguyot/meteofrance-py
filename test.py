# -*- coding: utf-8 -*-
from meteofrance.client import meteofranceClient, meteofranceError
import time
import unittest

class TestLocation(unittest.TestCase):
  def test_oslo(self):
    client = meteofranceClient('oslo, norvege', True, include_today=True)
    data = client.get_data()
    self.assertEqual(data['name'], 'Oslo')
    self.assertEqual(data['printName'], u'Oslo (Norvège)')

  def test_luxembourg(self):
    client = meteofranceClient('luxembourg', True, include_today=True)
    data = client.get_data()
    self.assertEqual(data['name'], 'Luxembourg')
    self.assertEqual(data['printName'], u'Luxembourg (Luxembourg )')

  def test_postal_code(self):
    client = meteofranceClient('80000', True, include_today=True)
    data = client.get_data()
    self.assertEqual(data['name'], 'Amiens')
    self.assertEqual(data['dept'], '80')
    self.assertEqual(data['printName'], 'Amiens (80000)')

  def test_city_name(self):
    client = meteofranceClient('Brest', True, include_today=True)
    data = client.get_data()
    self.assertEqual(data['name'], 'Brest')
    self.assertEqual(data['printName'], u'Brest (Biélorussie)')

  #postal code is not correct : should return the first result which is "Ableiges"
  def test_department(self):
    client = meteofranceClient('95', True, include_today=True)
    data = client.get_data()
    self.assertEqual(data['name'], 'Ableiges')
    self.assertEqual(data['printName'], 'Ableiges (95450)')

  def f_test_invalid(self):
    meteofranceClient('foobar')

  def test_invalid(self):
    self.assertRaises(meteofranceError, self.f_test_invalid)

class TestClientData(unittest.TestCase):
  def test_beynost(self):
    client = meteofranceClient('01700', include_today=True)
    client.need_rain_forecast = False
    client.update()
    data = client.get_data()
    self.assertIn('name', data)
    self.assertIn('dept', data)
    self.assertIn('fetched_at', data)
    self.assertIn('forecast', data)
    self.assertIn('freeze_chance', data)
    self.assertIn('rain_chance', data)
    self.assertIn('snow_chance', data)
    self.assertIn('temperature', data)
    self.assertIn('thunder_chance', data)
    self.assertIn('uv', data)
    self.assertIn('weather_class', data)
    self.assertIn('weather', data)
    self.assertIn('wind_bearing', data)
    self.assertIn('wind_speed', data)
    self.assertNotIn('next_rain_intervals', data)
    self.assertNotIn('next_rain', data)
    self.assertNotIn('next_rain_datetime', data)
    self.assertNotIn('rain_forecast_text', data)
    self.assertNotIn('rain_forecast', data)
    self.assertEqual(len(data['forecast']), 14)

  # pointe-a-pitre : result from meteo-france is different and it returns less data
  def test_pointe_a_pitre(self):
    client = meteofranceClient('97110', include_today=True)
    client.need_rain_forecast = False
    client.update()
    data = client.get_data()
    self.assertIn('name', data)
    self.assertNotIn('dept', data)
    self.assertIn('fetched_at', data)
    self.assertIn('forecast', data)
    self.assertNotIn('freeze_chance', data)
    self.assertNotIn('rain_chance', data)
    self.assertNotIn('snow_chance', data)
    self.assertIn('temperature', data)
    self.assertNotIn('thunder_chance', data)
    self.assertIn('uv', data)
    self.assertIn('weather_class', data)
    self.assertIn('weather', data)
    self.assertIn('wind_bearing', data)
    self.assertIn('wind_speed', data)
    self.assertNotIn('next_rain_intervals', data)
    self.assertNotIn('next_rain', data)
    self.assertNotIn('next_rain_datetime', data)
    self.assertNotIn('rain_forecast_text', data)
    self.assertNotIn('rain_forecast', data)
    self.assertGreaterEqual(len(data['forecast']), 9)

  # Same with world data
  def test_pointe_a_pitre(self):
    client = meteofranceClient('Tokyo', include_today=True)
    client.need_rain_forecast = False
    client.update()
    data = client.get_data()
    self.assertIn('name', data)
    self.assertNotIn('dept', data)
    self.assertIn('fetched_at', data)
    self.assertIn('forecast', data)
    self.assertNotIn('freeze_chance', data)
    self.assertNotIn('rain_chance', data)
    self.assertNotIn('snow_chance', data)
    self.assertIn('temperature', data)
    self.assertNotIn('thunder_chance', data)
    self.assertNotIn('uv', data)
    self.assertIn('weather_class', data)
    self.assertIn('weather', data)
    self.assertIn('wind_bearing', data)
    self.assertIn('wind_speed', data)
    self.assertNotIn('next_rain_intervals', data)
    self.assertNotIn('next_rain', data)
    self.assertNotIn('rain_forecast_text', data)
    self.assertNotIn('rain_forecast', data)
    self.assertGreaterEqual(len(data['forecast']), 9)

class TestRainForecast(unittest.TestCase):
  def test_rain_forecast_is_updated(self):
    client = meteofranceClient('01700', include_today=True)
    client.need_rain_forecast = False
    client.update()
    self.assertEqual(client.need_rain_forecast, False)
    data = client.get_data()
    self.assertNotIn('next_rain_intervals', data)
    self.assertNotIn('next_rain', data)
    self.assertNotIn('next_rain_datetime', data)
    self.assertNotIn('rain_forecast_text', data)
    self.assertNotIn('rain_forecast', data)
    client.need_rain_forecast = True
    client.update()
    self.assertEqual(client.need_rain_forecast, True)
    data = client.get_data()
    self.assertIn('next_rain_intervals', data)
    self.assertIn('next_rain', data)
    self.assertIn('next_rain_datetime', data)
    self.assertIn('rain_forecast_text', data)
    self.assertIn('rain_forecast', data)

  #marseille : no rain forecast
  def test_marseille(self):
    client = meteofranceClient(13000, True, include_today=True)
    data = client.get_data()
    self.assertNotIn('next_rain_intervals', data)
    self.assertNotIn('next_rain', data)
    self.assertNotIn('next_rain_datetime', data)
    self.assertNotIn('rain_forecast_text', data)
    self.assertNotIn('rain_forecast', data)

  #Rouen : rain forecast available
  def test_rouen(self):
    client = meteofranceClient(76000, True, include_today=True)
    data = client.get_data()
    self.assertIn('next_rain_intervals', data)
    self.assertIn('next_rain', data)
    self.assertIn('next_rain_datetime', data)
    self.assertIn('rain_forecast_text', data)
    self.assertIn('rain_forecast', data)

class TestOldAPI(unittest.TestCase):
  def test_beynost(self):
    new_client = meteofranceClient('01700', include_today=True)
    new_client.need_rain_forecast = False
    old_client = meteofranceClient('01700', include_today=False)
    old_client.need_rain_forecast = False
    new_client.update()
    old_client.update()
    new_data = new_client.get_data()
    self.assertEqual(len(new_data['forecast']), 14)
    old_data = old_client.get_data()
    self.assertEqual(len(old_data['forecast']), 5)
    self.assertEqual(new_data['forecast'][1], old_data['forecast'][0])
    self.assertEqual(new_data['forecast'][2], old_data['forecast'][1])
    self.assertEqual(new_data['forecast'][3], old_data['forecast'][2])
    self.assertEqual(new_data['forecast'][4], old_data['forecast'][3])
    self.assertEqual(new_data['forecast'][5], old_data['forecast'][4])

if __name__ == '__main__':
    unittest.main()
