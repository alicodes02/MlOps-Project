import pytest
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

@pytest.fixture(scope="session")
def test_data_dir(tmp_path_factory):
    return tmp_path_factory.mktemp("test_data")

@pytest.fixture(scope="session")
def sample_dates():
    base_date = datetime(2024, 1, 1)
    return [base_date + timedelta(hours=i) for i in range(5)]

@pytest.fixture(scope="session")
def raw_weather_data(sample_dates):
    return pd.DataFrame({
        'temperature': np.random.uniform(15, 25, 5),
        'humidity': np.random.uniform(60, 80, 5),
        'wind_speed': np.random.uniform(4, 8, 5),
        'weather_condition': np.random.choice(['Clear', 'Cloudy', 'Rain'], 5),
        'date_time': [d.strftime('%Y-%m-%d %H:%M:%S') for d in sample_dates]
    })

@pytest.fixture(scope="session")
def api_key():
    key = os.getenv('WEATHER_API_KEY')
    if not key:
        pytest.skip("WEATHER_API_KEY environment variable not set")
    return key