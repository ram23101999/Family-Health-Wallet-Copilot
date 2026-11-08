import pandas as pd
from ml_model import train_and_get_model

if __name__ == "__main__":
    print("Training Family Health Wallet Risk Prediction Model...")
    model, acc = train_and_get_model()
    print(f"Model Training Complete! Accuracy: {acc * 100:.2f}%")
