from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from src.data_collection import WeatherDataCollector
from src.data_preprocessing import DataPreprocessor
from src.model_training import WeatherModel

# Load environment variables
load_dotenv()

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 12, 6),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'weather_pipeline',
    default_args=default_args,
    description='Weather data pipeline',
    schedule_interval=timedelta(days=1),
)

def collect_data():
    """Collect weather data from multiple cities"""
    collector = WeatherDataCollector(os.getenv('WEATHER_API_KEY'))
    collector.collect_weather_data(
        cities=["London", "New York", "Tokyo", "Paris", "Sydney"],
        interval_seconds=2,
        samples_per_city=3
    )

def preprocess_data():
    """Preprocess the collected weather data"""
    preprocessor = DataPreprocessor()
    preprocessor.preprocess_data(
        input_path='data/raw/raw_data.csv',
        output_path='data/processed/processed_data.csv'
    )

def train_model():
    """Train the weather prediction model"""
    model = WeatherModel()
    model.train_model(
        data_path='data/processed/processed_data.csv',
        model_path='models/model.pkl'
    )

# Define DAG tasks
collect_task = PythonOperator(
    task_id='collect_data',
    python_callable=collect_data,
    dag=dag,
)

preprocess_task = PythonOperator(
    task_id='preprocess_data',
    python_callable=preprocess_data,
    dag=dag,
)

train_task = PythonOperator(
    task_id='train_model',
    python_callable=train_model,
    dag=dag,
)

# Set task dependencies
collect_task >> preprocess_task >> train_task