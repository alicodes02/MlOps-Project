import os
import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

class WeatherModel:
    def __init__(self):
        self.model = LinearRegression()
        
    def train_model(self, data_path, model_path):
        # Read preprocessed data
        print(f"Reading data from: {data_path}")
        df = pd.read_csv(data_path)
        
        # Prepare features and target
        print("Preparing features and target...")
        X = df[['humidity', 'wind_speed']]
        y = df['temperature']
        
        # Train model
        print("Training model...")
        self.model.fit(X, y)
        
        # Create models directory if it doesn't exist
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        
        # Save model
        print(f"Saving model to: {model_path}")
        with open(model_path, 'wb') as f:
            pickle.dump(self.model, f)
        print("Model saved successfully!")

def main():
    try:
        model = WeatherModel()
        model.train_model(
            data_path='data/processed/processed_data.csv',
            model_path='models/model.pkl'
        )
    except Exception as e:
        print(f"Error in model training: {str(e)}")
        raise e

if __name__ == "__main__":
    main()