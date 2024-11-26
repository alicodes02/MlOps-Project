import os
import pandas as pd
from sklearn.preprocessing import StandardScaler

class DataPreprocessor:
    def __init__(self):
        self.scaler = StandardScaler()
        
    def preprocess_data(self, input_path, output_path):
        # Read data
        df = pd.read_csv(input_path)
        
        # Handle missing values
        df = df.fillna(df.mean(numeric_only=True))
        
        # Normalize numerical fields
        numerical_cols = ['temperature', 'humidity', 'wind_speed']
        df[numerical_cols] = self.scaler.fit_transform(df[numerical_cols])
        
        # Save preprocessed data
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        return df

def main():
    preprocessor = DataPreprocessor()
    preprocessor.preprocess_data(
        input_path='data/raw/raw_data.csv',
        output_path='data/processed/processed_data.csv'
    )

if __name__ == "__main__":
    main()