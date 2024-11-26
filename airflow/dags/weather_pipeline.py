from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from src.data_collection import WeatherDataCollector
from src.data_preprocessing import DataPreprocessor
from src.model_training import WeatherModel

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
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
    collector = WeatherDataCollector(os.getenv('WEATHER_API_KEY'))
    collector.collect_weather_data()

def preprocess_data():
    preprocessor = DataPreprocessor()
    preprocessor.preprocess_data(
        'data/raw/raw_data.csv',
        'data/processed/processed_data.csv'
    )

def train_model():
    model = WeatherModel()
    model.train_model(
        'data/processed/processed_data.csv',
        'models/model.pkl'
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