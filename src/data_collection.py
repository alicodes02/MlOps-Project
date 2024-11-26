import os
import requests
import pandas as pd
from datetime import datetime, timedelta
import json
from dotenv import load_dotenv

class WeatherDataCollector:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        
    def collect_weather_data(self, city="London", days=5):
        data_list = []
        
        for i in range(days):
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(self.base_url, params=params)
            if response.status_code == 200:
                data = response.json()
                
                weather_data = {
                    'temperature': data['main']['temp'],
                    'humidity': data['main']['humidity'],
                    'wind_speed': data['wind']['speed'],
                    'weather_condition': data['weather'][0]['main'],
                    'date_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
                data_list.append(weather_data)
            
        df = pd.DataFrame(data_list)
        os.makedirs('data/raw', exist_ok=True)
        df.to_csv('data/raw/raw_data.csv', index=False)
        return df

def main():
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv('WEATHER_API_KEY')
    if not api_key:
        raise ValueError("No API key found. Please set WEATHER_API_KEY in .env file")
    
    # Collect data
    collector = WeatherDataCollector(api_key)
    collector.collect_weather_data()

if __name__ == "__main__":
    main()